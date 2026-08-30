"""
syllabus_architect.py
Assembles full multi-week course portals from ingested documents.
Maps syllabi, slides, and lecture notes into a unified curriculum tree.
"""

import re
import json
from typing import List, Dict, Any, Optional
from coursecraft.core.models import CoursePortal, CourseWeek
from coursecraft.parsers.syllabus_parser import parse_syllabus_text
from coursecraft.parsers.slide_parser import parse_slides
from coursecraft.agents.lesson_synthesizer import synthesize_lesson_from_material
from coursecraft.agents.llm_orchestrator import generate_structured_synthesis


def build_course_from_ingested_materials(
    syllabus_raw_text: Optional[str] = None,
    slide_texts: Optional[List[str]] = None,
    lecture_notes: Optional[List[str]] = None,
    course_metadata: Optional[Dict[str, str]] = None,
) -> CoursePortal:
    """Builds a full multi-week CoursePortal from all provided materials."""
    meta = course_metadata or {}
    course = CoursePortal(
        course_code=meta.get("course_code", "MBA-602"),
        course_title=meta.get("course_title", "Strategic Management & Digital Business Models"),
        university=meta.get("university", "Department of Management Studies, School of Business"),
        professor_name=meta.get("professor_name", "Prof. Rajesh Sharma, Ph.D."),
        semester=meta.get("semester", "Trimester III / Academic Year 2026-27"),
        theme_palette=meta.get("theme_palette", "oxford_navy"),
    )

    parsed_weeks = []

    # 1. AI-Powered Curriculum Architecture with Gemini
    if syllabus_raw_text and len(syllabus_raw_text.strip()) > 100:
        system_prompt = (
            "You are an Academic Dean & Curriculum Architect for a university graduate MBA program. "
            "Examine the uploaded textbook or syllabus text and design a coherent 4-to-8 week MBA course curriculum. "
            "CRITICAL: Completely ignore bibliographies, video citations, copyright pages, table of contents clutter, and publisher boilerplate. "
            "Return a valid JSON object with: 'course_code', 'course_title', 'professor_name', "
            "'weeks' (an array of 4-8 objects each with 'week_number', 'title', 'theme', 'overview')."
        )
        user_prompt = f"Uploaded Material Sample:\n{syllabus_raw_text[:3500]}\n\nSynthesize an authentic MBA curriculum schedule."
        ai_resp = generate_structured_synthesis(system_prompt, user_prompt, max_tokens=1800)
        if ai_resp:
            try:
                ai_data = json.loads(ai_resp)
                if ai_data.get("course_code") and ai_data["course_code"] != "CS-101":
                    course.course_code = ai_data["course_code"]
                if ai_data.get("course_title"):
                    course.course_title = ai_data["course_title"]
                if ai_data.get("professor_name") and "instructor" not in ai_data["professor_name"].lower():
                    course.professor_name = ai_data["professor_name"]
                if ai_data.get("weeks") and len(ai_data["weeks"]) >= 3:
                    parsed_weeks = [
                        {
                            "week_number": idx + 1,
                            "title": f"Week {idx + 1}: {re.sub(r'^(?:Week|Module)\s*\d+\s*[-:]?\s*', '', w.get('title', '')).strip()}",
                            "theme": w.get("theme") or re.sub(r'^(?:Week|Module)\s*\d+\s*[-:]?\s*', '', w.get('title', '')).strip(),
                            "overview": w.get("overview", f"Curriculum module {idx + 1}."),
                        }
                        for idx, w in enumerate(ai_data["weeks"][:8])
                    ]
            except Exception:
                pass

    # 2. Heuristic Parser fallback if AI synthesis wasn't available
    if not parsed_weeks and syllabus_raw_text:
        syl = parse_syllabus_text(syllabus_raw_text)
        if syl.get("course_code") and syl["course_code"] != "CS-101":
            course.course_code = syl["course_code"]
        if syl.get("course_title") and syl["course_title"] != "Academic Course":
            course.course_title = syl["course_title"]
        if syl.get("professor_name") and syl["professor_name"] != "Instructor":
            course.professor_name = syl["professor_name"]
        if syl.get("grading_policy"):
            course.grading_policy = syl["grading_policy"]
        parsed_weeks = syl.get("weeks", [])

    # 3. Default Management Schedule if no materials parsed
    if not parsed_weeks:
        default_topics = [
            ("Platform Ecosystems & Cross-Side Network Effects", "Analysis of two-sided marketplaces, Swiggy/Zomato competitive dynamics, and contribution margins"),
            ("India's Digital Public Infrastructure & Fintech Models", "UPI, ONDC, Account Aggregators, and digital lending risk spreads in Bengaluru"),
            ("Enterprise Generative AI & Bangalore GCC Strategy", "Transformation of Indian IT consulting, Infosys/TCS AI foundry, and GCC governance"),
            ("Quick Commerce, Dark Stores & Hyper-local Supply Chains", "Unit economics, delivery density, and last-mile logistics optimization"),
        ]
        parsed_weeks = [
            {
                "week_number": idx + 1,
                "title": f"Week {idx + 1}: {title}",
                "theme": title,
                "overview": overview,
            }
            for idx, (title, overview) in enumerate(default_topics)
        ]

    # 4. Build weeks and synthesize lessons
    all_slide_text = "\n".join(slide_texts) if slide_texts else ""
    all_notes = "\n".join(lecture_notes) if lecture_notes else ""
    all_syl = syllabus_raw_text or ""
    combined_content = f"{all_syl}\n{all_slide_text}\n{all_notes}".strip()

    weeks: List[CourseWeek] = []
    for w_info in parsed_weeks:
        w_num = w_info["week_number"]
        w_title = w_info["title"]
        w_overview = w_info["overview"]
        
        # Derive a clean theme (never emit "Core Module 20")
        raw_theme = w_info.get("theme", "")
        if not raw_theme or "core module" in raw_theme.lower():
            clean_theme = re.sub(r"^Week\s*\d+\s*[-:]?\s*", "", w_title).strip()
            theme_name = clean_theme if clean_theme else f"Module {w_num}"
        else:
            theme_name = raw_theme

        lesson_content = combined_content if len(combined_content) > 50 else w_overview
        lesson = synthesize_lesson_from_material(
            lesson_title=f"{w_title} — Core Concepts & Analysis",
            raw_content=lesson_content,
        )

        week = CourseWeek(
            week_number=w_num,
            title=w_title,
            theme=theme_name,
            dates=f"Week {w_num} of Semester",
            overview=w_overview,
            lessons=[lesson],
            assignments=[f"Problem Set {w_num}: In-depth analytical exercises and implementation."],
            readings=[f"Selected chapter readings & lecture companion notes for Week {w_num}."],
        )
        weeks.append(week)

    course.weeks = weeks
    return course
