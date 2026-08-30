"""
models.py
Core Pydantic data contracts for CourseCraft AI.
Defines the schema for entire course portals, weeks, lessons, interactive quizzes,
case studies, web topic suggestions, and visual components.
Tailored for Management Studies (MBA/BBA programs).
"""

from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field
import uuid


class QuizOption(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    text: str
    is_correct: bool
    explanation: str


class QuizQuestion(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    question: str
    question_type: Literal["multiple_choice", "true_false", "numerical", "short_answer"] = "multiple_choice"
    options: List[QuizOption] = []
    hint: Optional[str] = None
    points: int = 10
    step_by_step_solution: Optional[str] = None


class ResourceLink(BaseModel):
    title: str
    url: Optional[str] = None
    type: Literal["pdf", "slides", "reading", "code", "external", "paper", "case_study"] = "reading"
    source_name: Optional[str] = None  # e.g., "Harvard Business Review", "McKinsey", "Economic Times"
    description: Optional[str] = None


class Flashcard(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    front: str
    back: str
    category: Optional[str] = "Core Concept"


class LessonBlock(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str
    block_type: Literal["concept", "proof_math", "code", "diagram", "callout", "quiz", "case_study"] = "concept"
    content_markdown: str
    applied_example: Optional[str] = None  # Concrete real-world business example
    latex_formulas: List[str] = []
    mermaid_diagram: Optional[str] = None
    code_language: Optional[str] = None
    code_snippet: Optional[str] = None
    case_company: Optional[str] = None  # e.g., "Swiggy", "Tata Motors", "Infosys"
    interactive_quiz: Optional[List[QuizQuestion]] = None


class LessonPage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str
    estimated_read_time_minutes: int = 15
    learning_objectives: List[str] = []
    blocks: List[LessonBlock] = []
    flashcards: List[Flashcard] = []
    practice_problems: List[QuizQuestion] = []
    further_readings: List[ResourceLink] = []


class CourseWeek(BaseModel):
    week_number: int
    title: str
    theme: str
    dates: Optional[str] = None
    overview: str
    lessons: List[LessonPage] = []
    assignments: List[str] = []
    readings: List[str] = []


class SuggestedTopic(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str
    discipline: str  # "Strategy", "Fintech", "Marketing", "Supply Chain", "HR", "AI in Business"
    source_website: str  # e.g. "Harvard Business Review", "McKinsey Insights", "Economic Times", "Livemint"
    source_url: str
    relevance_summary: str
    suggested_case_study: str
    why_relevant_for_bangalore_students: str
    target_learning_outcome: str


class CoursePortal(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    course_code: str = "MBA-602"
    course_title: str = "Strategic Management & Digital Business Models"
    university: str = "Department of Management Studies, School of Business"
    professor_name: str = "Prof. Rajesh Sharma, Ph.D."
    semester: str = "Trimester III / Academic Year 2026-27"
    office_hours: Optional[str] = "Mon & Wed 2:30 PM – 4:30 PM (Management Block, Cabin 304)"
    prerequisites: List[str] = [
        "Principles of Management",
        "Managerial Economics",
        "Business Analytics & Statistics",
    ]
    syllabus_summary: str = (
        "Designed specifically for Management Students (MBA/BBA), this course "
        "bridges foundational business strategy with digital platform ecosystems, high-growth startup and "
        "fintech models, AI-driven corporate transformation, and real-world Harvard Business Review style case studies."
    )
    grading_policy: Dict[str, str] = {
        "HBR Case Study Analyses (3x)": "30%",
        "Mid-Trimester Examination": "20%",
        "Corporate Industry Capstone Project": "35%",
        "Class Discussion & Formative Quizzes": "15%",
    }
    weeks: List[CourseWeek] = []
    theme_palette: Literal[
        "oxford_navy", "harvard_crimson", "mit_slate", "stanford_cardinal", "emerald_poly"
    ] = "oxford_navy"
