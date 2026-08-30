"""
portal_generator.py
Compiles a CoursePortal data model into a high-fidelity, interactive, responsive HTML5/CSS3/JS web application.
Includes KaTeX math formulas, Mermaid.js diagrams, interactive formative quizzes with scoring,
dark/light mode switcher, and academic themes.

USES PRE-RENDERED STATIC HTML (SSR) for guaranteed instant visibility in any browser,
IDE preview, or offline context without relying on client-side innerHTML rendering.
"""

import json
import re
from typing import Optional
from coursecraft.core.models import CoursePortal, CourseWeek, LessonPage, LessonBlock


THEME_COLORS = {
    "oxford_navy": {
        "primary": "#0d3b66",
        "primary_hover": "#092847",
        "accent": "#f4d35e",
        "badge": "#eef4f8",
        "badge_text": "#0d3b66",
    },
    "harvard_crimson": {
        "primary": "#a51c30",
        "primary_hover": "#7c1524",
        "accent": "#f29c38",
        "badge": "#fdf2f4",
        "badge_text": "#a51c30",
    },
    "mit_slate": {
        "primary": "#3a3d40",
        "primary_hover": "#202224",
        "accent": "#d9534f",
        "badge": "#f0f2f5",
        "badge_text": "#3a3d40",
    },
    "stanford_cardinal": {
        "primary": "#8c1515",
        "primary_hover": "#651010",
        "accent": "#e98300",
        "badge": "#fbf2f2",
        "badge_text": "#8c1515",
    },
    "emerald_poly": {
        "primary": "#1b4931",
        "primary_hover": "#113020",
        "accent": "#d4af37",
        "badge": "#eef8f3",
        "badge_text": "#1b4931",
    },
}


def format_markdown(text: str) -> str:
    """Pre-renders Markdown into clean, accessible HTML."""
    if not text:
        return ""
    # Bold
    res = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    res = re.sub(r"\*(.*?)\*", r"<em>\1</em>", res)
    # Markdown links
    res = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2" target="_blank" style="color:var(--primary);font-weight:600;text-decoration:underline;">\1</a>',
        res,
    )
    # Paragraphs
    paragraphs = [p.strip().replace("\n", "<br>") for p in res.split("\n\n") if p.strip()]
    return "".join(f'<p class="block-p">{p}</p>' for p in paragraphs)


