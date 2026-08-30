"""
app.py
CourseCraft AI — Academic Course Portal Studio.
A modern Streamlit application allowing management professors to upload course materials,
discover trending business topics from HBR/McKinsey/Mint, and synthesize full-trimester
interactive academic web portals.
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import sys
from pathlib import Path

# Ensure root workspace directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from coursecraft.core.models import (
    CoursePortal,
    CourseWeek,
    LessonPage,
    LessonBlock,
    QuizQuestion,
    QuizOption,
    SuggestedTopic,
)
from coursecraft.core.state_manager import (
    create_sample_course,
    save_course_to_file,
    load_course_from_file,
)
from coursecraft.parsers.document_parser import (
    extract_text_from_pdf,
    detect_document_type,
    extract_potential_latex,
)
from coursecraft.agents.syllabus_architect import build_course_from_ingested_materials
from coursecraft.agents.quiz_generator import generate_quizzes_from_text
from coursecraft.agents.lesson_synthesizer import synthesize_lesson_from_material
from coursecraft.agents.topic_scout import fetch_suggested_topics, convert_topic_to_lesson
from coursecraft.renderer.portal_generator import generate_portal_html
from coursecraft.renderer.exporter import create_course_zip_bundle

st.set_page_config(
    page_title="CourseCraft AI — Academic Course Portal Studio",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for Streamlit Studio
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }
    .sub-header {
        color: #475569;
        font-size: 1.02rem;
        margin-bottom: 18px;
    }
    .topic-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        border-left: 5px solid #0d3b66;
    }
    .topic-badge {
        display: inline-block;
        background: #eef4f8;
        color: #0d3b66;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .source-badge {
        display: inline-block;
        background: #fdf2f4;
        color: #a51c30;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
        margin-left: 8px;
    }
    .bangalore-callout {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 0.9rem;
        color: #166534;
        margin: 12px 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "course" not in st.session_state:
    st.session_state.course = create_sample_course()

if "ingested_texts" not in st.session_state:
    st.session_state.ingested_texts = []

if "scouted_topics" not in st.session_state:
    st.session_state.scouted_topics = fetch_suggested_topics()

if "flash_message" not in st.session_state:
    st.session_state.flash_message = None

if "selected_preview_label" not in st.session_state:
    st.session_state.selected_preview_label = "📋 Overview & Syllabus Roadmap"

course: CoursePortal = st.session_state.course

# Top App Banner
st.markdown('<div class="main-header">🏛️ CourseCraft AI — Academic Course Portal Studio</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header"><strong>Academic Course Portal Studio</strong> &bull; Tailored for MBA & BBA Management Programs &bull; Live Web Topic Scout & Case Study Synthesis</div>',
    unsafe_allow_html=True,
)

# Display persistent flash notification if available
if st.session_state.flash_message:
    st.success(st.session_state.flash_message)
    st.session_state.flash_message = None

# Sidebar: Course Metadata & Quick Switcher
with st.sidebar:
    st.header("⚙️ Course Settings")
    course.course_code = st.text_input("Course Code", value=course.course_code)
    course.course_title = st.text_input("Course Title", value=course.course_title)
    course.professor_name = st.text_input("Instructor", value=course.professor_name)
    course.university = st.text_input("Institution / Department", value=course.university)
    course.semester = st.text_input("Semester / Trimester", value=course.semester)

    theme_choice = st.selectbox(
        "Institutional Theme",
        options=["oxford_navy", "harvard_crimson", "mit_slate", "stanford_cardinal", "emerald_poly"],
        index=["oxford_navy", "harvard_crimson", "mit_slate", "stanford_cardinal", "emerald_poly"].index(course.theme_palette),
        format_func=lambda x: {
            "oxford_navy": "🏛️ Classic Oxford Navy & Gold",
            "harvard_crimson": "🍷 Harvard Crimson",
            "mit_slate": "⚙️ MIT Slate",
            "stanford_cardinal": "🌲 Stanford Cardinal",
            "emerald_poly": "🌿 Emerald Green",
        }[x],
    )
    course.theme_palette = theme_choice

    st.markdown("---")
    st.subheader("🔑 LLM Configuration")

    provider = st.radio(
        "AI Provider",
        options=["Google Gemini (Free)", "OpenAI"],
        index=0 if os.environ.get("GEMINI_API_KEY") or not os.environ.get("OPENAI_API_KEY") else 1,
        help="Google Gemini offers a 100% free tier from Google AI Studio without credit card."
    )

    if provider == "Google Gemini (Free)":
        current_gemini = os.environ.get("GEMINI_API_KEY", "")
        gemini_input = st.text_input(
            "Gemini API Key",
            value=current_gemini,
            type="password",
            placeholder="AIzaSy...",
            help="Free from https://aistudio.google.com/app/apikey"
        )
        if gemini_input:
            os.environ["GEMINI_API_KEY"] = gemini_input

        st.caption("✨ [Get a Free Gemini API Key (Google AI Studio)](https://aistudio.google.com/app/apikey)")

        if st.button("🧪 Test Gemini Connection", use_container_width=True):
            if not os.environ.get("GEMINI_API_KEY"):
                st.error("Please enter a Gemini API key first.")
            else:
                from coursecraft.agents.llm_orchestrator import call_gemini_api
                res = call_gemini_api(os.environ["GEMINI_API_KEY"], "System: reply with 1 word", "Ping", max_tokens=5)
                if res:
                    st.success(f"✅ Gemini is Connected! Model response: {res.strip()}")
                else:
                    st.error("❌ Gemini API test failed. Check key validity or connection.")
    else:
        current_openai = os.environ.get("OPENAI_API_KEY", "")
        user_api_key = st.text_input(
            "OpenAI API Key",
            value=current_openai,
            type="password",
            placeholder="sk-proj-...",
        )
        if user_api_key:
            os.environ["OPENAI_API_KEY"] = user_api_key

        chosen_model = st.selectbox(
            "OpenAI Model",
            options=["gpt-4o-mini", "gpt-4o"],
            index=0 if os.environ.get("OPENAI_MODEL") != "gpt-4o" else 1,
        )
        os.environ["OPENAI_MODEL"] = chosen_model

        if st.button("🧪 Test OpenAI Connection", use_container_width=True):
            if not os.environ.get("OPENAI_API_KEY"):
                st.error("Please enter an OpenAI API key first.")
            else:
                from coursecraft.agents.llm_orchestrator import get_openai_client
                cli, mdl = get_openai_client()
                try:
                    r = cli.chat.completions.create(model=mdl, messages=[{"role": "user", "content": "ping"}], max_tokens=5)
                    st.success(f"✅ OpenAI is Connected! Response: {r.choices[0].message.content.strip()}")
                except Exception as ex:
                    st.error(f"❌ OpenAI Error: {ex}")

    st.markdown("---")
    st.subheader("📚 Course Stats")
    col1, col2 = st.columns(2)
    col1.metric("Curriculum", f"{len(course.weeks)} Weeks")
    total_lessons = sum(len(w.lessons) for w in course.weeks)
    col2.metric("Interactive Pages", f"{total_lessons} Lessons")

    st.markdown("---")
    if st.button("🔄 Reset to Default MBA Syllabus"):
        st.session_state.course = create_sample_course()
        st.session_state.selected_preview_label = "📋 Overview & Syllabus Roadmap"
        st.session_state.flash_message = "Reset to standard MBA 602 syllabus."
        st.rerun()

# Main Tabs
tab_preview, tab_scout, tab_ingest, tab_editor, tab_copilot, tab_export = st.tabs([
    "🌐 Live Interactive Portal",
    "🔍 Web Topic Scout (HBR / McKinsey / Mint)",
    "📤 Material Ingestion & Ingest Hub",
    "📝 Curriculum & Lesson Editor",
    "🤖 AI Educational Copilot",
    "📦 Export & Publish Web Bundle",
])

# TAB 1: Live Interactive Portal Preview
with tab_preview:
    st.subheader("Interactive Course Portal Preview")
    st.caption("Rendered live with responsive navigation, KaTeX mathematical business formulas, interactive formative quizzes, and Harvard Business Review style case studies.")

    # Quick Jump Selector
    preview_options = ["📋 Overview & Syllabus Roadmap"]
    lesson_map = {}
    for w in course.weeks:
        for l_idx, l in enumerate(w.lessons):
            label = f"📅 Week {w.week_number}: {l.title}"
            preview_options.append(label)
            lesson_map[label] = (w.week_number, l_idx, l)

    default_idx = 0
    if st.session_state.selected_preview_label in preview_options:
        default_idx = preview_options.index(st.session_state.selected_preview_label)

    chosen_preview = st.selectbox(
        "👁️ Jump to Lesson / Section in Live Portal:",
        options=preview_options,
        index=default_idx,
    )
    st.session_state.selected_preview_label = chosen_preview

    init_week = None
    init_lesson = 0
    current_lesson_obj = None
    if chosen_preview != "📋 Overview & Syllabus Roadmap" and chosen_preview in lesson_map:
        init_week, init_lesson, current_lesson_obj = lesson_map[chosen_preview]

    html_code = generate_portal_html(st.session_state.course, initial_week=init_week, initial_lesson=init_lesson)
    components.html(html_code, height=800, scrolling=True)

    # Content Inspector
    if current_lesson_obj:
        with st.expander(f"📖 Inspect Raw Content & Quizzes for '{current_lesson_obj.title}'", expanded=False):
            st.markdown(f"**Estimated Read Time**: {current_lesson_obj.estimated_read_time_minutes} minutes")
            st.markdown("**Learning Objectives**:")
            for obj in current_lesson_obj.learning_objectives:
                st.markdown(f"- {obj}")
            st.markdown("---")
            st.markdown("#### Generated Lesson Blocks:")
            for b in current_lesson_obj.blocks:
                st.markdown(f"**{b.title}** ({b.block_type})")
                st.markdown(b.content_markdown)
                if b.latex_formulas:
                    for f in b.latex_formulas:
                        st.latex(f)
                st.markdown("")
            if current_lesson_obj.practice_problems:
                st.markdown("---")
                st.markdown(f"#### Formative Quizzes ({len(current_lesson_obj.practice_problems)} Questions):")
                for q_idx, q in enumerate(current_lesson_obj.practice_problems):
                    st.markdown(f"**Q{q_idx + 1}: {q.question}**")
                    for opt in q.options:
                        prefix = "✅" if opt.is_correct else "⚪"
                        st.markdown(f"- {prefix} {opt.text} *(Explanation: {opt.explanation})*")
                    if q.hint:
                        st.caption(f"💡 Hint: {q.hint}")

# TAB 2: Web Topic Scout
with tab_scout:
    st.subheader("🌐 Trending Business Topic Scout for Management Programs")
    st.write(
        "Suggests cutting-edge management topics and industry case studies from authoritative business websites "
        "(**Harvard Business Review**, **McKinsey Insights**, **MIT Sloan**, **The Economic Times**, **Livemint**). "
        "With one click, adopt any suggested topic as a complete interactive lesson module into your course."
    )

    scout_col1, scout_col2, scout_col3 = st.columns([2, 2, 1])
    with scout_col1:
        discipline_filter = st.selectbox(
            "Management Discipline",
            [
                "All Disciplines",
                "Strategy & Business Models",
                "Fintech & Digital Public Infrastructure",
                "AI & Technology Management (GCCs)",
                "Supply Chain & Quick Commerce",
                "Marketing Analytics & D2C",
                "Sustainable Finance & Operations",
            ],
        )
    with scout_col2:
        custom_topic_prompt = st.text_input(
            "Custom Focus / Keyword (Optional)",
            placeholder="e.g. UPI cross-border expansion, Tata EV battery supply chain, GCC hiring trends",
        )
    with scout_col3:
        st.write("")
        st.write("")
        if st.button("🔍 Scout Topics", type="primary"):
            with st.spinner("Analyzing business publications & synthesizing case studies..."):
                disc = None if discipline_filter == "All Disciplines" else discipline_filter
                st.session_state.scouted_topics = fetch_suggested_topics(
                    discipline=disc, custom_query=custom_topic_prompt or None
                )
                st.session_state.flash_message = f"Discovered {len(st.session_state.scouted_topics)} management topics!"
                st.rerun()

    st.markdown("---")
    st.markdown(f"#### Suggested Management Topics ({len(st.session_state.scouted_topics)})")

    for idx, topic in enumerate(st.session_state.scouted_topics):
        with st.container():
            st.markdown(
                f"""
                <div class="topic-card">
                    <span class="topic-badge">{topic.discipline}</span>
                    <span class="source-badge">📰 {topic.source_website}</span>
                    <h3 style="margin: 8px 0; color: #0f172a;">{topic.title}</h3>
                    <p style="font-size: 0.95rem; color: #334155; line-height: 1.6;">{topic.relevance_summary}</p>
                    <div class="bangalore-callout">
                        <strong>🏫 Industry & Regional Relevance:</strong><br/>
                        {topic.why_relevant_for_bangalore_students}
                    </div>
                    <div style="font-size: 0.88rem; color: #64748b; margin-bottom: 12px;">
                        <strong>💼 Case Study Focus:</strong> {topic.suggested_case_study} &bull;
                        <strong>🎯 Learning Outcome:</strong> {topic.target_learning_outcome}
                    </div>
                    <div>
                        <a href="{topic.source_url}" target="_blank" style="font-size: 0.85rem; font-weight: 600; color: #0d3b66; text-decoration: none;">
                            🔗 View Source Publication ({topic.source_website}) &rarr;
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            act_col1, act_col2 = st.columns([3, 2])
            with act_col1:
                target_options = [f"Week {w.week_number}: {w.title}" for w in course.weeks] + ["➕ Create as New Week in Syllabus"]
                chosen_target = st.selectbox(
                    f"Select Target Week for '{topic.title[:35]}...'",
                    options=target_options,
                    key=f"target_week_scout_{idx}",
                )
            with act_col2:
                st.write("")
                st.write("")
                if st.button(f"➕ Adopt Topic & Generate Lesson", key=f"adopt_btn_{idx}", type="secondary"):
                    with st.spinner(f"Generating interactive lesson module, case study, and quiz for {topic.title}..."):
                        if "New Week" in chosen_target:
                            new_w_num = len(course.weeks) + 1
                            new_lesson = convert_topic_to_lesson(topic, new_w_num)
                            new_week = CourseWeek(
                                week_number=new_w_num,
                                title=f"Week {new_w_num}: {topic.title}",
                                theme=topic.discipline,
                                dates=f"Term Week {new_w_num}",
                                overview=topic.relevance_summary,
                                lessons=[new_lesson],
                                assignments=[f"Case Analysis: {topic.suggested_case_study}"],
                                readings=[f"{topic.source_website}: {topic.title}"],
                            )
                            course.weeks.append(new_week)
                            st.session_state.course = course
                            st.session_state.selected_preview_label = f"📅 Week {new_w_num}: {new_lesson.title}"
                            st.session_state.flash_message = f"🎉 Successfully created Week {new_w_num} for '{topic.title}' with HBR Case Study and Quizzes! Switched to Live Portal preview."
                        else:
                            week_num = int(chosen_target.split(":")[0].replace("Week", "").strip())
                            target_week = next(w for w in course.weeks if w.week_number == week_num)
                            new_lesson = convert_topic_to_lesson(topic, week_num)
                            target_week.lessons.append(new_lesson)
                            st.session_state.course = course
                            st.session_state.selected_preview_label = f"📅 Week {week_num}: {new_lesson.title}"
                            st.session_state.flash_message = f"🎉 Successfully added '{topic.title}' to Week {week_num}! Switched to Live Portal preview."
                        st.rerun()

