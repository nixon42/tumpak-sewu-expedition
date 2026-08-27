#!/usr/bin/env python3
"""
Tumpak Sewu Guide - High-Performance Zero-Dependency HTTP Server & REST API.
Provides static file serving, in-context voting REST API, SQLite (WAL mode)
and atomic JSON dual persistence, CORS support, and thread-safe execution.

Usage:
    python server.py [--port 8000] [--host 0.0.0.0] [--db votes.db] [--json votes.json]
"""

import argparse
import contextlib
import datetime
import http.server
import json
import mimetypes
import os
import posixpath
import re
import signal
import socketserver
import sqlite3
import sys
import threading
import urllib.parse
from typing import Any, Dict, Generator, List, Optional, Tuple

DEFAULT_PORT = 8000
DEFAULT_HOST = "0.0.0.0"
DEFAULT_DB_PATH = "votes.db"
DEFAULT_JSON_PATH = "votes.json"

# Canonical option mapping and standard definitions
ROUTE_CANONICAL_NAMES = {
    "plan1": "Plan 1",
    "plan 1": "Plan 1",
    "plan 1: transit warkop malang": "Plan 1",
    "plan2": "Plan 2",
    "plan 2": "Plan 2",
    "plan 2: transit dampit (pujon)": "Plan 2",
    "plan3": "Plan 3",
    "plan 3": "Plan 3",
    "plan 3: blitar sleep recovery": "Plan 3",
    "plan4": "Plan 4",
    "plan 4": "Plan 4",
    "plan 4: blitar warkop 24h": "Plan 4",
}

DESTINATION_CANONICAL_NAMES = {
    "dest_goa_tetes": "Goa Tetes",
    "goa tetes": "Goa Tetes",
    "goa tetes / teras semeru": "Goa Tetes",
    "dest_kapas_biru": "Coban Kapas Biru",
    "coban kapas biru": "Coban Kapas Biru",
    "panorama kapas biru": "Coban Kapas Biru",
    "dest_kabut_pelangi": "Kabut Pelangi",
    "kabut pelangi": "Kabut Pelangi",
    "air terjun kabut pelangi": "Kabut Pelangi",
    "coban kabut pelangi": "Kabut Pelangi",
    "dest_pantai_selatan": "Pantai Selatan Malang",
    "pantai selatan": "Pantai Selatan Malang",
    "pantai selatan malang": "Pantai Selatan Malang",
    "dest_bromo": "Bromo Sunrise",
    "bromo": "Bromo Sunrise",
    "bromo sunrise": "Bromo Sunrise",
    "dest_teras_semeru": "Teras Semeru",
    "teras semeru": "Teras Semeru",
    "teras semeru sumberurip": "Teras Semeru",
}

DEFAULT_ROUTES = ["Plan 1", "Plan 2", "Plan 3", "Plan 4"]
DEFAULT_DESTINATIONS = [
    "Goa Tetes",
    "Coban Kapas Biru",
    "Pantai Selatan Malang",
    "Bromo Sunrise",
]


def canonicalize_choice(category: str, raw_choice: str) -> str:
    """Normalize raw choice strings to clean canonical labels while preserving custom choices."""
    norm = raw_choice.strip().lower()
    if category == "route":
        return ROUTE_CANONICAL_NAMES.get(norm, raw_choice.strip())
    elif category == "destination":
        return DESTINATION_CANONICAL_NAMES.get(norm, raw_choice.strip())
    return raw_choice.strip()


