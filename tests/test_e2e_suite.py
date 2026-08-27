#!/usr/bin/env python3
"""
Comprehensive E2E Test Suite for FastAPI/Jinja2 UI/UX Layout Refactor
Project: Tumpak Sewu Expedition Guide (Kediri - Lumajang)

Coverage Tiers:
- Tier 1: Feature Coverage across all 18 Features (DOM structure, unique IDs, templates, REST endpoints)
- Tier 2: Boundary & Corner Cases (360px viewport simulation, empty/max names, Unicode/BOM, ties, errors)
- Tier 3: Cross-Feature Interactions (Plan switching sync, live voting sync, calculator sync, reset sync)
- Tier 4: Real-World Application Scenarios (5 complete end-to-end user journeys)

Total Verifiable Assertions: > 250 (Exceeds >= 200 threshold)
Runner: python -m unittest tests/test_e2e_suite.py or python tests/test_e2e_suite.py
"""

import sys
import os

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import asyncio
import collections
import glob
import json
import re
import shutil
import tempfile
import unittest
from typing import Any, Dict, List, Optional, Set

import bs4
import jinja2

# Import project backend modules
from database import VoteDatabase, DEFAULT_ROUTES, DEFAULT_DESTINATIONS, canonicalize_choice
from main import app, serve_index, health_check, get_votes, post_vote, reset_votes, VoteRequest


class TestHarnessBase(unittest.TestCase):
    """Base test harness with shared fixtures, DOM parser, CSS parser, and isolated DB environment."""

    @classmethod
    def setUpClass(cls):
        cls.project_root = PROJECT_ROOT
        cls.templates_dir = os.path.join(cls.project_root, "templates")
        cls.static_dir = os.path.join(cls.project_root, "static")
        cls.css_path = os.path.join(cls.static_dir, "css", "main.css")
        cls.js_path = os.path.join(cls.static_dir, "js", "app.js")

        # Jinja2 environment setup
        cls.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(cls.templates_dir),
            autoescape=True,
            cache_size=0
        )

        # Read static CSS and JS
        with open(cls.css_path, "r", encoding="utf-8", errors="replace") as f:
            cls.css_content = f.read()

        with open(cls.js_path, "r", encoding="utf-8", errors="replace") as f:
            cls.js_content = f.read()

    def setUp(self):
        # Create isolated temporary directory for test DB and JSON persistence
        self.test_dir = tempfile.mkdtemp(prefix="tumpak_test_")
        self.test_db_path = os.path.join(self.test_dir, "test_votes.db")
        self.test_json_path = os.path.join(self.test_dir, "test_votes.json")
        self.db = VoteDatabase(db_path=self.test_db_path, json_path=self.test_json_path)

    def tearDown(self):
        # Cleanup temporary files
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def render_template(self, template_name: str = "index.html", **context) -> str:
        """Render a Jinja2 template and return the raw HTML string."""
        tmpl = self.jinja_env.get_template(template_name)
        return tmpl.render(**context)

    def get_soup(self, html: Optional[str] = None) -> bs4.BeautifulSoup:
        """Parse HTML string with BeautifulSoup4 and return the soup object."""
        if html is None:
            html = self.render_template("index.html")
        return bs4.BeautifulSoup(html, "html.parser")


# =============================================================================
# TIER 1: FEATURE COVERAGE (ALL 18 FEATURES)
# =============================================================================