# TAB 3: Material Ingestion
with tab_ingest:
    st.subheader("Upload Academic Course Materials")
    st.write("Upload management syllabus, lecture slide decks, or HBR case study problem sets in PDF or Text format.")

    uploaded_files = st.file_uploader(
        "Upload materials (PDF, TXT, Markdown, Docx)",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.info(f"Loaded {len(uploaded_files)} file(s). Click below to trigger the AI synthesis pipeline.")
        if st.button("🚀 Analyze & Synthesize Course Portal", type="primary"):
            with st.spinner("Extracting documents, parsing business frameworks, and synthesizing curriculum..."):
                syllabus_text = ""
                slide_texts = []
                notes_texts = []

                for up_file in uploaded_files:
                    if up_file.name.lower().endswith(".pdf"):
                        raw_text = extract_text_from_pdf(up_file.read())
                    else:
                        raw_text = up_file.read().decode("utf-8", errors="ignore")

                    doc_type = detect_document_type(raw_text)
                    st.write(f"• **{up_file.name}** classified as: `{doc_type}` ({len(raw_text)} chars)")

                    if doc_type in ["syllabus", "textbook_chapter"]:
                        syllabus_text += f"\n{raw_text}"
                    elif doc_type == "slides":
                        slide_texts.append(raw_text)
                    else:
                        notes_texts.append(raw_text)

                new_course = build_course_from_ingested_materials(
                    syllabus_raw_text=syllabus_text or None,
                    slide_texts=slide_texts or None,
                    lecture_notes=notes_texts or None,
                    course_metadata={
                        "course_code": course.course_code,
                        "course_title": course.course_title,
                        "professor_name": course.professor_name,
                        "university": course.university,
                        "semester": course.semester,
                        "theme_palette": course.theme_palette,
                    },
                )
                st.session_state.course = new_course
                st.session_state.selected_preview_label = f"📅 Week 1: {new_course.weeks[0].lessons[0].title}" if new_course.weeks and new_course.weeks[0].lessons else "📋 Overview & Syllabus Roadmap"
                st.session_state.flash_message = f"🎉 Successfully analyzed {len(uploaded_files)} file(s) and synthesized {len(new_course.weeks)} weeks of curriculum!"
                st.rerun()

    st.markdown("---")
    st.markdown("#### Specialized Management Course Templates:")
    sample_col1, sample_col2, sample_col3 = st.columns(3)
    with sample_col1:
        if st.button("🏛️ Load: Strategic Management & Platforms (MBA 602)"):
            st.session_state.course = create_sample_course()
            st.session_state.selected_preview_label = "📋 Overview & Syllabus Roadmap"
            st.session_state.flash_message = "Loaded MBA 602: Strategic Management & Platform Ecosystems."
            st.rerun()
    with sample_col2:
        if st.button("💳 Load: Fintech & DPI Ecosystems (MBA 615)"):
            sample_fintech = create_sample_course()
            sample_fintech.course_code = "MBA-615"
            sample_fintech.course_title = "Fintech Architecture, Open Banking & UPI Protocols"
            sample_fintech.theme_palette = "oxford_navy"
            sample_fintech.syllabus_summary = "Exploration of India Stack, Account Aggregators, digital lending algorithms, and central bank digital currencies (e-Rupee)."
            st.session_state.course = sample_fintech
            st.session_state.selected_preview_label = "📋 Overview & Syllabus Roadmap"
            st.session_state.flash_message = "Loaded MBA 615: Fintech & Digital Public Infrastructure."
            st.rerun()
    with sample_col3:
        if st.button("🤖 Load: Enterprise AI in Bangalore GCCs (MBA 625)"):
            sample_ai = create_sample_course()
            sample_ai.course_code = "MBA-625"
            sample_ai.course_title = "Enterprise Generative AI & Corporate Digital Transformation"
            sample_ai.theme_palette = "harvard_crimson"
            sample_ai.syllabus_summary = "Strategic frameworks for AI governance, outcome-based pricing in IT services, and building Global Capability Centers (GCCs) in Bengaluru."
            st.session_state.course = sample_ai
            st.session_state.selected_preview_label = "📋 Overview & Syllabus Roadmap"
            st.session_state.flash_message = "Loaded MBA 625: Enterprise AI in Bangalore GCCs."
            st.rerun()

# TAB 4: Curriculum & Lesson Editor
with tab_editor:
    st.subheader("Curriculum Structure & Module Inspector")
    st.caption("Inspect and fine-tune your syllabus overview, weeks, case studies, and lesson blocks.")

    with st.expander("📝 Edit Course Overview & Syllabus Summary", expanded=False):
        course.syllabus_summary = st.text_area("Syllabus Summary", value=course.syllabus_summary, height=120)
        course.office_hours = st.text_input("Office Hours", value=course.office_hours or "")

    st.markdown("#### Course Weeks")
    for w_idx, week in enumerate(course.weeks):
        with st.expander(f"Week {week.week_number}: {week.title}", expanded=(w_idx == 0)):
            week.title = st.text_input(f"Week {week.week_number} Title", value=week.title, key=f"w_title_{w_idx}")
            week.overview = st.text_area(f"Week {week.week_number} Overview", value=week.overview, key=f"w_ov_{w_idx}")

            st.markdown("##### Lessons in this Week:")
            for l_idx, lesson in enumerate(week.lessons):
                st.markdown(f"**Lesson {l_idx + 1}: {lesson.title}** ({lesson.estimated_read_time_minutes} mins)")
                lesson.title = st.text_input("Lesson Title", value=lesson.title, key=f"l_title_{w_idx}_{l_idx}")

                if lesson.practice_problems:
                    st.caption(f"🧠 {len(lesson.practice_problems)} Formative Quiz Questions attached.")

    if st.button("➕ Add New Week to Syllabus"):
        new_w_num = len(course.weeks) + 1
        new_lesson = synthesize_lesson_from_material(
            f"Module {new_w_num}: Contemporary Business Strategy",
            "Core management theories, strategic trade-offs, and empirical business performance in Bangalore.",
        )
        new_week = CourseWeek(
            week_number=new_w_num,
            title=f"Week {new_w_num}: Contemporary Strategic Issues",
            theme=f"Theme {new_w_num}",
            overview=f"Contemporary management dilemmas for week {new_w_num}.",
            lessons=[new_lesson],
        )
        course.weeks.append(new_week)
        st.session_state.course = course
        st.session_state.selected_preview_label = f"📅 Week {new_w_num}: {new_lesson.title}"
        st.session_state.flash_message = f"Added Week {new_w_num} to syllabus!"
        st.rerun()

# TAB 5: AI Copilot
with tab_copilot:
    st.subheader("Professor's AI Teaching Assistant")
    st.write("Use AI to augment your management courseware: add HBR-style case dilemmas, formulate quantitative business metrics, or generate executive quizzes.")

    target_week = st.selectbox(
        "Target Week",
        options=[f"Week {w.week_number}: {w.title}" for w in course.weeks],
    )
    target_week_num = int(target_week.split(":")[0].replace("Week", "").strip())
    selected_week = next(w for w in course.weeks if w.week_number == target_week_num)

    copilot_action = st.radio(
        "What would you like the AI to generate?",
        [
            "🧠 Generate Formative Business Decision Quizzes (with hints & step-by-step solutions)",
            "📊 Generate Mermaid.js Strategic Value Chain / Process Flow Diagram",
            "📐 Add Managerial Economics Formulas (LTV:CAC, Contribution Margin, WACC)",
            "💼 Add Executive Case Study Dilemma (Indian Corporate Context)",
        ],
    )

    custom_instructions = st.text_input("Additional Instructions / Focus Area (Optional)", placeholder="e.g. Focus on quick commerce dark store density or UPI transaction volume")

    if st.button("✨ Apply AI Generation", type="primary"):
        with st.spinner("AI Synthesizer at work..."):
            if "Quizzes" in copilot_action:
                topic = f"{selected_week.title} {custom_instructions}"
                new_quizzes = generate_quizzes_from_text(topic, selected_week.overview, count=2)
                if selected_week.lessons:
                    selected_week.lessons[0].practice_problems.extend(new_quizzes)
                    st.session_state.flash_message = f"Added {len(new_quizzes)} new interactive quizzes to {selected_week.lessons[0].title}!"
            elif "Diagram" in copilot_action:
                from coursecraft.agents.diagram_generator import generate_mermaid_diagram
                diagram = generate_mermaid_diagram(selected_week.title, custom_instructions or selected_week.overview)
                if selected_week.lessons:
                    selected_week.lessons[0].blocks.append(
                        LessonBlock(
                            title="Strategic Value Chain Diagram",
                            block_type="diagram",
                            content_markdown="Auto-generated architectural state flow:",
                            mermaid_diagram=diagram,
                        )
                    )
                    st.session_state.flash_message = f"New Mermaid strategic diagram added to {selected_week.title}!"
            elif "Mathematical" in copilot_action or "Managerial" in copilot_action:
                if selected_week.lessons:
                    selected_week.lessons[0].blocks.append(
                        LessonBlock(
                            title="Quantitative Decision Formulation",
                            block_type="proof_math",
                            content_markdown="Analytical invariant formulation for corporate valuation:",
                            latex_formulas=[
                                r"\text{WACC} = \left(\frac{E}{V} \times Re\right) + \left(\frac{D}{V} \times Rd \times (1 - T_c)\right)",
                                r"\text{Economic Value Added (EVA)} = \text{NOPAT} - (\text{WACC} \times \text{Invested Capital})",
                            ],
                        )
                    )
                    st.session_state.flash_message = f"Managerial economic formulas added to {selected_week.title}!"
            elif "Case Study" in copilot_action:
                if selected_week.lessons:
                    selected_week.lessons[0].blocks.append(
                        LessonBlock(
                            title="Executive Case Dilemma: Indian Market Disruption",
                            block_type="case_study",
                            case_company="Bengaluru Tech Ecosystem",
                            content_markdown=(
                                f"**Executive Dilemma**: In evaluating {selected_week.title}, executive leadership must navigate "
                                f"regulatory compliance, local market rivalry, and customer retention. "
                                f"{custom_instructions or 'Analyze how platform governance and capital allocation resolve this trade-off.'}"
                            ),
                        )
                    )
                    st.session_state.flash_message = f"Executive case dilemma added to {selected_week.title}!"

            st.session_state.course = course
            if selected_week.lessons:
                st.session_state.selected_preview_label = f"📅 Week {selected_week.week_number}: {selected_week.lessons[0].title}"
            st.rerun()

# TAB 6: Export & Publishing
with tab_export:
    st.subheader("📦 Export Production Course Website")
    st.write(
        "Export your course portal as a self-contained web bundle ready for hosting on **GitHub Pages**, "
        "**Netlify**, **Vercel**, or embedding as an iframe inside your **University LMS (Canvas / Moodle)**."
    )

    zip_bytes = create_course_zip_bundle(course)
    html_bundle = generate_portal_html(course)

    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.download_button(
            label="📥 Download Complete Course Website (.ZIP)",
            data=zip_bytes,
            file_name=f"{course.course_code}_course_portal.zip",
            mime="application/zip",
            help="Contains index.html, course_manifest.json, and deployment instructions.",
        )
    with col_exp2:
        st.download_button(
            label="📄 Download Standalone 'index.html'",
            data=html_bundle,
            file_name=f"{course.course_code}_index.html",
            mime="text/html",
            help="Single-file self-contained web page with zero dependencies.",
        )

    st.markdown("---")
    st.markdown("#### How to Publish for Students:")
    st.markdown(
        """
        1. **University LMS (Canvas/Moodle)**: Upload `index.html` to your Course Files or embed it directly:
           ```html
           <iframe src="https://your-university.edu/courses/mba602/index.html" width="100%" height="800px" style="border:none;"></iframe>
           ```
        2. **GitHub Pages / Netlify**: Unzip the bundle, push `index.html` to your GitHub repo, and publish for instant student access.
        3. **Offline Student Sharing**: Share `index.html` directly with students — it runs in Chrome/Edge/Safari without needing any server or internet!
        """
    )
