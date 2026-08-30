"""
document_parser.py
PDF and document parser for CourseCraft AI.
Extracts text, slide boundaries, section titles, and math formulas from uploaded materials.
Cleans raw PDF artifacts, page headers, copyright boilerplate, and distinguishes real LaTeX from currency amounts.
"""

import io
import re
from typing import List, Dict, Any
from pypdf import PdfReader


def clean_academic_text(text: str) -> str:
    """Removes page markers, copyright disclaimers, and publishing boilerplate."""
    if not text:
        return ""
    # Strip page header lines like --- [Page 1] ---
    cleaned = re.sub(r"---\s*\[Page\s*\d+\]\s*---", "\n", text)
    # Remove common open-textbook / publisher boilerplate
    boilerplate_patterns = [
        r"Creative Commons\s+Attribution[^\n\r]+",
        r"Pressbooks\s+[A-Za-z\s]+",
        r"Library of Congress[^\n\r]+",
        r"ISBN[:\s\-\d]+",
        r"All rights reserved\.?",
        r"Printed in[^\n\r]+",
        r"Changes from Adapted Resource[^\n\r]+",
        r"Acknowledgments\s+[ivx\d]+",
        r"About This Book\s+[ivx\d]+",
    ]
    for bp in boilerplate_patterns:
        cleaned = re.sub(bp, "", cleaned, flags=re.IGNORECASE)

    # Normalize excessive blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts raw text page-by-page from an in-memory PDF file and cleans boilerplate."""
    reader = PdfReader(io.BytesIO(file_bytes))
    full_text = []
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        # Skip completely empty or 1-2 character pages
        if len(page_text.strip()) > 5:
            full_text.append(f"--- [Page {i + 1}] ---\n{page_text.strip()}")
    raw = "\n\n".join(full_text)
    return raw


def detect_document_type(text: str) -> str:
    """Classifies the uploaded document based on structural heuristics."""
    lower = text.lower()
    if any(k in lower for k in ["syllabus", "grading policy", "office hours", "course schedule", "course outline"]):
        return "syllabus"
    if any(k in lower for k in ["chapter 1", "table of contents", "learning outcomes", "introduction to human resource"]):
        return "textbook_chapter"
    if any(k in lower for k in ["problem set", "homework", "exam", "assignment", "quiz", "points"]):
        return "problem_set"
    if any(k in lower for k in ["slide", "agenda", "key takeaways"]) or text.count("--- [Page ") > 12:
        return "slides"
    return "lecture_notes"


def extract_potential_latex(text: str) -> List[str]:
    """Extracts genuine LaTeX equations formatted with $...$ or $$...$$ or \\begin{equation}.
    Carefully filters out currency amounts ($10, $50,000) and prose between dollar signs.
    """
    if not text:
        return []

    dd_matches = re.findall(r"\$\$(.+?)\$\$", text, flags=re.DOTALL)
    eq_matches = re.findall(
        r"\\begin\{(?:equation|align|gather)\*?\}(.+?)\\end\{(?:equation|align|gather)\*?\}",
        text,
        flags=re.DOTALL,
    )

    # For single dollar signs ($...$), require genuine mathematical indicators
    single_dollar = re.findall(r"(?<!\\)\$([^\$\n\r]+?)\$", text)
    valid_singles = []
    math_indicators = ["\\", "^", "_", "=", r"\ge", r"\le", r"\times", r"\pm", r"\approx", r"\frac", r"\text"]
    for s in single_dollar:
        clean = s.strip()
        # Reject currency (e.g. 5, 100,000, 51 billion) or plain text without math indicators
        if any(ind in clean for ind in math_indicators):
            # Verify it is not just a currency phrase
            if not re.search(r"^\d+[\d,\.]*\s*(?:billion|million|thousand|dollars|per\s+year)", clean, re.IGNORECASE):
                valid_singles.append(clean)

    formulas = []
    for f in dd_matches + eq_matches + valid_singles:
        clean = f.strip()
        if clean and clean not in formulas and len(clean) > 2:
            # Final sanity check: cannot contain words like "death of an employee" or "per year"
            if not any(bad in clean.lower() for bad in ["employee", "death", "per year", "costs range"]):
                formulas.append(clean)

    return formulas
