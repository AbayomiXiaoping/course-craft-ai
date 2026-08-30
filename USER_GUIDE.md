# CourseCraft AI — Complete User Guide & Operating Manual

> **CourseCraft AI**: An intelligent course portal synthesis engine engineered for university professors and academic deans to transform raw academic materials (textbooks, PDFs, syllabi, and slides) into high-engagement, production-ready web portals.

---

## 📑 Table of Contents
1. [Overview & Key Capabilities](#1-overview--key-capabilities)
2. [Quick Start & Launching the App](#2-quick-start--launching-the-app)
3. [LLM Configuration & API Key Setup](#3-llm-configuration--api-key-setup)
4. [Step-by-Step Studio Walkthrough](#4-step-by-step-studio-walkthrough)
   - [Sidebar: Institutional Settings & AI Provider](#sidebar-institutional-settings--ai-provider)
   - [Tab 1: Course Roadmap & Week Navigator](#tab-1-course-roadmap--week-navigator)
   - [Tab 2: Web Topic Scout & External Industry Cases](#tab-2-web-topic-scout--external-industry-cases)
   - [Tab 3: Material Ingestion & Ingest Hub (PDF / Syllabus)](#tab-3-material-ingestion--ingest-hub-pdf--syllabus)
   - [Tab 4: Interactive Live HTML Portal Preview](#tab-4-interactive-live-html-portal-preview)
   - [Tab 5: Production Export & Packaging](#tab-5-production-export--packaging)
5. [Interactive Features in Generated Web Pages](#5-interactive-features-in-generated-web-pages)
   - [🗂️ 3D Interactive Concept Flashcards](#-3d-interactive-concept-flashcards)
   - [💡 Applied Business & Industry Examples](#-applied-business--industry-examples)
   - [📐 Managerial & Analytical Formulas (KaTeX)](#-managerial--analytical-formulas-katex)
   - [📊 Strategy Flowcharts & Value Chains (Mermaid)](#-strategy-flowcharts--value-chains-mermaid)
   - [🧠 Formative Decision Quizzes & Scoring](#-formative-decision-quizzes--scoring)
6. [Automated Testing & Pipeline Verification](#6-automated-testing--pipeline-verification)
7. [Troubleshooting & FAQs](#7-troubleshooting--faqs)

---

## 1. Overview & Key Capabilities

CourseCraft AI solves a major pain point for university faculty: **turning dense textbooks, fragmented PDFs, and lecture slides into engaging, interactive online learning hubs**.

### Core Pillars:
* **Server-Side Pre-Rendered Portals (SSR)**: Generates single-file, zero-dependency HTML portals that open in any browser (Chrome, Safari, Edge, Firefox) without requiring Node.js, external servers, or internet access.
* **Dual-Engine LLM Architecture**:
  * **Google Gemini (Free Tier via Antigravity / AI Studio)**: Ultra-fast multimodal reasoning using `gemini-3.6-flash`.
  * **OpenAI Integration**: Full support for `gpt-4o-mini` and `gpt-4o`.
  * **Built-in Heuristic Fallback**: Generates rigorous academic curriculums and formulas completely offline if API keys are absent or rate-limited.
* **Management Curriculum Focus**: Specifically tailored for MBA and BBA management disciplines (Business Strategy, Platform Economics, Fintech, Supply Chain, Human Resource Management, and Marketing Analytics).
* **Smart Cleaning Pipeline**: Automatically filters out front-matter boilerplate (copyright notices, ISBN, blank pages, and Pressbooks licenses) and excludes bibliographic video citations (`"Brotherhood of Sleeping Car Porters"`) from contaminating curriculum weeks.

---

## 2. Quick Start & Launching the App

### Prerequisites
* macOS, Linux, or Windows with Python 3.10+
* Recommended package runner: `uv` (or standard `python3` / `pip`)

### Launching CourseCraft Studio
Run the following command from the repository root:

```bash
PYTHONPATH=. uv run streamlit run coursecraft/app.py --server.port 8503
```

Open your browser and navigate to:
👉 **`http://localhost:8503`**

*(If port 8503 is in use, Streamlit will automatically assign the next available port, e.g. 8504).*

---

## 3. LLM Configuration & API Key Setup

CourseCraft AI gives you complete freedom to use **Free Google Gemini**, **OpenAI**, or **Offline Mode**.

### Option 1: Free Google Gemini (Recommended)
Google provides a **100% Free Tier** through Google AI Studio with generous limits (15 requests/minute, 1M tokens/minute) and **no credit card required**:
1. Get a key in 30 seconds at: **[Google AI Studio](https://aistudio.google.com/app/apikey)**.
2. In the CourseCraft Studio sidebar under **🔑 LLM Configuration**, select **"Google Gemini (Free)"**.
3. Paste your key (`AIzaSy...` or `AQ.Ab8...`) into the **Gemini API Key** field.
4. Click **"🧪 Test Gemini Connection"** to verify that the model responds.
5. *(Optional)* Store it in `~/.zshrc` or `.env` so you never have to re-enter it:
   ```bash
   echo 'export GEMINI_API_KEY="your_gemini_key_here"' >> ~/.zshrc
   source ~/.zshrc
   ```

### Option 2: OpenAI
1. Select **"OpenAI"** in the sidebar.
2. Paste your OpenAI API key (`sk-proj-...`).
3. Select your model (`gpt-4o-mini` or `gpt-4o`).
4. Click **"🧪 Test OpenAI Connection"**.

### Option 3: Offline Mode (No API Key Required)
If no key is configured or your credit balance is exhausted, CourseCraft **automatically switches to its built-in pedagogical heuristic synthesizer**. It constructs formulas, cases, and diagrams without crashing.

---

## 4. Step-by-Step Studio Walkthrough

CourseCraft Studio is organized into a sidebar and **5 intuitive tabs**:

```
┌─────────────────┬────────────────────────────────────────────────────────┐
│  SIDEBAR        │  TABS:                                                 │
│                 │  1. 📅 Course Roadmap & Week Navigator                 │
│  ⚙️ Course Meta │  2. 🌐 Web Topic Scout & External Industry Cases       │
│  🎨 Theme Picker│  3. 📤 Material Ingestion & Ingest Hub (PDF / Outline) │
│  🔑 LLM Config  │  4. 👁️ Interactive Live HTML Portal Preview           │
│  📊 Statistics  │  5. 📦 Production Export & Packaging                   │
└─────────────────┴────────────────────────────────────────────────────────┘
```

---

### Sidebar: Institutional Settings & AI Provider
* **Course Code**: Edit the course identifier (e.g., `MBA-602`, `HRM-501`).
* **Course Title**: Course name (e.g., *Strategic Management & Digital Business Models*).
* **Instructor**: Instructor name (e.g., *Prof. Rajesh Sharma, Ph.D.*).
* **Institution**: University department (*Department of Management Studies, School of Business*).
* **Institutional Theme**: Choose from 5 curated academic palettes:
  * 🏛️ **Classic Oxford Navy & Gold** (Default)
  * 🍷 **Harvard Crimson**
  * ⚙️ **MIT Slate**
  * 🌲 **Stanford Cardinal**
  * 🌿 **Emerald Poly**
* **Course Stats**: Live metrics showing active curriculum weeks, total lessons, case studies, and quiz problems.

---

### Tab 1: Course Roadmap & Week Navigator
This tab displays your semester curriculum tree:
* **Weekly Breakdown**: Expand any week to inspect its learning theme, dates, lecture title, estimated reading time, and learning objectives.
* **Lesson Inspector**: Review the sequence of content blocks inside each lesson (Foundations, Analytical Formulas, Diagrams, Executive Case Studies, Quizzes).
* **Add Week Button**: Dynamically append new customized weeks to your curriculum.

---

### Tab 2: Web Topic Scout & External Industry Cases
Keep your curriculum cutting-edge by scouting trending management developments from reputable sources (Harvard Business Review, McKinsey Insights, MIT Sloan, The Economic Times):
1. **Filter by Discipline**: Select your subject domain (*Strategic Management*, *Platform Economics*, *Fintech & Banking*, *Operations & Supply Chain*, *HR & Talent Analytics*, *Marketing Analytics*).
2. **Search Custom Trends**: Enter a custom keyword (e.g., `"Quick Commerce Zepto Blinkit"`, `"GCC Talent Retention Bangalore"`).
3. **Curated Topic Cards**: Each card displays:
   * Article Source & Link (e.g. *Harvard Business Review*)
   * Executive Summary
   * Bangalore & Indian Market Relevance
   * Target Learning Outcome
4. **"➕ Adopt into Course Curriculum"**: Clicking this button instantly synthesizes the trending topic into a full multi-block interactive lesson (complete with formulas, diagrams, a case study, quiz, and 3D flashcards) and appends it to your course!

---

### Tab 3: Material Ingestion & Ingest Hub (PDF / Syllabus)
Upload raw teaching files to automatically assemble new courses:
1. **Supported Formats**: `.pdf` (textbooks, chapters, syllabi), `.docx`, `.pptx` (slide decks), and `.txt` / `.md` (notes).
2. **Text Paste Area**: Alternatively, paste syllabus outlines, course specifications, or reading excerpts directly.
3. **Click "🚀 Analyze & Synthesize Multi-Week Course Portal"**:
   * **Boilerplate Stripper**: Automatically removes copyright notices, Pressbooks publishing metadata, ISBN headers, and `--- [Page X] ---` markers.
   * **Smart Citation Filter**: Excludes endnotes, video references, and bibliography entries (e.g. *"Brotherhood of Sleeping Car Porters"*) from becoming fake weeks.
   * **Currency vs. Math Separation**: Dollar amounts (`$5 and $1 to $100,000`) are treated as normal financial text; genuine LaTeX equations are converted into KaTeX mathematical callouts.
   * **Gemini Curriculum Architect**: Generates a structured 4-to-8 week MBA course schedule with real academic unit themes.

---

### Tab 4: Interactive Live HTML Portal Preview
View the exact portal your students will see directly inside Streamlit:
* **View Selector**: Switch between the **Overview & Syllabus Roadmap** and individual weekly lectures.
* **Live Features**: Click through the 3D flashcards, test the quizzes, and inspect the Mermaid diagrams in real-time.
* **Full-Window Preview**: Click the link to open the pre-rendered portal in a dedicated browser tab.

---

### Tab 5: Production Export & Packaging
Package and deploy your course web portal:
* **Option A: Download Standalone HTML (`portal.html`)**:
  * A single, self-contained file with all CSS, JavaScript, pre-rendered DOM, KaTeX, and Mermaid bundles included.
  * Send it via email or upload to LMS (Canvas, Moodle, Blackboard, Google Classroom). Students simply double-click to open it offline.
* **Option B: Download Complete Bundle (`course_portal_bundle.zip`)**:
  * Contains `index.html`, course JSON data, syllabus backups, and deployment instructions for hosting on GitHub Pages, Vercel, Netlify, or university web servers.
* **Option C: Export Course Blueprint (`course_data.json`)**:
  * Full JSON state file that can be version-controlled in Git or re-imported into CourseCraft later.

---

## 5. Interactive Features in Generated Web Pages

When students open your CourseCraft portal, they experience a rich, modern digital textbook with:

### 🗂️ 3D Interactive Concept Flashcards
* **Active Recall**: Located at the end of each lecture to test knowledge retention before assignments.
* **3D Flipping Animation**: Click any card or click **"Flip Card 🔄"** to smoothly rotate the card 180 degrees.
* **Front Face**: Displays the core concept or formula name, domain category badge, and flip hint.
* **Back Face**: Displays the strategic definition, managerial derivation, and practical takeaway.
* **Navigation Controls**: `◀ Previous`, `Flip Card 🔄`, `Next ▶`, and live card counter (`Card 1 of 4`).

### 💡 Applied Business & Industry Examples
* Every theoretical concept is accompanied by a styled **Applied Business Example** callout card.
* Framed around real-world Indian and global market dynamics (e.g. Swiggy/Zomato unit economics in Bangalore, Blinkit dark store batching, Razorpay UPI underwriting, and IT GCC talent retention frameworks).

### 📐 Managerial & Analytical Formulas (KaTeX)
* High-visibility callout blocks for quantitative metrics (Contribution Margin II, LTV:CAC ratios, Annual Employee Turnover Rate, Human Capital ROI, and Net Interest Margin).
* Rendered via KaTeX for crisp rendering on high-resolution screens.

### 📊 Strategy Flowcharts & Value Chains (Mermaid)
* Interactive platform flowcharts, multi-sided network interactions, and supply chain diagrams.
* Sanitized label parsing prevents syntax crashes; includes automatic fallback rendering cards.

### 🧠 Formative Decision Quizzes & Scoring
* Multiple-choice questions testing managerial judgment over rote memorization.
* **Instant Visual Feedback**: Selected options turn green (✅ Correct) or red (❌ Incorrect) with detailed pedagogical explanations.
* **Point Tracking**: Live score badge at the top of the quiz.
* **Step-by-Step Solutions**: Collapsible drawer revealing analytical derivations and decision rationale.

---

## 6. Automated Testing & Pipeline Verification

CourseCraft AI includes an automated 7-stage verification test suite. To verify your setup, run:

```bash
uv run python coursecraft/tests/test_pipeline.py
```

### Verification Test Stages:
1. `[1/7]` **Course Model & State Manager**: Validates Pydantic schemas and course portal state integrity.
2. `[2/7]` **Web Topic Scout**: Tests external business trend discovery and 1-click lesson synthesis.
3. `[3/7]` **Syllabus & Document Parser**: Validates PDF text cleaning, math extraction, and citation noise rejection.
4. `[4/7]` **Quiz & Lesson Synthesizer**: Checks block compilation, applied examples, and 3D flashcard generation.
5. `[5/7]` **Multi-Week Architect**: Tests Gemini AI curriculum scheduling and fallback heuristics.
6. `[6/7]` **HTML Portal Pre-Renderer (SSR)**: Generates standalone HTML with KaTeX, Mermaid, and quizzes.
7. `[7/7]` **Exporter & Bundler**: Validates ZIP packaging and JSON serialization.

---

## 7. Troubleshooting & FAQs

### Q1: Why did my uploaded textbook have "Week 20" or video titles in the navigation?
* **Cause**: Older versions of the parser matched chapter-end video citations (e.g. `Module 20: 19: Brotherhood of Sleeping Car Porters By Historica Canada`).
* **Fix**: The current version has a dedicated citation validator that excludes video links, author quotes, and bibliography lines. It automatically caps courses to 4–8 authentic MBA weeks.

### Q2: Why were dollar amounts showing up as math formulas?
* **Cause**: In older parsers, prose containing multiple currency figures (`$5 and $1 to $100,000`) was misinterpreted as inline LaTeX math (`$...$`).
* **Fix**: The regex now strictly requires mathematical syntax (`\frac`, `=`, `_`, `^`, `\text`) before creating a formula card. Regular dollar amounts remain formatted as clean currency text.

### Q3: My OpenAI key says "credit_balance_exhausted (429)". What should I do?
* **Solution**: Switch to **Google Gemini (Free)** in the sidebar! It uses the free Google AI Studio key you have configured in your environment (`GEMINI_API_KEY`), which has zero charges and requires no credit card. CourseCraft will also fall back to its offline academic synthesizer if no credits are available.

### Q4: How do I share the generated course with my students?
* Navigate to **Tab 5 (`📦 Production Export`)**.
* Click **"Download Standalone Portal (HTML)"**.
* Upload `portal.html` to your university LMS (Canvas, Moodle, Google Classroom) or email it to students. They do not need to install anything—double-clicking the file opens the entire interactive portal in any browser.

---

*CourseCraft AI &bull; Academic Course Portal Studio &bull; Documentation Version 2.4*
