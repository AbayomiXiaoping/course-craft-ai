"""
test_pipeline.py
Automated end-to-end verification for CourseCraft AI.
Tests model integrity, topic scout, parser extraction, portal compilation, and ZIP bundling.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from coursecraft.core.models import CoursePortal, CourseWeek, LessonPage
from coursecraft.core.state_manager import create_sample_course
from coursecraft.parsers.syllabus_parser import parse_syllabus_text
from coursecraft.parsers.document_parser import detect_document_type, extract_potential_latex
from coursecraft.agents.quiz_generator import generate_quizzes_from_text
from coursecraft.agents.lesson_synthesizer import synthesize_lesson_from_material
from coursecraft.agents.syllabus_architect import build_course_from_ingested_materials
from coursecraft.agents.topic_scout import fetch_suggested_topics, convert_topic_to_lesson
from coursecraft.renderer.portal_generator import generate_portal_html
from coursecraft.renderer.exporter import create_course_zip_bundle


def run_all_tests():
    print("🚀 [1/7] Testing Course Model & State Manager...")
    course = create_sample_course()
    assert course.course_code == "MBA-602"
    assert "Management Studies" in course.university
    assert len(course.weeks) >= 2
    assert len(course.weeks[0].lessons) >= 1
    assert len(course.weeks[0].lessons[0].practice_problems) >= 1
    print("  ✅ MBA course portal state generated & validated.")

    print("🌐 [2/7] Testing Web Topic Scout & External Case Studies...")
    topics = fetch_suggested_topics()
    assert len(topics) >= 3
    assert any("Quick Commerce" in t.title or "Digital Public" in t.title for t in topics)
    sample_topic = topics[0]
    converted_lesson = convert_topic_to_lesson(sample_topic, week_num=3)
    assert converted_lesson.title is not None
    assert len(converted_lesson.blocks) >= 3
    assert len(converted_lesson.practice_problems) >= 1
    print("  ✅ Web Topic Scout successfully retrieved topics and converted to interactive lesson.")

    print("📄 [3/7] Testing Syllabus & Document Parsing...")
    dummy_syllabus = """
    MBA 615: Fintech & Digital Banking
    Professor Rajesh Sharma
    Grading Policy:
    Case Study Projects: 40%
    Trimester Exam: 60%

    Week 1: Foundations of Open Banking & UPI
    Week 2: Account Aggregators and MSME Credit
    """
    parsed = parse_syllabus_text(dummy_syllabus)
    assert parsed["course_code"] == "MBA-615"
    assert "Rajesh Sharma" in parsed["professor_name"]
    assert len(parsed["weeks"]) == 2
    assert detect_document_type(dummy_syllabus) == "syllabus"
    print("  ✅ Parsers successfully extracted metadata and weeks.")

    print("🧠 [4/7] Testing Quiz & Lesson Synthesis...")
    quiz = generate_quizzes_from_text("Fintech Strategy", "DPI unbundles discovery, payments, and fulfillment.")
    assert len(quiz) >= 1
    assert quiz[0].options[0].text is not None

    lesson = synthesize_lesson_from_material("Platform Economics", "Network effects drive platform defensibility.")
    assert len(lesson.blocks) >= 3
    assert lesson.blocks[1].block_type == "proof_math"
    print("  ✅ Educational synthesizers constructed pedagogical lesson blocks.")

    print("🏛️ [5/7] Testing Multi-Week Synthesis Engine...")
    assembled = build_course_from_ingested_materials(
        syllabus_raw_text=dummy_syllabus,
        course_metadata={"course_code": "MBA-615", "course_title": "Fintech & Digital Banking"},
    )
    assert assembled.course_code == "MBA-615"
    assert len(assembled.weeks) == 2
    print("  ✅ Syllabus architect successfully compiled curriculum tree.")

    print("🎨 [6/7] Testing HTML Portal Compilation with Case Studies...")
    html = generate_portal_html(assembled)
    assert "<!DOCTYPE html>" in html
    assert "KaTeX" in html or "katex" in html
    assert "mermaid" in html
    assert "MBA-615" in html
    print("  ✅ Standalone HTML portal successfully generated with KaTeX, Mermaid & case studies.")

    print("📦 [7/7] Testing Exporter & ZIP Bundling...")
    zip_bytes = create_course_zip_bundle(assembled)
    assert len(zip_bytes) > 1000
    print("  ✅ ZIP archive successfully created.")

    print("\n🎉 ALL 7 VERIFICATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_all_tests()
