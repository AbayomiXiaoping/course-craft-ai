"""
quiz_generator.py
Generates interactive formative quizzes, hints, and step-by-step solutions
for graduate management and MBA students.
"""

import json
import re
from typing import List
from coursecraft.core.models import QuizQuestion, QuizOption
from coursecraft.agents.llm_orchestrator import generate_structured_synthesis


def generate_quizzes_from_text(topic: str, content: str, count: int = 2) -> List[QuizQuestion]:
    """Generates interactive formative assessment questions for a given topic."""
    system_prompt = (
        "You are an expert MBA business school professor creating rigorous formative assessment questions. "
        "Return a valid JSON object with key 'questions', which is an array of objects. "
        "Each object must have: 'question' (string), 'options' (array of 3-4 objects with 'text', 'is_correct' boolean, 'explanation'), "
        "'hint' (string), 'step_by_step_solution' (string), and 'points' (int)."
    )
    user_prompt = f"Topic: {topic}\nContext:\n{content[:2500]}\nGenerate {count} high-quality management decision-making questions."

    raw_json = generate_structured_synthesis(system_prompt, user_prompt)
    if raw_json:
        try:
            data = json.loads(raw_json)
            questions = []
            for q in data.get("questions", []):
                options = [
                    QuizOption(
                        text=opt["text"],
                        is_correct=opt["is_correct"],
                        explanation=opt["explanation"],
                    )
                    for opt in q.get("options", [])
                ]
                questions.append(
                    QuizQuestion(
                        question=q["question"],
                        options=options,
                        hint=q.get("hint"),
                        points=q.get("points", 10),
                        step_by_step_solution=q.get("step_by_step_solution"),
                    )
                )
            if questions:
                return questions
        except Exception:
            pass

    # High-quality MBA / Management Offline Fallback Questions
    clean_t = re.sub(r"^(?:Week\s*\d+\s*[-:]?\s*)+", "", topic).strip()
    topic_lower = topic.lower()

    if any(k in topic_lower for k in ["human resource", "hrm", "talent", "employee", "organization", "personnel"]):
        return [
            QuizQuestion(
                question=f"In Strategic Human Resource Management ({clean_t}), what is the primary purpose of aligning HR practices with corporate strategy?",
                options=[
                    QuizOption(
                        text="To leverage human capital and employee competencies as a source of sustained competitive advantage",
                        is_correct=True,
                        explanation="Strategic HRM positions employees as core assets whose capabilities directly execute and differentiate organizational strategy.",
                    ),
                    QuizOption(
                        text="To minimize all investments in employee development and focus solely on short-term payroll cuts",
                        is_correct=False,
                        explanation="Treating HR solely as a cost center impairs organizational agility and increases turnover costs.",
                    ),
                    QuizOption(
                        text="To eliminate the need for regulatory compliance, labor standards, and health regulations",
                        is_correct=False,
                        explanation="Compliance remains a fundamental baseline requirement of the HR management function.",
                    ),
                ],
                hint="Consider how strategic HRM views employees as assets rather than mere administrative overhead.",
                points=10,
                step_by_step_solution=(
                    "1. Strategic HRM aligns workforce planning with long-term business goals.\n"
                    "2. Competitive moats increasingly rely on tacit knowledge, culture, and employee innovation.\n"
                    "3. Therefore, human capital alignment creates sustainable competitive advantage."
                ),
            )
        ]

    if any(k in topic_lower for k in ["platform", "network", "ecosystem", "marketplace", "swiggy", "zomato"]):
        return [
            QuizQuestion(
                question=f"In platform economics and digital marketplaces ({clean_t}), what creates defensibility against traditional competitors?",
                options=[
                    QuizOption(
                        text="Cross-side network effects where high demand-side density attracts supply partners, creating a self-reinforcing flywheel",
                        is_correct=True,
                        explanation="Multi-sided platforms generate defensible moats through positive feedback loops between buyers and sellers.",
                    ),
                    QuizOption(
                        text="Exclusive linear ownership of physical assets and elimination of all software orchestration",
                        is_correct=False,
                        explanation="Platforms rely on coordination and orchestration rather than heavy capital assets.",
                    ),
                    QuizOption(
                        text="Fixed flat pricing models completely detached from market equilibrium and real-time demand",
                        is_correct=False,
                        explanation="Dynamic pricing and algorithmic allocation are essential to platform liquidity.",
                    ),
                ],
                hint="Think about the feedback loop between customers and merchant supply density.",
                points=10,
                step_by_step_solution=(
                    "1. Pipeline firms compete linearly via supply chain control.\n"
                    "2. Platform firms orchestrate interactions between two or more user groups.\n"
                    "3. Network effects make the platform exponentially more valuable as participation grows."
                ),
            )
        ]

    # General Business Strategy Fallback
    return [
        QuizQuestion(
            question=f"When analyzing strategic decision-making in '{clean_t}', which criterion best validates long-term economic viability?",
            options=[
                QuizOption(
                    text="Generating sustained positive contribution margins with an LTV-to-CAC ratio exceeding 3.0",
                    is_correct=True,
                    explanation="Sustainable value creation requires unit economics where customer lifetime value comfortably covers acquisition and operational delivery costs.",
                ),
                QuizOption(
                    text="Aggressively scaling customer acquisition while operating on perpetually negative gross margins",
                    is_correct=False,
                    explanation="Growth without positive unit economics leads to insolvency once external capital subsidies end.",
                ),
                QuizOption(
                    text="Focusing exclusively on short-term vanity metrics without measuring retention or churn rates",
                    is_correct=False,
                    explanation="Retention and cohorts determine long-term enterprise value.",
                ),
            ],
            hint="Focus on the relationship between customer acquisition cost and lifetime value.",
            points=10,
            step_by_step_solution=(
                "1. Sustainable business models require positive unit economics.\n"
                "2. Customer Lifetime Value (LTV) must exceed Acquisition Cost (CAC) by at least 3:1.\n"
                "3. Contribution margin must cover fixed overhead and capital costs."
            ),
        )
    ]
