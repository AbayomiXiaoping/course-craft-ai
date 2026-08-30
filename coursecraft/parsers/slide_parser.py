"""
slide_parser.py
Parses slide-based lecture presentations, extracting individual slide titles, bullet hierarchies,
and code snippets.
"""

import re
from typing import List, Dict, Any


def parse_slides(text: str) -> List[Dict[str, Any]]:
    """Splits a multi-slide PDF transcript into structured slide objects."""
    # Split by Page or Slide markers
    pages = re.split(r"--- \[(?:Page|Slide) \d+\] ---", text)
    slides = []
    for idx, page in enumerate(pages):
        cleaned = page.strip()
        if not cleaned:
            continue
        lines = [l.strip() for l in cleaned.split("\n") if l.strip()]
        title = lines[0] if lines else f"Slide {idx + 1}"
        bullets = [l for l in lines[1:] if l.startswith(("-", "•", "*")) or len(l) > 15]

        slides.append(
            {
                "slide_index": idx + 1,
                "title": title.lstrip("#-•* "),
                "bullets": bullets,
                "raw_text": cleaned,
            }
        )
    return slides
