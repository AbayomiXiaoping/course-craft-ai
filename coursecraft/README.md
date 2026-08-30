# CourseCraft AI — Module Documentation

This directory contains the complete source code for **CourseCraft AI**, the intelligent course portal synthesis engine for academic management faculty.

---

## 🚀 Running CourseCraft Studio

```bash
PYTHONPATH=. uv run streamlit run coursecraft/app.py --server.port 8503
```

Access the studio at: **`http://localhost:8503`**

---

## 📂 Architecture & Package Organization

```
coursecraft/
├── app.py                      # Main Streamlit web application & studio UI
├── core/
│   ├── models.py               # Pydantic data contracts (CoursePortal, LessonPage, Flashcard, etc.)
│   └── state_manager.py        # Default MBA management course state and serialization
├── parsers/
│   ├── document_parser.py      # PDF, Word, PowerPoint, Text parsing with LaTeX math extraction
│   ├── syllabus_parser.py      # Syllabus, grading policies, and chapter-to-week extraction
│   └── slide_parser.py         # Slide deck text extraction
├── agents/
│   ├── llm_orchestrator.py     # Gemini 3.6 Flash, OpenAI, and offline heuristic synthesizers
│   ├── syllabus_architect.py   # Multi-week curriculum compiler
│   ├── lesson_synthesizer.py   # Pedagogical lesson synthesis with 3D flashcards and applied cases
│   ├── quiz_generator.py       # Multiple-choice decision quiz generator
│   ├── diagram_generator.py    # Mermaid flowchart generator with syntax sanitization
│   └── topic_scout.py          # Live web business trend scout
├── renderer/
│   └── portal_generator.py     # Server-side pre-rendered standalone HTML portal generator
└── tests/
    └── test_pipeline.py        # 7-stage end-to-end automated verification pipeline
```

---

## 🧪 Running Automated Tests

```bash
uv run python coursecraft/tests/test_pipeline.py
```

All 7 stages validate state integrity, parsers, Gemini LLM generation, flashcard rendering, and export bundling.

---

## 📚 Complete Guides

* For an in-depth step-by-step operating walkthrough, see **[`../USER_GUIDE.md`](../USER_GUIDE.md)**.
* For project overview and quick reference, see **[`../README.md`](../README.md)**.
