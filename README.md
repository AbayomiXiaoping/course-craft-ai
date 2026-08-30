# 🏛️ CourseCraft AI — Management Course Portal Studio

> **Transforming Academic Materials & Field Case Studies into Interactive Course Web Portals**  
> *Engineered for Graduate Business Schools & Management Faculty (MBA & BBA Programs)*

---

## 📖 What is CourseCraft AI?

**CourseCraft AI** is an intelligent pairing assistant and course synthesizer for university professors. It ingests raw teaching materials—such as **textbook PDFs, syllabi, lecture slides, and notes**—and compiles them into a **fully interactive, zero-dependency HTML course portal**.

Students can access complete multi-week curriculums, interactive 3D concept flashcards, applied corporate case studies, KaTeX mathematical models, Mermaid strategy diagrams, and formative decision quizzes—all running locally or hosted online with **zero client-side installation**.

---

## ⚡ Quick Start (In Under 1 Minute)

### 1. Prerequisites
- Python 3.10+ installed
- Recommended runner: `uv` (or `pip`)

### 2. Launch the Studio
Run the following command from the repository root:

```bash
PYTHONPATH=. uv run streamlit run coursecraft/app.py --server.port 8503
```

Open your browser and navigate to:
👉 **`http://localhost:8503`**

---

## 🔑 LLM Configuration & API Key Options

CourseCraft AI features a **multi-provider LLM orchestrator** with automatic fallbacks:

```
┌────────────────────────────────────────────────────────┐
│               Multi-Provider LLM Engine                │
├──────────────────────────┬─────────────────────────────┤
│ 1. Google Gemini (Free)  │ Google AI Studio            │
│ 2. OpenAI                │ GPT-4o-mini / GPT-4o        │
│ 3. Heuristic Synthesizer │ Built-in Offline Fallback   │
└──────────────────────────┴─────────────────────────────┘
```