class VoteDatabase:
    """Thread-safe SQLite database manager with WAL mode and atomic JSON synchronization."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH, json_path: str = DEFAULT_JSON_PATH):
        self.db_path = os.path.abspath(db_path)
        self.json_path = os.path.abspath(json_path)
        self.lock = threading.RLock()
        self._init_database()

    @contextlib.contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Create a new SQLite connection configured with WAL mode, yielding it and closing on exit."""
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        try:
            yield conn
        finally:
            conn.close()

    def _init_database(self) -> None:
        """Initialize SQLite database tables and indexes."""
        with self.lock:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS votes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        voter_name TEXT NOT NULL COLLATE NOCASE,
                        category TEXT NOT NULL,
                        choice TEXT NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(voter_name, category)
                    );
                    """
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_votes_category ON votes(category);"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_votes_choice ON votes(choice);"
                )
                conn.commit()
            self._export_json_unlocked()

    def record_vote(self, voter_name: str, category: str, choice: str) -> Dict[str, Any]:
        """Atomically record or update a vote in SQLite and sync to JSON."""
        voter_clean = voter_name.strip()
        category_clean = category.strip().lower()
        choice_clean = canonicalize_choice(category_clean, choice)

        if not voter_clean:
            raise ValueError("voter_name cannot be empty")
        if category_clean not in ("route", "destination"):
            raise ValueError("category must be 'route' or 'destination'")
        if not choice_clean:
            raise ValueError("choice cannot be empty")

        with self.lock:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO votes (voter_name, category, choice, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(voter_name, category) DO UPDATE SET
                        choice = excluded.choice,
                        updated_at = CURRENT_TIMESTAMP;
                    """,
                    (voter_clean, category_clean, choice_clean),
                )
                conn.commit()

            self._export_json_unlocked()
            return {
                "voter_name": voter_clean,
                "category": category_clean,
                "choice": choice_clean,
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }

    def get_all_votes_summary(self) -> Dict[str, Any]:
        """Fetch all votes from SQLite and calculate full aggregation tallies."""
        with self.lock:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT id, voter_name, category, choice, updated_at FROM votes ORDER BY updated_at ASC"
                )
                rows = cursor.fetchall()

            total_participants_set = set()
            participants_list = []
            routes_counts: Dict[str, int] = {k: 0 for k in DEFAULT_ROUTES}
            destinations_counts: Dict[str, int] = {k: 0 for k in DEFAULT_DESTINATIONS}
            votes_by_user: Dict[str, Dict[str, Any]] = {}
            raw_votes_list: List[Dict[str, Any]] = []

            # Detailed tallies structure
            route_voters_map: Dict[str, List[str]] = {k: [] for k in DEFAULT_ROUTES}
            dest_voters_map: Dict[str, List[str]] = {k: [] for k in DEFAULT_DESTINATIONS}

            for row in rows:
                voter = row["voter_name"]
                cat = row["category"].lower()
                ch = row["choice"]
                upd = row["updated_at"]

                raw_votes_list.append(
                    {
                        "id": row["id"],
                        "voter_name": voter,
                        "category": cat,
                        "choice": ch,
                        "choice_id": ch,
                        "updated_at": upd,
                    }
                )

                if voter not in total_participants_set:
                    total_participants_set.add(voter)
                    participants_list.append(voter)

                if voter not in votes_by_user:
                    votes_by_user[voter] = {}
                votes_by_user[voter][cat] = ch
                votes_by_user[voter]["updated_at"] = upd

                if cat == "route":
                    routes_counts[ch] = routes_counts.get(ch, 0) + 1
                    if ch not in route_voters_map:
                        route_voters_map[ch] = []
                    route_voters_map[ch].append(voter)
                elif cat == "destination":
                    destinations_counts[ch] = destinations_counts.get(ch, 0) + 1
                    if ch not in dest_voters_map:
                        dest_voters_map[ch] = []
                    dest_voters_map[ch].append(voter)

            total_route_votes = sum(routes_counts.values())
            total_dest_votes = sum(destinations_counts.values())

            # Find leaders
            route_leader = (
                max(routes_counts.items(), key=lambda x: x[1])[0]
                if routes_counts and max(routes_counts.values()) > 0
                else None
            )
            dest_leader = (
                max(destinations_counts.items(), key=lambda x: x[1])[0]
                if destinations_counts and max(destinations_counts.values()) > 0
                else None
            )

            # Detailed tallies for routes
            route_tallies = {}
            for plan, count in routes_counts.items():
                pct = round((count / total_route_votes * 100), 1) if total_route_votes > 0 else 0.0
                route_tallies[plan] = {
                    "count": count,
                    "percentage": pct,
                    "voters": route_voters_map.get(plan, []),
                    "label": plan,
                }

            # Detailed tallies for destinations
            dest_tallies = {}
            for dest, count in destinations_counts.items():
                pct = round((count / total_dest_votes * 100), 1) if total_dest_votes > 0 else 0.0
                dest_tallies[dest] = {
                    "count": count,
                    "percentage": pct,
                    "voters": dest_voters_map.get(dest, []),
                    "label": dest,
                }

            return {
                "success": True,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "total_participants": len(participants_list),
                "participants": participants_list,
                "routes": routes_counts,
                "destinations": destinations_counts,
                "votes_by_user": votes_by_user,
                "tallies": {
                    "routes": {
                        "total_votes": total_route_votes,
                        "leader": route_leader,
                        "tallies": route_tallies,
                    },
                    "destinations": {
                        "total_votes": total_dest_votes,
                        "leader": dest_leader,
                        "tallies": dest_tallies,
                    },
                },
                "raw_votes": raw_votes_list,
            }

    def reset_all_votes(self) -> None:
        """Clear all votes from SQLite and reset JSON file."""
        with self.lock:
            with self._get_connection() as conn:
                conn.execute("DELETE FROM votes;")
                conn.execute("DELETE FROM sqlite_sequence WHERE name='votes';")
                conn.commit()
            self._export_json_unlocked()

    def _export_json_unlocked(self) -> None:
        """Export state atomically to votes.json (must be called with self.lock held)."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT id, voter_name, category, choice, updated_at FROM votes ORDER BY id ASC"
                )
                rows = cursor.fetchall()

            votes_list = [
                {
                    "id": r["id"],
                    "voter_name": r["voter_name"],
                    "category": r["category"],
                    "choice": r["choice"],
                    "choice_id": r["choice"],
                    "updated_at": r["updated_at"],
                }
                for r in rows
            ]

            payload = {
                "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "total_votes": len(votes_list),
                "votes": votes_list,
            }

            temp_path = f"{self.json_path}.tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            os.replace(temp_path, self.json_path)
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to export JSON snapshot: {e}\n")


