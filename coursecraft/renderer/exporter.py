"""
exporter.py
Exports CourseCraft generated portals into standalone HTML bundles and downloadable ZIP archives.
"""

import io
import zipfile
from pathlib import Path
from coursecraft.core.models import CoursePortal
from coursecraft.renderer.portal_generator import generate_portal_html


def export_portal_to_file(course: CoursePortal, output_path: str | Path) -> Path:
    """Writes the generated course portal HTML to disk."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    html_content = generate_portal_html(course)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return path


def create_course_zip_bundle(course: CoursePortal) -> bytes:
    """Creates an in-memory ZIP package containing index.html, metadata, and README."""
    html_content = generate_portal_html(course)
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("index.html", html_content)
        zip_file.writestr("course_manifest.json", course.model_dump_json(indent=2))
        readme_text = f"""# {course.course_code}: {course.course_title}
Instructor: {course.professor_name}
University: {course.university}
Semester: {course.semester}

## Deployment
- Simply upload this directory or 'index.html' to GitHub Pages, Netlify, Vercel, or AWS S3.
- To view locally, double-click 'index.html' in any modern web browser.
- Generated automatically via CourseCraft AI.
"""
        zip_file.writestr("README.md", readme_text)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()