### Option 1: Google Gemini Free API (Recommended)
Google provides a **100% free tier** with generous limits (15 requests/min and 1,000,000 tokens/min) and **no credit card required**:
1. Get a free API key at **[Google AI Studio](https://aistudio.google.com/app/apikey)** (takes 30 seconds).
2. Add it to your environment or `~/.zshrc`:
   ```bash
   export GEMINI_API_KEY="AIzaSy..."
   ```
   *(Or paste it into the **Gemini API Key** field in the studio sidebar).*
3. Click the **"🧪 Test Gemini Connection"** button in the sidebar to verify.

### Option 2: OpenAI
If you prefer OpenAI, export your key or paste it in the sidebar:
```bash
export OPENAI_API_KEY="sk-proj-..."
```

### Option 3: Offline Mode (Zero API Keys)
If no API key is provided (or if credit quotas are exhausted), CourseCraft automatically engages its **Pedagogical Heuristic Synthesizer**. It parses textbook chapters, computes quantitative metrics, creates strategy diagrams, and builds case quizzes completely offline without errors.

---

## 🛠️ Step-by-Step Operating Guide

CourseCraft Studio is organized into an institutional sidebar and **5 functional tabs**:

### 📍 Sidebar: Course Metadata & AI Settings
1. **Course Code & Title**: Configure your course identifier (e.g. `MBA-602`, `HRM-501`) and subject name.
2. **Faculty Details**: Set the instructor name and department (*Department of Management Studies*).
3. **Institutional Theme**: Choose from 5 curated academic palettes:
   - 🏛️ **Classic Oxford Navy & Gold** (Default)
   - 🍷 **Harvard Crimson**
   - ⚙️ **MIT Slate**
   - 🌲 **Stanford Cardinal**
   - 🌿 **Emerald Poly**
4. **AI Connection**: Switch between Gemini and OpenAI, enter keys, and test connectivity.

---

### 🗂️ Tab 1: Course Roadmap & Week Navigator
* **Inspect Weeks**: Expand each semester week to view learning themes, lecture titles, objectives, and content blocks.
* **Review Content Blocks**: See how conceptual foundations, applied examples, formulas, diagrams, and quizzes are structured.
* **Add Custom Weeks**: Click **"➕ Add New Curriculum Week"** to introduce additional modules.

---

### 🌐 Tab 2: Web Topic Scout & Trend Discovery
* **Discipline Filters**: Select disciplines such as *Strategic Management*, *Platform Economics*, *Fintech*, *Supply Chain*, or *Human Resource Management*.
* **Scout Trending Topics**: CourseCraft searches leading sources (Harvard Business Review, McKinsey Insights, MIT Sloan, The Economic Times) for current business issues.
* **1-Click Adoption**: Click **"➕ Adopt into Course Curriculum"** on any topic card. CourseCraft will automatically synthesize a complete interactive lesson—with Bangalore market context, formulas, diagrams, case analysis, and flashcards—and append it to your course!

---

### 📤 Tab 3: Material Ingestion & Ingest Hub
* **Upload Academic Files**: Supports `.pdf` (textbooks, research papers, syllabi), `.docx`, `.pptx` (slide presentations), and `.txt` / `.md`.
* **Paste Direct Text**: Paste reading excerpts, syllabi, or chapter outlines directly into the text box.
* **Click "🚀 Analyze & Synthesize Multi-Week Course Portal"**:
  - Automatically strips PDF cover pages, ISBNs, copyright notices, and Pressbooks boilerplate.
  - Excludes video citations and bibliography endnotes (e.g. *"Brotherhood of Sleeping Car Porters"*) from becoming fake modules.
  - Distinguishes between currency dollar signs (`$100,000`) and LaTeX mathematical equations.
  - Generates a clean 4-to-8 week university curriculum with authentic academic titles.

---

### 👁️ Tab 4: Interactive Live HTML Portal Preview
* **Live In-App Rendering**: Preview your portal directly inside Streamlit before publishing.
* **View Selector**: Switch between the **Overview & Syllabus Roadmap** and individual lectures.
* **Interactive Testing**: Click to flip 3D concept flashcards, test multiple-choice quizzes, inspect Mermaid diagrams, and toggle Dark Mode.

---

### 📦 Tab 5: Production Export & Packaging
* **Option A: Download Standalone HTML (`portal.html`)**:
  - Single self-contained file with all CSS, pre-rendered DOM, KaTeX, and Mermaid scripts included.
  - Students can double-click and open it in any browser offline. No server required.
  - Easily uploaded to Canvas, Moodle, Blackboard, or Google Classroom.
* **Option B: Download Complete Bundle (`course_portal_bundle.zip`)**:
  - Full deployment package ready for hosting on GitHub Pages, Netlify, Vercel, or institutional servers.
* **Option C: Export Course Blueprint (`course_data.json`)**:
  - Portable JSON backup of your entire course state for version control in Git.

---

## 🎨 Interactive Features in Student Portals

| Feature | Description | Student Experience |
|---|---|---|
| 🗂️ **3D Concept Flashcards** | Active recall deck at the end of each lesson | Click card or "Flip Card 🔄" for 3D rotation. Navigate with Previous / Next buttons. |
| 💡 **Applied Business Examples** | Real-world Indian & global corporate case callouts | Amber-accented cards showing how concepts apply at Swiggy, Blinkit, Razorpay, Infosys. |
| 📐 **KaTeX Mathematical Models** | High-visibility analytical equation callout blocks | Renders formulas for Contribution Margin II, LTV:CAC, Employee Turnover, and HCROI. |
| 📊 **Mermaid Architecture Diagrams** | Visual flowcharts and value chain diagrams | Pre-rendered SVG charts illustrating multi-sided platforms, logistics routing, and workflows. |
| 🧠 **Formative Decision Quizzes** | Scenario-based multiple choice assessments | Instant color-coded feedback (✅/❌), score tracking, hints, and step-by-step solutions. |
| 🌓 **Light / Dark Mode Toggle** | Adaptive reading theme switcher | Students can toggle between daylight reading and dark mode for comfortable night study. |

---

## 🧪 Automated Testing

CourseCraft includes a comprehensive 7-stage verification test suite:

```bash
uv run python coursecraft/tests/test_pipeline.py
```

### Verification Pipeline:
1. `[1/7]` Course Model & State Manager
2. `[2/7]` Web Topic Scout & Case Study Integration
3. `[3/7]` Syllabus & Document Parsing
4. `[4/7]` Quiz & Lesson Synthesis (with Flashcards)
5. `[5/7]` Multi-Week Curriculum Architect
6. `[6/7]` Standalone HTML Portal Compilation (SSR)
7. `[7/7]` Exporter & ZIP Bundling

---

## 📁 Repository Structure

```
banking-support-agent/
├── coursecraft/
│   ├── app.py                      # Streamlit Studio (Port 8503)
│   ├── core/
│   │   ├── models.py               # Pydantic data schemas (Flashcard, LessonPage, CourseWeek, etc.)
│   │   └── state_manager.py        # Course state persistence and sample courses
│   ├── parsers/
│   │   ├── document_parser.py      # PDF, DOCX, PPTX, TXT parser & LaTeX extractor
│   │   ├── syllabus_parser.py      # Syllabus, grading policy, & chapter extractor
│   │   └── slide_parser.py         # Slide deck extractor
│   ├── agents/
│   │   ├── llm_orchestrator.py     # Multi-provider client (Gemini, OpenAI, Heuristic)
│   │   ├── syllabus_architect.py   # Multi-week curriculum compiler
│   │   ├── lesson_synthesizer.py   # Lesson block & flashcard synthesis
│   │   ├── quiz_generator.py       # Multiple choice quiz generator
│   │   ├── diagram_generator.py    # Mermaid diagram generator & syntax sanitizer
│   │   └── topic_scout.py          # Web business trend scout
│   ├── renderer/
│   │   └── portal_generator.py     # Standalone SSR HTML portal compiler
│   └── tests/
│       └── test_pipeline.py        # 7-stage test suite
├── USER_GUIDE.md                   # In-depth user manual and troubleshooting guide
├── sample_output.html              # Pre-compiled standalone portal preview
└── pyproject.toml                  # Python dependencies and project configuration
```

---

## ❓ Frequently Asked Questions

### Q: Does CourseCraft require an active internet connection to view generated course portals?
**No.** Portals are compiled into a standalone HTML file (`portal.html`) using Server-Side Pre-rendering (SSR). Students can view all lectures, formulas, diagrams, and quizzes completely offline.

### Q: Why did my uploaded textbook previously show "Week 20" or video titles?
In earlier versions, chapter-end reference lists (e.g. video citations like *"Brotherhood of Sleeping Car Porters"*) were captured as modules. The current version includes an intelligent citation filter and caps courses to authentic 4-to-8 week MBA modules.

### Q: What if my API key runs out of credits?
CourseCraft automatically switches to its offline heuristic synthesizer, ensuring the application never crashes during a live class or preparation session.

---

*CourseCraft AI &bull; Open-Source Academic Course Portal Studio*