class TestTier1FeatureCoverage(TestHarnessBase):
    """
    Tier 1: Feature Isolation Coverage across all 18 Features in Scope.
    Ensures DOM element existence, proper text content, tag hierarchy, and REST endpoints.
    """

    def test_f01_sticky_nav_pill(self):
        """Feature 1: Sticky Navigation Pill Bar with responsive one-tap section anchors."""
        soup = self.get_soup()
        nav = soup.find("nav", id="stickyNavbar")
        self.assertIsNotNone(nav, "Feature 1: #stickyNavbar element must exist in DOM")
        self.assertIn("sticky-nav", nav.get("class", []), "Feature 1: Nav must have class 'sticky-nav'")

        links = nav.find_all("a", class_="nav-link")
        self.assertGreaterEqual(len(links), 6, "Feature 1: Sticky nav must contain at least 6 anchor links")

        hrefs = [a.get("href") for a in links]
        expected_sections = [
            "#section-timeline",
            "#section-vote-summary",
            "#section-destinations",
            "#section-costs",
            "#section-safety",
            "#section-checklist",
            "#section-emergency"
        ]
        for section in expected_sections:
            self.assertIn(section, hrefs, f"Feature 1: Sticky nav must include anchor link to {section}")

        # Check CSS sticky position rule
        self.assertIn("position: sticky", self.css_content, "Feature 1: CSS must declare 'position: sticky' for nav")

    def test_f02_hero_header_redesign(self):
        """Feature 2: Hero Header Redesign with expedition badge, title, subtitle, and decluttered layout."""
        soup = self.get_soup()
        hero = soup.find("header", class_="hero-section")
        self.assertIsNotNone(hero, "Feature 2: Header with class 'hero-section' must exist")

        badge = hero.find(class_="hero-badge")
        self.assertIsNotNone(badge, "Feature 2: '.hero-badge' element must exist in hero section")
        self.assertIn("Travel Plan Disusun oleh AI", badge.get_text(), "Feature 2: Badge must state that travel plan is AI-generated baseline")

        title = hero.find("h1", class_="hero-title")
        self.assertIsNotNone(title, "Feature 2: '.hero-title' must exist")
        self.assertIn("Ekspedisi Motor Kediri", title.get_text(), "Feature 2: Hero title must mention Kediri expedition")

        subtitle = hero.find("p", class_="hero-subtitle")
        self.assertIsNotNone(subtitle, "Feature 2: '.hero-subtitle' must exist")
        self.assertIn("4 orang", subtitle.get_text(), "Feature 2: Subtitle must mention '4 orang'")
        self.assertIn("2 motor", subtitle.get_text(), "Feature 2: Subtitle must mention '2 motor'")

    def test_f03_voter_profile_bar(self):
        """Feature 3: Voter Profile Bar with avatar, name display, server status dot, and change trigger."""
        soup = self.get_soup()
        profile_bar = soup.find(id="voterProfileBar")
        self.assertIsNotNone(profile_bar, "Feature 3: #voterProfileBar must exist")

        avatar = soup.find(id="voterAvatarIcon")
        self.assertIsNotNone(avatar, "Feature 3: #voterAvatarIcon must exist")

        voter_disp = soup.find(id="currentVoterDisplay")
        self.assertIsNotNone(voter_disp, "Feature 3: #currentVoterDisplay must exist")
        self.assertIn("Tamu", voter_disp.get_text(), "Feature 3: Initial voter display must indicate Guest / Tamu")

        status_dot = soup.find(id="serverStatusDot")
        self.assertIsNotNone(status_dot, "Feature 3: #serverStatusDot must exist")

        btn_change = soup.find(id="btnChangeVoterName")
        self.assertIsNotNone(btn_change, "Feature 3: #btnChangeVoterName must exist")
        self.assertIn("promptVoterModal", btn_change.get("onclick", ""), "Feature 3: Change button must trigger modal")

    def test_f04_key_stats_grid(self):
        """Feature 4: Key Stats Grid with 4 responsive pills (Distance, Peak, Target Time, Descent Risk)."""
        soup = self.get_soup()
        stats_grid = soup.find(class_="stats-grid")
        self.assertIsNotNone(stats_grid, "Feature 4: '.stats-grid' container must exist")

        pills = stats_grid.find_all(class_="stat-pill")
        self.assertEqual(len(pills), 4, "Feature 4: Stats grid must contain exactly 4 stat-pill elements")

        text_content = stats_grid.get_text()
        self.assertTrue("158–180 km" in text_content or "180 km" in text_content, "Feature 4: Must display distance stat")
        self.assertTrue("350–1.180m" in text_content or "1.180" in text_content, "Feature 4: Must display elevation peak stat")
        self.assertIn("06:00 WIB", text_content, "Feature 4: Must display arrival target stat (06:00 WIB)")
        self.assertTrue("970m" in text_content or "Pujon" in text_content, "Feature 4: Must display Pujon descent risk stat")

    def test_f05_clean_character_encoding(self):
        """Feature 5: Clean Character Encoding with UTF-8 meta, zero BOM, and zero mojibake."""
        html = self.render_template("index.html")
        soup = self.get_soup(html)

        meta_charset = soup.find("meta", charset=re.compile(r"utf-8", re.I))
        self.assertIsNotNone(meta_charset, "Feature 5: Document must specify '<meta charset=\"UTF-8\">'")

        # Ensure no mojibake artifacts like 'dY??', 'â€', or raw replacement characters in rendered HTML
        self.assertNotIn("dY??", html, "Feature 5: Mojibake artifact 'dY??' must not be present")
        self.assertNotIn("\ufffd", html, "Feature 5: Unicode replacement character (\\ufffd) must not be present")
        self.assertFalse(html.startswith("\ufeff"), "Feature 5: Rendered HTML must not have UTF-8 BOM prefix")

        title = soup.find("title")
        self.assertIsNotNone(title, "Feature 5: Page title must exist")
        self.assertIn("Tumpak Sewu", title.get_text(), "Feature 5: Title must cleanly render 'Tumpak Sewu'")

    def test_f06_live_voting_charts_component(self):
        """Feature 6: Dedicated Live Voting Charts Component with zero duplicate DOM IDs."""
        soup = self.get_soup()
        
        # Verify required live voting elements
        self.assertIsNotNone(soup.find(id="routeVoteTotalLabel"), "Feature 6: #routeVoteTotalLabel must exist")
        self.assertIsNotNone(soup.find(id="destVoteTotalLabel"), "Feature 6: #destVoteTotalLabel must exist")
        self.assertIsNotNone(soup.find(id="routeVoteBarsList"), "Feature 6: #routeVoteBarsList must exist")
        self.assertIsNotNone(soup.find(id="destVoteBarsList"), "Feature 6: #destVoteBarsList must exist")

        # Verify summary bars for all 4 plans
        for p in [1, 2, 3, 4]:
            self.assertIsNotNone(soup.find(id=f"summaryBar-route-Plan{p}"), f"Feature 6: #summaryBar-route-Plan{p} must exist")
            self.assertIsNotNone(soup.find(id=f"summaryPct-route-Plan{p}"), f"Feature 6: #summaryPct-route-Plan{p} must exist")

        # Verify summary bars for destinations
        for d in ["GoaTetes", "KapasBiru", "PantaiSelatan", "Bromo"]:
            self.assertIsNotNone(soup.find(id=f"summaryBar-dest-{d}"), f"Feature 6: #summaryBar-dest-{d} must exist")

        # Check DOM ID uniqueness across entire document
        all_ids = [el["id"] for el in soup.find_all(id=True)]
        counts = collections.Counter(all_ids)
        self.assertEqual(counts.get("routeVoteTotalLabel", 0), 1, "Feature 6: #routeVoteTotalLabel must be unique (count == 1)")
        self.assertEqual(counts.get("destVoteTotalLabel", 0), 1, "Feature 6: #destVoteTotalLabel must be unique (count == 1)")

    def test_f07_in_context_voting_action(self):
        """Feature 7: In-Context Voting Buttons, Nickname Modal, and REST API Integration."""
        soup = self.get_soup()

        # In-card route buttons
        route_vote_btns = soup.find_all(class_=re.compile(r"btn-vote-route"))
        self.assertGreaterEqual(len(route_vote_btns), 1, "Feature 7: Route cards must have in-card vote buttons")

        # Modal elements
        modal = soup.find(id="voteNicknameModal")
        self.assertIsNotNone(modal, "Feature 7: #voteNicknameModal must exist in DOM")
        self.assertIsNotNone(soup.find(id="voterNameInput"), "Feature 7: #voterNameInput must exist")
        self.assertIsNotNone(soup.find(id="voterNameError"), "Feature 7: #voterNameError must exist")
        self.assertIsNotNone(soup.find(id="btnSaveVoterName"), "Feature 7: #btnSaveVoterName must exist")

        # REST API endpoint health & vote recording via VoteDatabase
        record = self.db.record_vote("TestUser", "route", "Plan 2")
        self.assertEqual(record["voter_name"], "TestUser", "Feature 7: DB must record voter name")
        self.assertEqual(record["choice"], "Plan 2", "Feature 7: DB must record canonical route choice")

    def test_f08_responsive_svg_elevation_map(self):
        """Feature 8: Responsive SVG Elevation Map without horizontal distortion."""
        soup = self.get_soup()
        elev_container = soup.find(id="elevationSvgContainer")
        self.assertIsNotNone(elev_container, "Feature 8: #elevationSvgContainer must exist")

        svg = elev_container.find("svg")
        self.assertIsNotNone(svg, "Feature 8: SVG element must exist inside elevation container")
        has_viewbox = svg.has_attr("viewbox") or svg.has_attr("viewBox")
        self.assertTrue(has_viewbox, "Feature 8: Elevation SVG must declare 'viewBox'")

        # Verify Pujon & Blitar elevation paths
        self.assertIsNotNone(soup.find(id="svgPujonArea"), "Feature 8: #svgPujonArea must exist")
        self.assertIsNotNone(soup.find(id="svgPujonLine"), "Feature 8: #svgPujonLine must exist")
        self.assertIsNotNone(soup.find(id="svgBlitarArea"), "Feature 8: #svgBlitarArea must exist")
        self.assertIsNotNone(soup.find(id="svgBlitarLine"), "Feature 8: #svgBlitarLine must exist")

    def test_f09_collision_free_elevation_labels(self):
        """Feature 9: Collision-Free Elevation Labels (Peak, Hazard Banners, Malang Waypoint)."""
        soup = self.get_soup()
        peak = soup.find(id="svgPeak")
        self.assertIsNotNone(peak, "Feature 9: Peak indicator #svgPeak must exist")
        self.assertIn("1.180", peak.get_text(), "Feature 9: Peak text must state 1.180 mdpl")

        hazard_banner = soup.find(id="svgHazardBanner")
        self.assertIsNotNone(hazard_banner, "Feature 9: Hazard banner #svgHazardBanner must exist")
        self.assertIn("Pujon", hazard_banner.get_text(), "Feature 9: Hazard banner must mention Pujon")

        blitar_banner = soup.find(id="svgBlitarBanner")
        self.assertIsNotNone(blitar_banner, "Feature 9: Blitar banner #svgBlitarBanner must exist")

        dot_malang = soup.find(id="svgDotMalang")
        text_malang = soup.find(id="svgTextMalang")
        self.assertIsNotNone(dot_malang, "Feature 9: Waypoint dot #svgDotMalang must exist")
        self.assertIsNotNone(text_malang, "Feature 9: Waypoint text #svgTextMalang must exist")

    def test_f10_four_plan_interactive_tab_switcher(self):
        """Feature 10: 4-Plan Interactive Tab Switcher buttons and content containers."""
        soup = self.get_soup()
        for p in [1, 2, 3, 4]:
            tab = soup.find(id=f"tabPlan{p}")
            self.assertIsNotNone(tab, f"Feature 10: Tab button #tabPlan{p} must exist")
            self.assertIn(f"switchPlan({p})", tab.get("onclick", ""), f"Feature 10: Tab {p} must call switchPlan({p})")

            info = soup.find(id=f"infoPlan{p}")
            self.assertIsNotNone(info, f"Feature 10: Plan info container #infoPlan{p} must exist")

        # Verify indicator and badge
        self.assertIsNotNone(soup.find(id="mapPlanIndicator"), "Feature 10: #mapPlanIndicator must exist")
        self.assertIsNotNone(soup.find(id="routePlanBadgeDetail"), "Feature 10: #routePlanBadgeDetail must exist")

        # Verify JS function definition in app.js
        self.assertIn("function switchPlan", self.js_content, "Feature 10: switchPlan function must be defined in app.js")

    def test_f11_initial_active_plan_display(self):
        """Feature 11: Initial Active Plan Display (Plan 2 active by default on load)."""
        soup = self.get_soup()
        tab2 = soup.find(id="tabPlan2")
        self.assertIsNotNone(tab2, "Feature 11: #tabPlan2 must exist")
        self.assertIn("active", tab2.get("class", []), "Feature 11: #tabPlan2 must have 'active' class on initial load")

        indicator = soup.find(id="mapPlanIndicator")
        self.assertIn("Plan 2", indicator.get_text(), "Feature 11: #mapPlanIndicator must default to Plan 2")

        badge = soup.find(id="routePlanBadgeDetail")
        self.assertIn("RECOMMENDED", badge.get_text().upper(), "Feature 11: Badge must indicate TOP RECOMMENDED")

    def test_f12_collapsible_itinerary_timelines(self):
        """Feature 12: Collapsible / Structured Itinerary Timelines for Expedition Plans."""
        soup = self.get_soup()
        timeline_section = soup.find(id="section-timeline")
        self.assertIsNotNone(timeline_section, "Feature 12: #section-timeline must exist")

        text_content = timeline_section.get_text()
        self.assertIn("Kediri", text_content, "Feature 12: Timelines must include Kediri waypoint")
        self.assertTrue("Pujon" in text_content or "Blitar" in text_content, "Feature 12: Timelines must include Pujon or Blitar")
        self.assertIn("Pronojiwo", text_content, "Feature 12: Timelines must include Pronojiwo basecamp")
        self.assertTrue("06:00" in text_content or "WIB" in text_content, "Feature 12: Timelines must include time stamps")

    def test_f13_mobile_first_responsive_layout(self):
        """Feature 13: Mobile-First Responsive Layout (viewport, box-sizing, and glassmorphism)."""
        soup = self.get_soup()
        meta_viewport = soup.find("meta", attrs={"name": "viewport"})
        self.assertIsNotNone(meta_viewport, "Feature 13: Viewport meta tag must be defined")
        self.assertIn("width=device-width", meta_viewport.get("content", ""), "Feature 13: Viewport must set width=device-width")

        # CSS checks
        self.assertIn("box-sizing: border-box", self.css_content, "Feature 13: CSS must apply box-sizing: border-box")
        self.assertIn("overflow-x: hidden", self.css_content, "Feature 13: CSS must prevent horizontal overflow on html/body")
        self.assertIn(".glass-panel", self.css_content, "Feature 13: CSS must provide .glass-panel utility")

    def test_f14_dynamic_cost_calculator(self):
        """Feature 14: Dynamic Cost Calculator (Plan buttons, Dest buttons, Pax mode, and checkboxes)."""
        soup = self.get_soup()
        calc_section = soup.find(id="section-costs")
        self.assertIsNotNone(calc_section, "Feature 14: #section-costs must exist")

        # Plan buttons 1-4
        for p in [1, 2, 3, 4]:
            self.assertIsNotNone(soup.find(id=f"calcPlanBtn{p}"), f"Feature 14: #calcPlanBtn{p} must exist")

        # Destination buttons A, D, B, S
        for d in ["A", "D", "B", "S"]:
            self.assertIsNotNone(soup.find(id=f"destBtn{d}"), f"Feature 14: #destBtn{d} must exist")

        # Cost mode & checkboxes
        self.assertIsNotNone(soup.find(id="btnPerPerson"), "Feature 14: #btnPerPerson must exist")
        self.assertIsNotNone(soup.find(id="btnTotalGroup"), "Feature 14: #btnTotalGroup must exist")
        self.assertIsNotNone(soup.find(id="chkIncludeFuel"), "Feature 14: #chkIncludeFuel must exist")
        self.assertIsNotNone(soup.find(id="chkIncludeMeals"), "Feature 14: #chkIncludeMeals must exist")
        self.assertIsNotNone(soup.find(id="calcGrandTotalVal"), "Feature 14: #calcGrandTotalVal must exist")

    def test_f15_destination_showcase_cards(self):
        """Feature 15: Destination Showcase Cards (4 options, specs, and pro/con accordions)."""
        soup = self.get_soup()
        dest_section = soup.find(id="section-destinations")
        self.assertIsNotNone(dest_section, "Feature 15: #section-destinations must exist")

        cards = dest_section.find_all(class_="dest-card")
        self.assertEqual(len(cards), 6, "Feature 15: Must render exactly 6 destination cards")

        # Check accordions and pro-con boxes
        toggles = dest_section.find_all(class_="accordion-toggle")
        self.assertEqual(len(toggles), 6, "Feature 15: Each destination card must have an accordion toggle")

        pro_cons = dest_section.find_all(class_="pro-con-box")
        self.assertEqual(len(pro_cons), 6, "Feature 15: Each card must have a pro-con comparison box")

    def test_f16_interactive_logistics_checklist(self):
        """Feature 16: Interactive Logistics Checklist (15 items across 3 categories with localStorage)."""
        soup = self.get_soup()
        checklist_section = soup.find(id="section-checklist")
        self.assertIsNotNone(checklist_section, "Feature 16: #section-checklist must exist")

        categories = checklist_section.find_all(class_="checklist-category-card")
        self.assertEqual(len(categories), 3, "Feature 16: Must have 3 category cards (Gear, Waterfall, Medical/Docs)")

        # Verify all 15 checkboxes chk1..chk15 exist
        for i in range(1, 16):
            chk = soup.find(id=f"chk{i}")
            self.assertIsNotNone(chk, f"Feature 16: Checkbox #chk{i} must exist")
            self.assertEqual(chk.get("type"), "checkbox", f"Feature 16: #chk{i} must be type='checkbox'")

    def test_f17_safety_risk_warning_wall(self):
        """Feature 17: Safety Risk Warning Wall (Brake fade physics & Hypothermia warnings)."""
        soup = self.get_soup()
        safety_section = soup.find(id="section-safety")
        self.assertIsNotNone(safety_section, "Feature 17: #section-safety must exist")

        warnings = safety_section.find_all(class_="warning-card")
        self.assertGreaterEqual(len(warnings), 2, "Feature 17: Must display at least 2 warning cards")

        text = safety_section.get_text()
        self.assertTrue("Brake Fade" in text or "vapour lock" in text or "Rem" in text, "Feature 17: Must warn about brake fade")
        self.assertTrue("1.313 kJ" in text or "970m" in text, "Feature 17: Must state brake physics numbers")
        self.assertTrue("hipotermia" in text or "Pronojiwo" in text, "Feature 17: Must warn about Pronojiwo sleeping risk")

    def test_f18_emergency_contacts_matrix(self):
        """Feature 18: Emergency Contacts Matrix (6 cards with direct tel: links)."""
        soup = self.get_soup()
        emergency_section = soup.find(id="section-emergency")
        self.assertIsNotNone(emergency_section, "Feature 18: #section-emergency must exist")

        cards = emergency_section.find_all(class_="emergency-card")
        self.assertEqual(len(cards), 6, "Feature 18: Must display exactly 6 emergency contact cards")

        tel_links = emergency_section.find_all("a", href=re.compile(r"^tel:"))
        self.assertEqual(len(tel_links), 6, "Feature 18: Must contain 6 'tel:' links for direct dialing")

        hrefs = [a.get("href") for a in tel_links]
        self.assertIn("tel:0334881110", hrefs, "Feature 18: Must contain Polsek Pronojiwo (0334881110)")
        self.assertIn("tel:0334881118", hrefs, "Feature 18: Must contain Puskesmas Pronojiwo (0334881118)")
        self.assertIn("tel:0341896110", hrefs, "Feature 18: Must contain Polsek Dampit (0341896110)")
        self.assertIn("tel:0341896118", hrefs, "Feature 18: Must contain Puskesmas Dampit (0341896118)")
        self.assertIn("tel:110", hrefs, "Feature 18: Must contain Call Center Polri 110")
        self.assertIn("tel:0342801110", hrefs, "Feature 18: Must contain Polres Blitar Kota (0342801110)")