def generate_portal_html(
    course: CoursePortal,
    initial_week: Optional[int] = None,
    initial_lesson: int = 0,
) -> str:
    """Generates a complete, pre-rendered, standalone HTML/CSS/JS course web portal."""
    theme = THEME_COLORS.get(course.theme_palette, THEME_COLORS["oxford_navy"])

    # Determine default active view
    default_active_view = "view-syllabus"
    default_active_nav = "btn-syllabus"
    if initial_week is not None:
        default_active_view = f"view-lesson-{initial_week}-{initial_lesson}"
        default_active_nav = f"nav-lesson-{initial_week}-{initial_lesson}"

    # Pre-render Sidebar Navigation Links
    sidebar_nav_html = []
    for week in course.weeks:
        week_group = [
            f"""
            <div class="week-nav-group">
              <button class="nav-btn week-header-btn" onclick="switchView('view-lesson-{week.week_number}-0', 'nav-lesson-{week.week_number}-0')">
                <span>📅</span> Week {week.week_number}: {week.theme or week.title}
              </button>
            """
        ]
        for l_idx, lesson in enumerate(week.lessons):
            clean_title = re.sub(r"^Lecture \d+:\s*", "", lesson.title)
            is_active = (initial_week == week.week_number and initial_lesson == l_idx)
            active_cls = " active" if is_active else ""
            week_group.append(
                f"""
                <button class="nav-btn lesson-sublink{active_cls}" id="nav-lesson-{week.week_number}-{l_idx}"
                  onclick="switchView('view-lesson-{week.week_number}-{l_idx}', 'nav-lesson-{week.week_number}-{l_idx}')">
                  <span>📖</span> {clean_title}
                </button>
                """
            )
        week_group.append("</div>")
        sidebar_nav_html.append("".join(week_group))

    sidebar_weeks_markup = "".join(sidebar_nav_html)

    # Pre-render Syllabus View Section
    grading_items = "".join(
        f'<li style="margin-bottom: 8px;"><strong>{k}:</strong> {v}</li>'
        for k, v in course.grading_policy.items()
    )
    prereq_pills = "".join(
        f'<span class="meta-pill">✓ {p}</span>'
        for p in course.prerequisites
    )
    schedule_rows = "".join(
        f"""
        <tr style="border-bottom: 1px solid var(--border); cursor: pointer;"
            onclick="switchView('view-lesson-{w.week_number}-0', 'nav-lesson-{w.week_number}-0')">
          <td style="padding: 12px 14px; font-weight: 600;">Week {w.week_number}</td>
          <td style="padding: 12px 14px; color: var(--text-muted);">{w.dates or 'Scheduled'}</td>
          <td style="padding: 12px 14px; font-weight: 500;">{w.title}</td>
          <td style="padding: 12px 14px; color: var(--primary); font-weight: 600;">{w.assignments[0] if w.assignments else 'Classroom Case Study'}</td>
        </tr>
        """
        for w in course.weeks
    )

    is_syl_active = (default_active_view == "view-syllabus")
    syl_active_cls = " active" if is_syl_active else ""
    syl_btn_cls = " active" if is_syl_active else ""

    syllabus_section_html = f"""
    <section id="view-syllabus" class="page-view{syl_active_cls}">
      <div class="hero-card">
        <div class="course-badge">{course.course_code}</div>
        <h1 class="hero-h1">{course.course_title}</h1>
        <div class="meta-pills">
          <span class="meta-pill">👤 {course.professor_name}</span>
          <span class="meta-pill">🏛️ {course.university}</span>
          <span class="meta-pill">🗓️ {course.semester}</span>
          <span class="meta-pill">🕒 {course.office_hours or 'By Appointment'}</span>
        </div>
        <p class="block-p" style="font-size: 1.1rem; line-height: 1.75; margin-top: 14px;">{course.syllabus_summary}</p>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 28px;">
        <div class="content-card">
          <h2 class="block-h2">Grading Policy & Evaluation</h2>
          <ul style="padding-left: 20px; font-size: 0.95rem; line-height: 1.8; margin-top: 10px;">
            {grading_items}
          </ul>
        </div>
        <div class="content-card">
          <h2 class="block-h2">Course Prerequisites</h2>
          <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;">
            {prereq_pills}
          </div>
        </div>
      </div>

      <div class="content-card">
        <h2 class="block-h2">Semester Schedule Roadmap</h2>
        <table style="width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 0.95rem;">
          <thead>
            <tr style="border-bottom: 2px solid var(--border); text-align: left;">
              <th style="padding: 10px 14px;">Week</th>
              <th style="padding: 10px 14px;">Dates</th>
              <th style="padding: 10px 14px;">Theme & Module Topics</th>
              <th style="padding: 10px 14px;">Deliverables & Case Study</th>
            </tr>
          </thead>
          <tbody>
            {schedule_rows}
          </tbody>
        </table>
      </div>
    </section>
    """

    # Pre-render Lesson Sections
    lesson_sections_html = []
    for week in course.weeks:
        for l_idx, lesson in enumerate(week.lessons):
            view_id = f"view-lesson-{week.week_number}-{l_idx}"
            is_view_active = (default_active_view == view_id)
            view_active_cls = " active" if is_view_active else ""

            # Learning objectives
            objs_html = "".join(f"<li>{obj}</li>" for obj in lesson.learning_objectives)

            # Blocks
            blocks_markup = []
            for b in lesson.blocks:
                case_tag = ""
                if b.block_type == "case_study":
                    case_tag = '<div style="display:inline-block; background:#fef3c7; color:#92400e; font-size:0.75rem; font-weight:700; padding:4px 10px; border-radius:6px; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.04em;">💼 Executive Case Analysis</div>'

                extra_content = []
                if b.latex_formulas:
                    for f in b.latex_formulas:
                        extra_content.append(f'<div class="math-callout">$${f}$$</div>')
                if b.mermaid_diagram:
                    extra_content.append(f'<div class="mermaid" style="margin: 20px 0; background: var(--bg); padding: 16px; border-radius: 8px;">{b.mermaid_diagram}</div>')
                if b.code_snippet:
                    safe_code = b.code_snippet.replace("<", "&lt;").replace(">", "&gt;")
                    extra_content.append(f'<pre><code class="language-{b.code_language or "text"}">{safe_code}</code></pre>')

                extra_markup = "".join(extra_content)
                rendered_markdown = format_markdown(b.content_markdown)

                example_markup = ""
                if b.applied_example:
                    rendered_example = format_markdown(b.applied_example)
                    example_markup = f"""
                    <div class="applied-example-box">
                      <div class="applied-example-badge">💡 Applied Business Example</div>
                      {rendered_example}
                    </div>
                    """

                blocks_markup.append(
                    f"""
                    <div class="content-card">
                      {case_tag}
                      <h2 class="block-h2">{b.title}</h2>
                      {rendered_markdown}
                      {example_markup}
                      {extra_markup}
                    </div>
                    """
                )

            blocks_html_str = "".join(blocks_markup)

            # Interactive Flashcard Deck
            flashcards_html = ""
            if lesson.flashcards:
                cards_markup = []
                for fc_idx, fc in enumerate(lesson.flashcards):
                    disp_style = "display: block;" if fc_idx == 0 else "display: none;"
                    cards_markup.append(
                        f"""
                        <div class="flashcard-slide" id="fc-{view_id}-{fc_idx}" style="{disp_style}">
                          <div class="flashcard-scene">
                            <div class="flashcard-inner" onclick="this.classList.toggle('is-flipped')">
                              <div class="flashcard-face flashcard-front">
                                <span class="flashcard-category">{fc.category or 'Core Concept'}</span>
                                <div class="flashcard-front-text">{fc.front}</div>
                                <div class="flashcard-hint-text">👆 Click card to flip</div>
                              </div>
                              <div class="flashcard-face flashcard-back">
                                <span class="flashcard-category">{fc.category or 'Core Concept'}</span>
                                <div class="flashcard-back-text">{fc.back}</div>
                                <div class="flashcard-hint-text">🔄 Click to flip back to front</div>
                              </div>
                            </div>
                          </div>
                        </div>
                        """
                    )
                all_cards = "".join(cards_markup)
                flashcards_html = f"""
                <div class="flashcards-container">
                  <div class="flashcards-header">
                    <div style="display:flex; align-items:center; gap:10px;">
                      <span style="font-size:1.4rem;">🗂️</span>
                      <div>
                        <h2 class="block-h2" style="margin:0; border:none; font-size:1.2rem;">Interactive Concept Flashcards</h2>
                        <div style="font-size:0.8rem; color:var(--text-muted);">Master strategic definitions, metrics, and core frameworks with active recall.</div>
                      </div>
                    </div>
                    <div class="fc-counter" id="fc-counter-{view_id}">Card 1 of {len(lesson.flashcards)}</div>
                  </div>
                  <div class="flashcard-deck-viewport">
                    {all_cards}
                  </div>
                  <div class="flashcard-controls">
                    <button class="fc-btn" onclick="prevCard('{view_id}', {len(lesson.flashcards)})">◀ Previous</button>
                    <button class="fc-btn fc-btn-flip" onclick="flipActiveCard('{view_id}')">Flip Card 🔄</button>
                    <button class="fc-btn" onclick="nextCard('{view_id}', {len(lesson.flashcards)})">Next ▶</button>
                  </div>
                </div>
                """

            # Further Readings
            readings_html = ""
            if lesson.further_readings:
                items = "".join(
                    f"""
                    <li style="margin-bottom: 8px;">
                      <a href="{r.url or '#'}" target="_blank" style="color: var(--primary); font-weight:600; text-decoration:underline;">🔗 {r.title}</a>
                      {f'<span style="font-size:0.8rem; color:var(--text-muted);"> ({r.source_name})</span>' if r.source_name else ''}
                      {f'<p style="margin:2px 0 0 0; color:var(--text-muted); font-size:0.85rem;">{r.description}</p>' if r.description else ''}
                    </li>
                    """
                    for r in lesson.further_readings
                )
                readings_html = f"""
                <div class="content-card" style="border-left: 4px solid var(--accent); margin-top: 24px;">
                  <h2 class="block-h2" style="border:none;">📚 Industry Readings & Case References</h2>
                  <ul style="padding-left: 20px; font-size: 0.92rem; line-height: 1.8;">
                    {items}
                  </ul>
                </div>
                """

            # Quizzes
            quiz_html = ""
            if lesson.practice_problems:
                q_cards = []
                for q_idx, q in enumerate(lesson.practice_problems):
                    opts = "".join(
                        f"""
                        <div class="quiz-option" onclick="handleQuizSelect(this, {str(opt.is_correct).lower()}, '{opt.explanation.replace("'", "\\'")}', {q.points})">
                          <span class="quiz-indicator">⚪</span>
                          <span>{opt.text}</span>
                        </div>
                        """
                        for opt in q.options
                    )
                    hint_box = f'<div class="quiz-hint-box">💡 <strong>Hint:</strong> {q.hint}</div>' if q.hint else ""
                    sol_box = ""
                    if q.step_by_step_solution:
                        sol_box = f"""
                        <button class="solution-btn" onclick="this.nextElementSibling.classList.toggle('visible')">Show Step-by-Step Derivation</button>
                        <div class="solution-drawer">{q.step_by_step_solution}</div>
                        """

                    q_cards.append(
                        f"""
                        <div class="quiz-question-card" id="q-card-{q.id}">
                          <div class="quiz-q-title">{q_idx + 1}. {q.question}</div>
                          <div class="quiz-options">{opts}</div>
                          <div class="quiz-feedback"></div>
                          {hint_box}
                          {sol_box}
                        </div>
                        """
                    )

                all_q_cards = "".join(q_cards)
                quiz_html = f"""
                <div class="quiz-container">
                  <div class="quiz-title-bar">
                    <div>
                      <h2 class="block-h2" style="margin: 0; border: none;">🧠 Formative Decision-Making Check</h2>
                      <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Test your grasp of the strategic concepts and unit economics above.</div>
                    </div>
                    <div class="score-badge" id="score-badge-{view_id}">Score: 0 pts</div>
                  </div>
                  {all_q_cards}
                </div>
                """

            lesson_sections_html.append(
                f"""
                <section id="{view_id}" class="page-view{view_active_cls}">
                  <div class="hero-card" style="padding: 24px 32px;">
                    <div class="meta-pills">
                      <span class="meta-pill">Week {week.week_number}</span>
                      <span class="meta-pill">⏱️ {lesson.estimated_read_time_minutes} min reading</span>
                    </div>
                    <h1 class="hero-h1" style="font-size: 1.8rem; margin-bottom: 16px;">{lesson.title}</h1>
                    <div style="background: var(--badge-bg); padding: 14px 18px; border-radius: 8px;">
                      <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--badge-text); margin-bottom: 6px;">Learning Objectives</div>
                      <ul style="padding-left: 20px; font-size: 0.92rem; line-height: 1.6;">
                        {objs_html}
                      </ul>
                    </div>
                  </div>
                  {blocks_html_str}
                  {flashcards_html}
                  {readings_html}
                  {quiz_html}
                </section>
                """
            )

    all_lesson_sections_markup = "".join(lesson_sections_html)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{course.course_code}: {course.course_title}</title>
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <!-- KaTeX for Mathematics -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{
      delimiters: [
        {{left: '$$', right: '$$', display: true}},
        {{left: '$', right: '$', display: false}}
      ],
      throwOnError: false
    }});"></script>
  <!-- Mermaid for Diagrams -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", function() {{
      if (window.mermaid) {{
        mermaid.initialize({{
          startOnLoad: false,
          theme: 'neutral',
          securityLevel: 'loose'
        }});
        const activeView = document.querySelector('.page-view.active');
        if (activeView) {{
          safeRenderMermaid(activeView);
        }}
      }}
    }});
  </script>

  <style>
    :root {{
      --primary: {theme['primary']};
      --primary-hover: {theme['primary_hover']};
      --accent: {theme['accent']};
      --badge-bg: {theme['badge']};
      --badge-text: {theme['badge_text']};
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --sidebar-bg: #ffffff;
      --text: #1e293b;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --radius: 12px;
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.07), 0 2px 4px -2px rgb(0 0 0 / 0.05);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.08), 0 4px 6px -4px rgb(0 0 0 / 0.04);
    }}

    [data-theme="dark"] {{
      --bg: #0f172a;
      --card-bg: #1e293b;
      --sidebar-bg: #111827;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --border: #334155;
      --badge-bg: #334155;
      --badge-text: #e2e8f0;
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.3);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background-color: var(--bg);
      color: var(--text);
      display: flex;
      height: 100vh;
      overflow: hidden;
      transition: background-color 0.25s ease, color 0.25s ease;
    }}

    /* Sidebar Navigation */
    #sidebar {{
      width: 320px;
      min-width: 320px;
      background: var(--sidebar-bg);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow-y: auto;
      box-shadow: var(--shadow);
    }}

    .sidebar-header {{
      padding: 24px;
      border-bottom: 1px solid var(--border);
      background: linear-gradient(135deg, var(--primary), var(--primary-hover));
      color: #ffffff;
    }}

    .course-badge {{
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      background: rgba(255, 255, 255, 0.2);
      padding: 4px 10px;
      border-radius: 9999px;
      margin-bottom: 8px;
    }}

    .course-title-sidebar {{
      font-size: 1.15rem;
      font-weight: 700;
      line-height: 1.35;
      margin-bottom: 6px;
    }}

    .prof-name-sidebar {{
      font-size: 0.85rem;
      opacity: 0.9;
    }}

    .sidebar-menu {{
      padding: 16px;
      flex: 1;
      overflow-y: auto;
    }}

    .nav-section-title {{
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
      margin: 16px 8px 8px 8px;
    }}

    .nav-btn {{
      display: flex;
      align-items: center;
      gap: 10px;
      width: 100%;
      padding: 10px 14px;
      border-radius: 8px;
      border: none;
      background: transparent;
      color: var(--text);
      font-size: 0.9rem;
      font-weight: 500;
      text-align: left;
      cursor: pointer;
      transition: all 0.15s ease;
      margin-bottom: 4px;
    }}

    .nav-btn:hover {{
      background: var(--border);
    }}

    .nav-btn.active {{
      background: var(--badge-bg);
      color: var(--badge-text);
      font-weight: 600;
    }}

    .week-nav-group {{
      margin-bottom: 8px;
    }}

    .week-header-btn {{
      font-weight: 600;
      font-size: 0.85rem;
      color: var(--text);
      padding: 8px 12px;
      background: rgba(0,0,0,0.02);
      border-radius: 6px;
    }}

    .lesson-sublink {{
      font-size: 0.82rem;
      padding-left: 28px;
      color: var(--text-muted);
    }}

    .lesson-sublink.active {{
      color: var(--primary);
      font-weight: 600;
    }}

    /* Main Content Area */
    #main-content {{
      flex: 1;
      height: 100vh;
      overflow-y: auto;
      padding: 32px 48px 80px 48px;
    }}

    .top-controls {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }}

    .theme-toggle-btn {{
      padding: 8px 14px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--card-bg);
      color: var(--text);
      cursor: pointer;
      font-size: 0.85rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* Page View Visibility (Pre-rendered Pages) */
    .page-view {{
      display: none;
    }}
    .page-view.active {{
      display: block;
      animation: fadeIn 0.2s ease-in-out;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Cards & Typography */
    .hero-card {{
      background: var(--card-bg);
      border-radius: var(--radius);
      padding: 32px;
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      margin-bottom: 28px;
    }}

    .hero-h1 {{
      font-family: 'Newsreader', serif;
      font-size: 2.2rem;
      font-weight: 600;
      color: var(--primary);
      margin-bottom: 12px;
    }}

    .meta-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 14px 0 20px 0;
    }}

    .meta-pill {{
      display: inline-flex;
      align-items: center;
      padding: 4px 12px;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 600;
      background: var(--badge-bg);
      color: var(--badge-text);
    }}

    .content-card {{
      background: var(--card-bg);
      border-radius: var(--radius);
      padding: 28px;
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      margin-bottom: 24px;
    }}

    .block-h2 {{
      font-family: 'Newsreader', serif;
      font-size: 1.45rem;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 14px;
      border-bottom: 2px solid var(--badge-bg);
      padding-bottom: 6px;
    }}

    .block-p {{
      font-size: 1rem;
      line-height: 1.7;
      color: var(--text);
      margin-bottom: 16px;
    }}

    .math-callout {{
      background: rgba(13, 59, 102, 0.04);
      border-left: 4px solid var(--primary);
      border-radius: 0 8px 8px 0;
      padding: 18px 24px;
      margin: 16px 0;
      font-size: 1.1rem;
      overflow-x: auto;
    }}

    pre code {{
      display: block;
      padding: 16px;
      background: #1e293b;
      color: #f8fafc;
      border-radius: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      line-height: 1.5;
      overflow-x: auto;
      margin: 16px 0;
    }}

    /* Formative Quiz Interactive Widget */
    .quiz-container {{
      margin-top: 32px;
      border-top: 2px dashed var(--border);
      padding-top: 28px;
    }}

    .quiz-title-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}

    .score-badge {{
      font-weight: 700;
      font-size: 0.85rem;
      background: var(--primary);
      color: white;
      padding: 6px 14px;
      border-radius: 9999px;
    }}

    .quiz-question-card {{
      background: rgba(0,0,0,0.015);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px;
      margin-bottom: 20px;
    }}

    .quiz-q-title {{
      font-weight: 600;
      font-size: 1.05rem;
      margin-bottom: 14px;
    }}

    .quiz-option {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 16px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--card-bg);
      margin-bottom: 8px;
      cursor: pointer;
      font-size: 0.95rem;
      transition: all 0.15s ease;
    }}

    .quiz-option:hover {{
      border-color: var(--primary);
      background: rgba(13, 59, 102, 0.02);
    }}

    .quiz-option.correct {{
      border-color: #10b981 !important;
      background: #ecfdf5 !important;
      color: #065f46 !important;
      font-weight: 600;
    }}

    .quiz-option.incorrect {{
      border-color: #ef4444 !important;
      background: #fef2f2 !important;
      color: #991b1b !important;
    }}

    .quiz-feedback {{
      margin-top: 10px;
      padding: 10px 14px;
      border-radius: 6px;
      font-size: 0.85rem;
      display: none;
    }}

    .quiz-hint-box {{
      margin-top: 10px;
      font-size: 0.85rem;
      color: var(--text-muted);
      font-style: italic;
    }}

    .solution-btn {{
      margin-top: 12px;
      background: transparent;
      border: 1px dashed var(--primary);
      color: var(--primary);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
    }}

    .solution-drawer {{
      margin-top: 10px;
      padding: 12px;
      background: var(--badge-bg);
      border-radius: 6px;
      font-size: 0.85rem;
      white-space: pre-line;
      display: none;
    }}

    .solution-drawer.visible {{
      display: block;
    }}

    /* Applied Business Example Callout */
    .applied-example-box {{
      background: linear-gradient(135deg, rgba(13, 59, 102, 0.04), rgba(244, 211, 94, 0.08));
      border-left: 4px solid var(--accent);
      border-radius: 0 10px 10px 0;
      padding: 18px 22px;
      margin: 18px 0 12px 0;
      border-top: 1px solid rgba(0,0,0,0.04);
      border-right: 1px solid rgba(0,0,0,0.04);
      border-bottom: 1px solid rgba(0,0,0,0.04);
    }}

    .applied-example-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--accent);
      color: #78350f;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 6px;
      margin-bottom: 10px;
    }}

    /* Interactive Flashcard Deck */
    .flashcards-container {{
      margin: 32px 0;
      padding: 26px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }}

    .flashcards-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }}

    .fc-counter {{
      font-weight: 700;
      font-size: 0.85rem;
      background: var(--badge-bg);
      color: var(--badge-text);
      padding: 4px 12px;
      border-radius: 9999px;
    }}

    .flashcard-scene {{
      perspective: 1000px;
      width: 100%;
      max-width: 680px;
      height: 250px;
      margin: 0 auto;
    }}

    .flashcard-inner {{
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
      transform-style: preserve-3d;
      cursor: pointer;
      border-radius: 16px;
      box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.09);
    }}

    .flashcard-inner.is-flipped {{
      transform: rotateY(180deg);
    }}

    .flashcard-face {{
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 16px;
      padding: 32px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border: 2px solid var(--border);
    }}

    .flashcard-front {{
      background: linear-gradient(135deg, var(--card-bg), var(--badge-bg));
      color: var(--text);
    }}

    .flashcard-back {{
      background: linear-gradient(135deg, var(--primary), var(--primary-hover));
      color: #ffffff;
      transform: rotateY(180deg);
    }}

    .flashcard-category {{
      position: absolute;
      top: 18px;
      left: 20px;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 3px 10px;
      border-radius: 9999px;
      background: rgba(0,0,0,0.06);
    }}

    .flashcard-back .flashcard-category {{
      background: rgba(255,255,255,0.2);
      color: #ffffff;
    }}

    .flashcard-front-text {{
      font-family: 'Newsreader', serif;
      font-size: 1.35rem;
      font-weight: 600;
      color: var(--primary);
      line-height: 1.4;
      max-width: 90%;
    }}

    .flashcard-back-text {{
      font-size: 1.02rem;
      line-height: 1.6;
      font-weight: 400;
      max-width: 92%;
    }}

    .flashcard-hint-text {{
      position: absolute;
      bottom: 14px;
      font-size: 0.75rem;
      opacity: 0.7;
    }}

    .flashcard-controls {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 14px;
      margin-top: 20px;
    }}

    .fc-btn {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .fc-btn:hover {{
      background: var(--badge-bg);
      border-color: var(--primary);
      color: var(--primary);
    }}

    .fc-btn-flip {{
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
    }}

    .fc-btn-flip:hover {{
      background: var(--primary-hover);
      color: #ffffff;
    }}
  </style>
</head>
<body>
  <!-- Sidebar -->
  <aside id="sidebar">
    <div class="sidebar-header">
      <div class="course-badge">{course.course_code}</div>
      <h1 class="course-title-sidebar">{course.course_title}</h1>
      <div class="prof-name-sidebar">{course.professor_name}</div>
    </div>
    <div class="sidebar-menu">
      <div class="nav-section-title">Course Information</div>
      <button class="nav-btn{syl_btn_cls}" id="btn-syllabus" onclick="switchView('view-syllabus', 'btn-syllabus')">
        <span>📋</span> Overview & Syllabus
      </button>

      <div class="nav-section-title">Curriculum Weeks</div>
      <div id="weeks-navigation">
        {sidebar_weeks_markup}
      </div>
    </div>
  </aside>

  <!-- Main Content -->
  <main id="main-content">
    <div class="top-controls">
      <div style="font-size: 0.9rem; color: var(--text-muted);">
        <strong>{course.university}</strong> &bull; {course.semester}
      </div>
      <button class="theme-toggle-btn" onclick="toggleTheme()">
        <span id="theme-icon">🌙</span> <span id="theme-label">Dark Mode</span>
      </button>
    </div>

    <!-- Pre-rendered Views -->
    <div id="viewport">
      {syllabus_section_html}
      {all_lesson_sections_markup}
    </div>
  </main>

  <script>
    let globalScores = {{}};

    function switchView(viewId, navId) {{
      // Hide all views
      document.querySelectorAll('.page-view').forEach(function(el) {{
        el.classList.remove('active');
      }});
      // Deactivate all nav buttons
      document.querySelectorAll('.nav-btn').forEach(function(btn) {{
        btn.classList.remove('active');
      }});

      // Show target view
      const target = document.getElementById(viewId);
      if (target) {{
        target.classList.add('active');
      }}

      // Activate target nav
      if (navId) {{
        const navBtn = document.getElementById(navId);
        if (navBtn) navBtn.classList.add('active');
      }}

      // Rerun KaTeX math on the newly revealed section if available
      if (window.renderMathInElement && target) {{
        try {{
          renderMathInElement(target, {{
            delimiters: [
              {{left: '$$', right: '$$', display: true}},
              {{left: '$', right: '$', display: false}}
            ],
            throwOnError: false
          }});
        }} catch(e) {{}}
      }}

      // Safe render Mermaid on the newly revealed section
      safeRenderMermaid(target);

      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    async function safeRenderMermaid(container) {{
      if (!window.mermaid || !container) return;
      const nodes = container.querySelectorAll('.mermaid:not([data-processed="true"])');
      for (let i = 0; i < nodes.length; i++) {{
        const node = nodes[i];
        const rawCode = node.textContent.trim();
        try {{
          const id = 'mermaid-svg-' + Math.random().toString(36).substring(2, 9);
          const res = await mermaid.render(id, rawCode);
          node.innerHTML = res.svg;
          node.setAttribute('data-processed', 'true');
        }} catch (err) {{
          console.warn("Mermaid parsing notice:", err);
          node.style.background = 'rgba(13, 59, 102, 0.03)';
          node.style.border = '1px solid var(--border)';
          node.style.borderRadius = '8px';
          node.style.padding = '18px';
          node.innerHTML = `
            <div style="font-weight:700; color:var(--primary); margin-bottom:8px; display:flex; align-items:center; gap:6px;">
              <span>📊</span> Strategic Concept Workflow
            </div>
            <pre style="background:transparent; color:var(--text); padding:0; margin:0; font-family:'JetBrains Mono',monospace; font-size:0.85rem; white-space:pre-wrap;">${{rawCode}}</pre>
          `;
          node.setAttribute('data-processed', 'true');
        }}
      }}
    }}

    function toggleTheme() {{
      const current = document.documentElement.getAttribute('data-theme');
      if (current === 'dark') {{
        document.documentElement.removeAttribute('data-theme');
        document.getElementById('theme-icon').textContent = '🌙';
        document.getElementById('theme-label').textContent = 'Dark Mode';
      }} else {{
        document.documentElement.setAttribute('data-theme', 'dark');
        document.getElementById('theme-icon').textContent = '☀️';
        document.getElementById('theme-label').textContent = 'Light Mode';
      }}
    }}

    function handleQuizSelect(optEl, isCorrect, explanation, points) {{
      const card = optEl.closest('.quiz-question-card');
      const allOpts = card.querySelectorAll('.quiz-option');
      const feedbackBox = card.querySelector('.quiz-feedback');
      const scoreBadge = card.closest('.quiz-container').querySelector('.score-badge');

      // Lock options
      allOpts.forEach(function(el) {{
        el.onclick = null;
      }});

      if (isCorrect) {{
        optEl.classList.add('correct');
        optEl.querySelector('.quiz-indicator').textContent = '✅';
        feedbackBox.style.display = 'block';
        feedbackBox.style.background = '#ecfdf5';
        feedbackBox.style.color = '#065f46';
        feedbackBox.innerHTML = '<strong>Correct!</strong> ' + explanation;

        const containerId = card.closest('.page-view').id;
        if (!globalScores[containerId]) globalScores[containerId] = 0;
        globalScores[containerId] += points;
        if (scoreBadge) {{
          scoreBadge.textContent = 'Score: ' + globalScores[containerId] + ' pts';
        }}
      }} else {{
        optEl.classList.add('incorrect');
        optEl.querySelector('.quiz-indicator').textContent = '❌';
        feedbackBox.style.display = 'block';
        feedbackBox.style.background = '#fef2f2';
        feedbackBox.style.color = '#991b1b';
        feedbackBox.innerHTML = '<strong>Not quite.</strong> ' + explanation;
      }}
    }}

    let currentCardIndices = {{}};

    function updateCardDisplay(deckId, total) {{
      const idx = currentCardIndices[deckId] || 0;
      const counter = document.getElementById('fc-counter-' + deckId);
      if (counter) {{
        counter.textContent = 'Card ' + (idx + 1) + ' of ' + total;
      }}
      for (let i = 0; i < total; i++) {{
        const slide = document.getElementById('fc-' + deckId + '-' + i);
        if (slide) {{
          slide.style.display = (i === idx) ? 'block' : 'none';
          const inner = slide.querySelector('.flashcard-inner');
          if (inner) inner.classList.remove('is-flipped');
        }}
      }}
    }}

    function nextCard(deckId, total) {{
      if (!currentCardIndices[deckId]) currentCardIndices[deckId] = 0;
      currentCardIndices[deckId] = (currentCardIndices[deckId] + 1) % total;
      updateCardDisplay(deckId, total);
    }}

    function prevCard(deckId, total) {{
      if (!currentCardIndices[deckId]) currentCardIndices[deckId] = 0;
      currentCardIndices[deckId] = (currentCardIndices[deckId] - 1 + total) % total;
      updateCardDisplay(deckId, total);
    }}

    function flipActiveCard(deckId) {{
      const idx = currentCardIndices[deckId] || 0;
      const slide = document.getElementById('fc-' + deckId + '-' + idx);
      if (slide) {{
        const inner = slide.querySelector('.flashcard-inner');
        if (inner) inner.classList.toggle('is-flipped');
      }}
    }}
  </script>
</body>
</html>"""