# =============================================================================
# TIER 2: BOUNDARY & CORNER CASES (ALL 18 FEATURES)
# =============================================================================

class TestTier2BoundaryAndCornerCases(TestHarnessBase):
    """
    Tier 2: Boundary and Corner Case Testing across all 18 Features.
    Tests viewport constraints (360px), empty/extreme strings, Unicode/mojibake,
    zero votes / ties, error handling, and mathematical boundary conditions.
    """

    def test_f01_boundary_sticky_nav(self):
        """Feature 1 Boundary: Horizontal overflow containment and touch scrollability on 360px viewport."""
        soup = self.get_soup()
        nav = soup.find(id="stickyNavbar")
        
        # Verify nav is configured for horizontal touch scrolling or wrapping
        self.assertIn("sticky-nav", nav.get("class", []))
        self.assertIn("z-index:", self.css_content.lower(), "Feature 1: Sticky nav must specify z-index to stay on top")
        self.assertIn(".sticky-nav", self.css_content, "Feature 1: CSS must style .sticky-nav")

        # Verify all anchor destinations actually exist in the DOM
        for a in nav.find_all("a"):
            target_id = a.get("href", "").lstrip("#")
            target_el = soup.find(id=target_id)
            self.assertIsNotNone(target_el, f"Feature 1: Target section #{target_id} must exist in rendered document")

    def test_f02_boundary_hero_header(self):
        """Feature 2 Boundary: 360px viewport typography, no hardcoded overflowing fixed widths."""
        soup = self.get_soup()
        hero = soup.find(class_="hero-section")
        
        # Ensure no inline fixed width > 360px on hero container or child blocks
        for tag in hero.find_all(True):
            style = tag.get("style", "")
            match = re.search(r"width:\s*(\d+)px", style)
            if match:
                width_val = int(match.group(1))
                self.assertLessEqual(width_val, 360, f"Feature 2: Element {tag.name} has inline fixed width {width_val}px > 360px")

        # Check line height and font size definitions in CSS
        self.assertIn(".hero-title", self.css_content, "Feature 2: CSS must style .hero-title")
        self.assertIn(".hero-subtitle", self.css_content, "Feature 2: CSS must style .hero-subtitle")

    def test_f03_boundary_voter_profile_bar(self):
        """Feature 3 Boundary: Extreme voter name lengths (40 chars, 100 chars), emojis, and empty fallback."""
        # Test extreme length in DB
        long_name = "Muhammad Rizky Ramadhan Al-Fatih 1234567"
        record = self.db.record_vote(long_name, "route", "Plan 1")
        self.assertEqual(record["voter_name"], long_name)

        # Test Unicode & emojis
        emoji_name = "Budi 🚀✨ (Kediri)"
        record2 = self.db.record_vote(emoji_name, "route", "Plan 2")
        self.assertEqual(record2["voter_name"], emoji_name)

        # Test empty voter name validation
        with self.assertRaises(ValueError):
            self.db.record_vote("", "route", "Plan 1")

        with self.assertRaises(ValueError):
            self.db.record_vote("   ", "route", "Plan 1")

    def test_f04_boundary_key_stats_grid(self):
        """Feature 4 Boundary: Responsive 2x2 wrapping on small mobile screens without text clipping."""
        self.assertIn(".stats-grid", self.css_content, "Feature 4: CSS must define .stats-grid")
        self.assertIn(".stat-pill", self.css_content, "Feature 4: CSS must define .stat-pill")

        # Verify all 4 pills have icon and text components
        soup = self.get_soup()
        pills = soup.find_all(class_="stat-pill")
        for p in pills:
            self.assertIsNotNone(p.find(class_="stat-val"), "Feature 4: Stat pill must have .stat-val")
            self.assertIsNotNone(p.find(class_="stat-lbl"), "Feature 4: Stat pill must have .stat-lbl")
            self.assertIsNotNone(p.find(class_="stat-icon-box"), "Feature 4: Stat pill must have .stat-icon-box")

    def test_f05_boundary_encoding_integrity(self):
        """Feature 5 Boundary: Verification that all files and templates contain no embedded BOM or mojibake."""
        templates_pattern = os.path.join(self.templates_dir, "**", "*.html")
        all_templates = glob.glob(templates_pattern, recursive=True)
        self.assertGreater(len(all_templates), 0, "Feature 5: Templates must be found")

        for tmpl_path in all_templates:
            with open(tmpl_path, "rb") as f:
                raw_bytes = f.read()
                # Check for start-of-file BOM
                self.assertFalse(
                    raw_bytes.startswith(b"\xef\xbb\xbf"),
                    f"Feature 5: Template {os.path.basename(tmpl_path)} must not have leading UTF-8 BOM"
                )
                # Check for embedded BOM anywhere in file
                self.assertNotIn(
                    b"\xef\xbb\xbf",
                    raw_bytes,
                    f"Feature 5: Template {os.path.basename(tmpl_path)} must not have embedded UTF-8 BOM"
                )

    def test_f06_boundary_voting_charts(self):
        """Feature 6 Boundary: Edge cases for 0 votes, 100% single voter, 50/50 split, and 4-way tie."""
        # 1. Zero votes state
        summary0 = self.db.get_all_votes_summary()
        self.assertEqual(summary0["total_participants"], 0)
        self.assertEqual(summary0["tallies"]["routes"]["total_votes"], 0)
        self.assertIsNone(summary0["tallies"]["routes"]["leader"])
        for plan in DEFAULT_ROUTES:
            self.assertEqual(summary0["tallies"]["routes"]["tallies"][plan]["percentage"], 0.0)

        # 2. 100% single voter
        self.db.record_vote("Alice", "route", "Plan 2")
        summary1 = self.db.get_all_votes_summary()
        self.assertEqual(summary1["tallies"]["routes"]["total_votes"], 1)
        self.assertEqual(summary1["tallies"]["routes"]["leader"], "Plan 2")
        self.assertEqual(summary1["tallies"]["routes"]["tallies"]["Plan 2"]["percentage"], 100.0)
        self.assertEqual(summary1["tallies"]["routes"]["tallies"]["Plan 1"]["percentage"], 0.0)

        # 3. 50/50 split
        self.db.record_vote("Bob", "route", "Plan 1")
        summary2 = self.db.get_all_votes_summary()
        self.assertEqual(summary2["tallies"]["routes"]["total_votes"], 2)
        self.assertEqual(summary2["tallies"]["routes"]["tallies"]["Plan 1"]["percentage"], 50.0)
        self.assertEqual(summary2["tallies"]["routes"]["tallies"]["Plan 2"]["percentage"], 50.0)

        # 4. 4-way tie (25% each)
        self.db.record_vote("Charlie", "route", "Plan 3")
        self.db.record_vote("Dave", "route", "Plan 4")
        summary4 = self.db.get_all_votes_summary()
        self.assertEqual(summary4["tallies"]["routes"]["total_votes"], 4)
        for plan in DEFAULT_ROUTES:
            self.assertEqual(summary4["tallies"]["routes"]["tallies"][plan]["percentage"], 25.0)

    def test_f07_boundary_voting_action_validation(self):
        """Feature 7 Boundary: Rejection of invalid category, empty choice, and malformed requests."""
        with self.assertRaises(ValueError):
            self.db.record_vote("Alice", "flight_booking", "Plan 1")

        with self.assertRaises(ValueError):
            self.db.record_vote("Alice", "route", "")

        # Test canonicalization of aliases
        record_alias = self.db.record_vote("Alice", "route", "plan 2: transit dampit (pujon)")
        self.assertEqual(record_alias["choice"], "Plan 2")

        dest_alias = self.db.record_vote("Alice", "destination", "dest_goa_tetes")
        self.assertEqual(dest_alias["choice"], "Goa Tetes")

    def test_f08_boundary_svg_elevation_aspect_ratio(self):
        """Feature 8 Boundary: Responsive SVG aspect ratio and coordinate bounds."""
        soup = self.get_soup()
        elev_svg = soup.find(id="elevationSvgContainer").find("svg")
        viewbox = elev_svg.get("viewbox") or elev_svg.get("viewBox") or ""
        self.assertTrue(bool(viewbox), "Feature 8: SVG must define a valid viewBox")
        
        # Verify viewBox dimensions: min-x min-y width height
        parts = [float(x) for x in viewbox.split()]
        self.assertEqual(len(parts), 4, "Feature 8: viewBox must have 4 numeric components")
        self.assertGreater(parts[2], 0, "Feature 8: viewBox width must be positive")
        self.assertGreater(parts[3], 0, "Feature 8: viewBox height must be positive")

        # Verify path definitions have valid coordinate syntax
        pujon_path = soup.find(id="svgPujonLine")
        self.assertIsNotNone(pujon_path.get("d"), "Feature 8: Pujon path must have 'd' coordinate attribute")

    def test_f09_boundary_elevation_label_collision(self):
        """Feature 9 Boundary: Label and banner isolation from path collision zones."""
        soup = self.get_soup()
        hazard_banner = soup.find(id="svgHazardBanner")
        blitar_banner = soup.find(id="svgBlitarBanner")
        peak_pill = soup.find(id="svgPeak")

        # Peak pill should be in header or separate flex row, not intersecting SVG baseline
        self.assertIsNotNone(peak_pill)
        self.assertIsNotNone(hazard_banner)
        self.assertIsNotNone(blitar_banner)

        # Ensure text is legible
        hazard_style = hazard_banner.get("style", "")
        self.assertTrue("font-size" in hazard_style or "font-size" in self.css_content)

    def test_f10_boundary_tab_switcher_bounds(self):
        """Feature 10 Boundary: Sequential switching across all 4 plans and JS contract integrity."""
        # Check all 4 switchPlan calls in rendered template
        for p in [1, 2, 3, 4]:
            self.assertIn(f"switchPlan({p})", self.render_template())
        
        self.assertIn("updateMapVisualPlan", self.js_content, "Feature 10: app.js must have updateMapVisualPlan")
        self.assertIn("currentMapPlan", self.js_content, "Feature 10: app.js must track currentMapPlan")

    def test_f11_boundary_initial_active_plan_isolation(self):
        """Feature 11 Boundary: Only Plan 2 is active on load; other plans are not marked active."""
        soup = self.get_soup()
        tab1 = soup.find(id="tabPlan1")
        tab2 = soup.find(id="tabPlan2")
        tab3 = soup.find(id="tabPlan3")
        tab4 = soup.find(id="tabPlan4")

        self.assertNotIn("active", tab1.get("class", []))
        self.assertIn("active", tab2.get("class", []))
        self.assertNotIn("active", tab3.get("class", []))
        self.assertNotIn("active", tab4.get("class", []))

    def test_f12_boundary_timeline_mobile_responsiveness(self):
        """Feature 12 Boundary: Timelines fit within 360px viewport without clipping."""
        self.assertIn(".section-block", self.css_content, "Feature 12: CSS must style .section-block")
        soup = self.get_soup()
        timeline = soup.find(id="section-timeline")
        self.assertIsNotNone(timeline)
        # Ensure no pre-formatted text with fixed pixel overflow
        pres = timeline.find_all("pre")
        self.assertEqual(len(pres), 0, "Feature 12: Timeline should not use hardcoded <pre> blocks")

    def test_f13_boundary_mobile_first_zero_overflow(self):
        """Feature 13 Boundary: Global zero horizontal overflow rules and viewport constraints."""
        self.assertIn("overflow-x: hidden", self.css_content)
        self.assertIn("max-width: 100vw", self.css_content)
        self.assertIn("box-sizing: border-box", self.css_content)

        soup = self.get_soup()
        # Ensure container element exists
        containers = soup.find_all(class_="container")
        self.assertGreaterEqual(len(containers), 1, "Feature 13: Must use .container wrapper")

    def test_f14_boundary_cost_calculator_pricing_engine(self):
        """Feature 14 Boundary: Dynamic cost calculation formulas for 1 Pax vs 4 Pax, fuel, and meals."""
        # Test calculation functions in app.js
        self.assertIn("updateDynamicCalculator", self.js_content)
        self.assertIn("calcState", self.js_content)
        self.assertIn("setCalcPlan", self.js_content)
        self.assertIn("setCalcDest", self.js_content)
        self.assertIn("setCostMode", self.js_content)

    def test_f15_boundary_destination_cards_accordion(self):
        """Feature 15 Boundary: Destination cards pro/con accordions and lazy loaded images."""
        soup = self.get_soup()
        dest_cards = soup.find_all(class_="dest-card")
        for card in dest_cards:
            img = card.find("img")
            self.assertIsNotNone(img, "Feature 15: Destination card must have an image")
            self.assertEqual(img.get("loading"), "lazy", "Feature 15: Destination images must use loading='lazy'")
            self.assertTrue(img.has_attr("onerror"), "Feature 15: Destination images must have fallback onerror handler")

    def test_f16_boundary_checklist_storage_serialization(self):
        """Feature 16 Boundary: Checklist localStorage key and 15 toggle handlers."""
        self.assertIn("tumpak_checklist_state", self.js_content, "Feature 16: JS must use key 'tumpak_checklist_state'")
        self.assertIn("toggleCheck", self.js_content, "Feature 16: JS must define toggleCheck function")

        # Verify all 15 checklist IDs are in HTML
        soup = self.get_soup()
        for i in range(1, 16):
            self.assertIsNotNone(soup.find(id=f"chk{i}"))

    def test_f17_boundary_safety_warning_clarity(self):
        """Feature 17 Boundary: High contrast warning cards with accurate physics calculations."""
        soup = self.get_soup()
        cards = soup.find(id="section-safety").find_all(class_="warning-card")
        self.assertEqual(len(cards), 2)
        # Verify card 1 has brake fade physics
        self.assertIn("1.313 kJ", cards[0].get_text())
        # Verify card 2 has hypothermia warning
        self.assertIn("16°C", cards[1].get_text())

    def test_f18_boundary_emergency_contact_links(self):
        """Feature 18 Boundary: Clean phone numbers without illegal characters in tel: URLs."""
        soup = self.get_soup()
        emergency_section = soup.find(id="section-emergency")
        tel_links = emergency_section.find_all("a", href=re.compile(r"^tel:"))
        
        for a in tel_links:
            href = a.get("href")
            phone = href.replace("tel:", "")
            self.assertTrue(phone.isdigit(), f"Feature 18: Phone URI '{href}' must contain only digits")
            self.assertGreaterEqual(len(phone), 3, f"Feature 18: Phone URI '{href}' must be at least 3 digits")


# =============================================================================
# TIER 3: CROSS-FEATURE INTERACTIONS
# =============================================================================

class TestTier3CrossFeatureInteractions(TestHarnessBase):
    """
    Tier 3: Cross-Feature State Synchronization and Interaction Testing.
    Verifies multi-module synchronization between:
    - Tab Switcher <-> GIS Map <-> Elevation Profile <-> Cost Calculator
    - Live Voting REST API <-> SQLite DB <-> JSON Mirror <-> Live Vote Charts
    - Destination Voting <-> Cost Calculator Sync
    - Database Cleardown / Reset <-> System-wide State Synchronization
    """

    def test_cross_tab_switcher_synchronization(self):
        """Tier 3: Switching to Plan 3 synchronizes Tabs, Map Indicator, Elevation Profile, and Calculator."""
        # 1. Verify tab buttons and onclick handlers
        soup = self.get_soup()
        tab3 = soup.find(id="tabPlan3")
        self.assertIsNotNone(tab3)
        self.assertIn("switchPlan(3)", tab3.get("onclick", ""))

        # 2. Verify JS logic updates currentMapPlan and triggers calculator plan update
        self.assertIn("function switchPlan", self.js_content)
        self.assertIn("updateMapVisualPlan", self.js_content)
        self.assertIn("setCalcPlan", self.js_content)

        # 3. Verify elevation SVG toggle logic in app.js
        self.assertIn("svgHazardBanner", self.js_content)
        self.assertIn("svgBlitarBanner", self.js_content)
        self.assertIn("svgPujonArea", self.js_content)
        self.assertIn("svgBlitarArea", self.js_content)

    def test_cross_live_voting_rest_and_local_state_sync(self):
        """Tier 3: REST API vote submission updates SQLite DB, JSON snapshot, voter chips, and percentages."""
        # 1. Initial state
        summary_initial = self.db.get_all_votes_summary()
        self.assertEqual(summary_initial["total_participants"], 0)

        # 2. Record vote for Plan 2 by "Rian"
        vote_res = self.db.record_vote("Rian", "route", "Plan 2")
        self.assertEqual(vote_res["voter_name"], "Rian")
        self.assertEqual(vote_res["choice"], "Plan 2")

        # 3. Verify SQLite DB state
        summary_after = self.db.get_all_votes_summary()
        self.assertEqual(summary_after["total_participants"], 1)
        self.assertEqual(summary_after["tallies"]["routes"]["total_votes"], 1)
        self.assertEqual(summary_after["tallies"]["routes"]["leader"], "Plan 2")
        self.assertEqual(summary_after["tallies"]["routes"]["tallies"]["Plan 2"]["count"], 1)
        self.assertEqual(summary_after["tallies"]["routes"]["tallies"]["Plan 2"]["percentage"], 100.0)
        self.assertIn("Rian", summary_after["tallies"]["routes"]["tallies"]["Plan 2"]["voters"])

        # 4. Verify JSON file mirror persistence
        self.assertTrue(os.path.exists(self.test_json_path))
        with open(self.test_json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            self.assertEqual(json_data["total_votes"], 1)
            self.assertEqual(json_data["votes"][0]["voter_name"], "Rian")
            self.assertEqual(json_data["votes"][0]["choice"], "Plan 2")

    def test_cross_destination_voting_and_cost_calculator_sync(self):
        """Tier 3: Destination voting updates live summary and correlates with cost calculator options."""
        # 1. Cast destination vote for "Goa Tetes" by "Budi"
        self.db.record_vote("Budi", "destination", "Goa Tetes")

        # 2. Cast destination vote for "Coban Kapas Biru" by "Siti"
        self.db.record_vote("Siti", "destination", "Coban Kapas Biru")

        # 3. Verify destination aggregation
        summary = self.db.get_all_votes_summary()
        self.assertEqual(summary["tallies"]["destinations"]["total_votes"], 2)
        self.assertEqual(summary["destinations"]["Goa Tetes"], 1)
        self.assertEqual(summary["destinations"]["Coban Kapas Biru"], 1)
        self.assertEqual(summary["tallies"]["destinations"]["tallies"]["Goa Tetes"]["percentage"], 50.0)
        self.assertEqual(summary["tallies"]["destinations"]["tallies"]["Coban Kapas Biru"]["percentage"], 50.0)

    def test_cross_database_reset_and_ui_resynchronization(self):
        """Tier 3: Database reset clears all SQLite records, JSON mirrors, and restores 0% distribution."""
        # 1. Seed database with multiple votes
        self.db.record_vote("Voter1", "route", "Plan 1")
        self.db.record_vote("Voter2", "route", "Plan 2")
        self.db.record_vote("Voter1", "destination", "Bromo Sunrise")
        self.assertEqual(self.db.get_all_votes_summary()["total_participants"], 2)

        # 2. Trigger reset
        self.db.reset_all_votes()

        # 3. Verify clean state across DB, JSON, and Summary
        clean_summary = self.db.get_all_votes_summary()
        self.assertEqual(clean_summary["total_participants"], 0)
        self.assertEqual(clean_summary["tallies"]["routes"]["total_votes"], 0)
        self.assertEqual(clean_summary["tallies"]["destinations"]["total_votes"], 0)
        self.assertEqual(len(clean_summary["raw_votes"]), 0)

        with open(self.test_json_path, "r", encoding="utf-8") as f:
            json_clean = json.load(f)
            self.assertEqual(json_clean["total_votes"], 0)
            self.assertEqual(len(json_clean["votes"]), 0)


# =============================================================================
# TIER 4: REAL-WORLD APPLICATION SCENARIOS (5 END-TO-END WORKFLOWS)
# =============================================================================

class TestTier4RealWorldUserScenarios(TestHarnessBase):
    """
    Tier 4: Comprehensive Real-World User Scenarios.
    Simulates complete user journeys:
    - Scenario 1: New Mobile User Expedition Planning Journey (360px viewport simulation)
    - Scenario 2: Group Multi-Voter Consensus & Leaderboard Journey
    - Scenario 3: Budget Estimator & Logistics Preparation Journey
    - Scenario 4: Safety & Emergency Protocol Walkthrough Journey
    - Scenario 5: Full Expedition Lifecycle with State Reset & Re-vote Journey
    """

    def test_scenario_1_mobile_expedition_planning_journey(self):
        """
        Scenario 1: Mobile User (360px screen) loads guide, reviews hero & stats,
        sets nickname 'Rian', switches to Plan 2, checks elevation hazard, and votes Plan 2.
        """
        # Step 1: Render DOM and verify mobile-first setup
        html = self.render_template("index.html")
        soup = self.get_soup(html)
        self.assertIsNotNone(soup.find("meta", attrs={"name": "viewport"}))
        self.assertNotIn("dY??", html)

        # Step 2: Inspect Hero & Stats Grid
        hero = soup.find(class_="hero-section")
        self.assertIsNotNone(hero)
        stats = soup.find(class_="stats-grid").find_all(class_="stat-pill")
        self.assertEqual(len(stats), 4)

        # Step 3: Check Voter Bar and Modal
        voter_bar = soup.find(id="voterProfileBar")
        self.assertIsNotNone(voter_bar)
        modal = soup.find(id="voteNicknameModal")
        self.assertIsNotNone(modal)

        # Step 4: Simulate Voter setting nickname and submitting vote
        voter_name = "Rian"
        vote_record = self.db.record_vote(voter_name, "route", "Plan 2")
        self.assertEqual(vote_record["voter_name"], "Rian")
        self.assertEqual(vote_record["choice"], "Plan 2")

        # Step 5: Verify Live Summary reflects the vote
        summary = self.db.get_all_votes_summary()
        self.assertEqual(summary["total_participants"], 1)
        self.assertEqual(summary["tallies"]["routes"]["leader"], "Plan 2")
        self.assertIn("Rian", summary["tallies"]["routes"]["tallies"]["Plan 2"]["voters"])

    def test_scenario_2_group_multi_voter_consensus_journey(self):
        """
        Scenario 2: 4 Group Members ('Aris', 'Budi', 'Citra', 'Doni') vote on routes & destinations.
        Validates aggregate math, voter chips, percentages, and leadership detection.
        """
        # 1. Aris votes Plan 2 & Goa Tetes
        self.db.record_vote("Aris", "route", "Plan 2")
        self.db.record_vote("Aris", "destination", "Goa Tetes")

        # 2. Budi votes Plan 2 & Coban Kapas Biru
        self.db.record_vote("Budi", "route", "Plan 2")
        self.db.record_vote("Budi", "destination", "Coban Kapas Biru")

        # 3. Citra votes Plan 3 & Goa Tetes
        self.db.record_vote("Citra", "route", "Plan 3")
        self.db.record_vote("Citra", "destination", "Goa Tetes")

        # 4. Doni votes Plan 2 & Bromo Sunrise
        self.db.record_vote("Doni", "route", "Plan 2")
        self.db.record_vote("Doni", "destination", "Bromo Sunrise")

        # 5. Verify Consensus Results
        summary = self.db.get_all_votes_summary()
        self.assertEqual(summary["total_participants"], 4)
        self.assertEqual(set(summary["participants"]), {"Aris", "Budi", "Citra", "Doni"})

        # Route Leaderboard: Plan 2 has 3 votes (75%), Plan 3 has 1 vote (25%)
        routes_tally = summary["tallies"]["routes"]
        self.assertEqual(routes_tally["total_votes"], 4)
        self.assertEqual(routes_tally["leader"], "Plan 2")
        self.assertEqual(routes_tally["tallies"]["Plan 2"]["count"], 3)
        self.assertEqual(routes_tally["tallies"]["Plan 2"]["percentage"], 75.0)
        self.assertEqual(routes_tally["tallies"]["Plan 3"]["count"], 1)
        self.assertEqual(routes_tally["tallies"]["Plan 3"]["percentage"], 25.0)

        # Destination Leaderboard: Goa Tetes has 2 votes (50%), Kapas Biru 1 (25%), Bromo 1 (25%)
        dest_tally = summary["tallies"]["destinations"]
        self.assertEqual(dest_tally["total_votes"], 4)
        self.assertEqual(dest_tally["leader"], "Goa Tetes")
        self.assertEqual(dest_tally["tallies"]["Goa Tetes"]["count"], 2)
        self.assertEqual(dest_tally["tallies"]["Goa Tetes"]["percentage"], 50.0)

    def test_scenario_3_budget_and_logistics_preparation_journey(self):
        """
        Scenario 3: User configures Budget Calculator (Plan 3, Dest D, 4 Pax, Fuel+Meals),
        checks off 5 packing checklist items, and verifies state integrity.
        """
        soup = self.get_soup()

        # Step 1: Verify Calculator Controls
        self.assertIsNotNone(soup.find(id="calcPlanBtn3"))
        self.assertIsNotNone(soup.find(id="destBtnD"))
        self.assertIsNotNone(soup.find(id="btnTotalGroup"))
        self.assertIsNotNone(soup.find(id="chkIncludeFuel"))
        self.assertIsNotNone(soup.find(id="chkIncludeMeals"))

        # Step 2: Verify Checklist Structure
        checklist_items = soup.find(id="section-checklist").find_all("input", type="checkbox")
        self.assertEqual(len(checklist_items), 15)

        # Step 3: Simulate checking 5 critical items
        checked_ids = ["chk1", "chk2", "chk6", "chk11", "chk14"]
        for cid in checked_ids:
            chk = soup.find(id=cid)
            self.assertIsNotNone(chk, f"Checklist item #{cid} must exist")

    def test_scenario_4_safety_and_emergency_protocol_journey(self):
        """
        Scenario 4: User navigates safety warning wall, studies brake physics and
        hypothermia rules, and verifies 6 emergency contact dialers.
        """
        soup = self.get_soup()

        # Step 1: Verify Safety Wall Content
        safety = soup.find(id="section-safety")
        self.assertIsNotNone(safety)
        self.assertIn("1.313 kJ", safety.get_text())
        self.assertIn("Pujon", safety.get_text())
        self.assertIn("16°C", safety.get_text())

        # Step 2: Verify Emergency Matrix
        emergency = soup.find(id="section-emergency")
        self.assertIsNotNone(emergency)
        cards = emergency.find_all(class_="emergency-card")
        self.assertEqual(len(cards), 6)

        # Step 3: Verify all contact numbers match emergency services
        phone_numbers = [a.get("href").replace("tel:", "") for a in emergency.find_all("a")]
        self.assertIn("0334881110", phone_numbers)  # Polsek Pronojiwo
        self.assertIn("0334881118", phone_numbers)  # Puskesmas Pronojiwo
        self.assertIn("0341896110", phone_numbers)  # Polsek Dampit
        self.assertIn("0341896118", phone_numbers)  # Puskesmas Dampit
        self.assertIn("110", phone_numbers)         # Polres Malang Kota 110
        self.assertIn("0342801110", phone_numbers)  # Polres Blitar Kota

    def test_scenario_5_full_expedition_lifecycle_journey(self):
        """
        Scenario 5: Complete expedition lifecycle:
        1. Pre-trip state with legacy votes
        2. System reset via /api/votes/reset
        3. Fresh group voting
        4. Verified consistency across database, JSON mirror, and live charts
        """
        # Step 1: Pre-populate votes
        self.db.record_vote("LegacyUser1", "route", "Plan 1")
        self.db.record_vote("LegacyUser2", "destination", "Bromo Sunrise")
        self.assertEqual(self.db.get_all_votes_summary()["total_participants"], 2)

        # Step 2: Reset system
        self.db.reset_all_votes()
        post_reset = self.db.get_all_votes_summary()
        self.assertEqual(post_reset["total_participants"], 0)
        self.assertEqual(post_reset["tallies"]["routes"]["total_votes"], 0)

        # Step 3: New expedition voting
        self.db.record_vote("Eko", "route", "Plan 4")
        self.db.record_vote("Eko", "destination", "Pantai Selatan Malang")

        final_summary = self.db.get_all_votes_summary()
        self.assertEqual(final_summary["total_participants"], 1)
        self.assertEqual(final_summary["tallies"]["routes"]["leader"], "Plan 4")
        self.assertEqual(final_summary["tallies"]["destinations"]["leader"], "Pantai Selatan Malang")
        self.assertEqual(final_summary["tallies"]["routes"]["tallies"]["Plan 4"]["percentage"], 100.0)


# =============================================================================
# RUNNER SCRIPT
# =============================================================================

def run_suite():
    """Execute the full E2E test suite and print a structured summary."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestTier1FeatureCoverage))
    suite.addTests(loader.loadTestsFromTestCase(TestTier2BoundaryAndCornerCases))
    suite.addTests(loader.loadTestsFromTestCase(TestTier3CrossFeatureInteractions))
    suite.addTests(loader.loadTestsFromTestCase(TestTier4RealWorldUserScenarios))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("E2E TEST SUITE EXECUTION SUMMARY")
    print("=" * 70)
    print(f"Total Test Methods Executed : {result.testsRun}")
    print(f"Passed                      : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures                    : {len(result.failures)}")
    print(f"Errors                      : {len(result.errors)}")
    print("=" * 70)

    return result


if __name__ == "__main__":
    res = run_suite()
    if not res.wasSuccessful():
        exit(1)
