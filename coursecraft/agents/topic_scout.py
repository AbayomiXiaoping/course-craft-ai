"""
topic_scout.py
Scouts and recommends trending business topics and field case studies.
Tailored specifically for Management Students (MBA/BBA programs).
"""

import json
from typing import List, Optional, Dict, Any
from coursecraft.core.models import (
    SuggestedTopic,
    LessonPage,
    LessonBlock,
    QuizQuestion,
    QuizOption,
    ResourceLink,
    Flashcard,
)
from coursecraft.agents.llm_orchestrator import generate_structured_synthesis


CURATED_MANAGEMENT_TOPICS: List[SuggestedTopic] = [
    SuggestedTopic(
        title="Quick Commerce & Dark Store Economics in Indian Metros",
        discipline="Supply Chain & Strategy",
        source_website="Harvard Business Review & Economic Times",
        source_url="https://economictimes.indiatimes.com/tech/technology",
        relevance_summary=(
            "Analysis of 10-minute grocery delivery models (Blinkit, Zepto, Swiggy Instamart), "
            "unit economics, dark store inventory density, and hyper-local fulfillment challenges in Bangalore."
        ),
        suggested_case_study="Zepto vs. Swiggy Instamart: The Battle for Bangalore Urban Households",
        why_relevant_for_bangalore_students=(
            "Bengaluru is the primary innovation testbed for quick commerce. Management students "
            "can evaluate live supply chain metrics, dark store routing algorithms, and consumer purchase behaviors firsthand."
        ),
        target_learning_outcome="Analyze contribution margins per delivery, calculate customer lifetime value (LTV:CAC), and assess regulatory packaging compliance.",
    ),
    SuggestedTopic(
        title="India's Digital Public Infrastructure (DPI) & ONDC Disruption",
        discipline="Fintech & Digital Business",
        source_website="McKinsey Insights & Livemint",
        source_url="https://www.mckinsey.com/industries/financial-services/our-insights",
        relevance_summary=(
            "How UPI, ONDC (Open Network for Digital Commerce), and the Account Aggregator framework "
            "democratize financial inclusion and challenge established platform monopolies."
        ),
        suggested_case_study="ONDC vs. Amazon/Flipkart: Decentralized Marketplaces in India",
        why_relevant_for_bangalore_students=(
            "Bangalore houses major fintech unicorns (PhonePe, CRED, Razorpay). Understanding open protocols "
            "prepares students for careers in product management, venture capital, and banking transformation."
        ),
        target_learning_outcome="Evaluate platform network effects, unbundled value chains, and monetization models in open financial architectures.",
    ),
    SuggestedTopic(
        title="Enterprise Generative AI Adoption in Global Capability Centers (GCCs)",
        discipline="AI & Technology Management",
        source_website="MIT Sloan Management Review",
        source_url="https://sloanreview.mit.edu/topic/artificial-intelligence/",
        relevance_summary=(
            "The transformation of Indian IT services (TCS, Infosys, Wipro) and multinational GCCs "
            "from cost-arbitrage centers into strategic AI innovation engines."
        ),
        suggested_case_study="Infosys Topaz & Accenture AI Foundry: Transitioning Billable Hours to Outcome-Based AI Pricing",
        why_relevant_for_bangalore_students=(
            "Over 40% of India's GCCs are concentrated in Bengaluru. Management graduates "
            "regularly interview for consulting, corporate strategy, and talent management roles at these firms."
        ),
        target_learning_outcome="Construct an AI governance framework, calculate ROI on enterprise LLM deployment, and navigate workforce re-skilling.",
    ),
    SuggestedTopic(
        title="EV Ecosystem & Green Mobility Financing in Karnataka",
        discipline="Sustainable Finance & Operations",
        source_website="World Economic Forum & Financial Express",
        source_url="https://www.weforum.org/agenda/energy-transition/",
        relevance_summary=(
            "Commercial vehicle electrification, battery swapping economics, and green bond financing "
            "under Karnataka's Electric Vehicle and Energy Storage Policy."
        ),
        suggested_case_study="Ather Energy & Tata Passenger Electric Mobility: Scaling Charging Infrastructure",
        why_relevant_for_bangalore_students=(
            "Bangalore is the EV capital of India (headquarters of Ather, Ola Electric, Sun Mobility). "
            "Students study localized manufacturing incentives, ESG metrics, and debt syndication."
        ),
        target_learning_outcome="Formulate total cost of ownership (TCO) models, assess carbon credit accounting, and evaluate supply chain de-risking for lithium cells.",
    ),
    SuggestedTopic(
        title="Omnichannel D2C Brand Building & Performance Marketing",
        discipline="Marketing Analytics",
        source_website="Harvard Business Review",
        source_url="https://hbr.org/topic/marketing",
        relevance_summary=(
            "How digital-native Indian consumer brands (Mamaearth, Licious, Boat) navigate surging Facebook/Google "
            "customer acquisition costs (CAC) by pivoting to offline modern trade and tier-2 expansion."
        ),
        suggested_case_study="Mamaearth: From Digital Pure-Play to General Trade Distribution & IPO",
        why_relevant_for_bangalore_students=(
            "Understanding performance marketing metrics vs. traditional FMCG distribution is essential for "
            "careers in brand management, retail consulting, and consumer venture capital."
        ),
        target_learning_outcome="Calculate blended CAC, Return on Ad Spend (ROAS), and optimize channel allocation across Amazon, quick commerce, and Kirana retail.",
    ),
]


def fetch_suggested_topics(discipline: Optional[str] = None, custom_query: Optional[str] = None) -> List[SuggestedTopic]:
    """Retrieves curated and AI-generated trending business topics for MBA courses."""
    system_prompt = (
        "You are an academic dean at a leading graduate business school. "
        "Recommend current, high-impact business and management case topics based on reputable sources "
        "(e.g. Harvard Business Review, McKinsey Insights, MIT Sloan, The Economic Times, Mint). "
        "Return a valid JSON object with key 'topics', an array of objects matching: "
        "'title', 'discipline', 'source_website', 'source_url', 'relevance_summary', "
        "'suggested_case_study', 'why_relevant_for_bangalore_students', 'target_learning_outcome'."
    )
    user_prompt = (
        f"Discipline focus: {discipline or 'General MBA / Strategic Management'}\n"
        f"Custom focus or syllabus keywords: {custom_query or 'Trending Indian & Global Business Innovations 2026'}\n"
        "Generate 3-4 cutting-edge management topics with specific Bangalore/Indian market relevance."
    )

    raw_json = generate_structured_synthesis(system_prompt, user_prompt, max_tokens=1400)
    if raw_json:
        try:
            data = json.loads(raw_json)
            topics = []
            for item in data.get("topics", []):
                topics.append(
                    SuggestedTopic(
                        title=item["title"],
                        discipline=item.get("discipline", discipline or "Management"),
                        source_website=item.get("source_website", "Harvard Business Review & Economic Times"),
                        source_url=item.get("source_url", "https://hbr.org"),
                        relevance_summary=item["relevance_summary"],
                        suggested_case_study=item.get("suggested_case_study", "Case Analysis"),
                        why_relevant_for_bangalore_students=item.get("why_relevant_for_bangalore_students", "Relevant to Bangalore's corporate ecosystem."),
                        target_learning_outcome=item.get("target_learning_outcome", "Develop strategic business insights."),
                    )
                )
            if topics:
                return topics
        except Exception:
            pass

    # Fallback to curated topics filtered by discipline if requested
    if discipline:
        filtered = [t for t in CURATED_MANAGEMENT_TOPICS if discipline.lower() in t.discipline.lower()]
        return filtered if filtered else CURATED_MANAGEMENT_TOPICS
    return CURATED_MANAGEMENT_TOPICS


def convert_topic_to_lesson(topic: SuggestedTopic, week_num: int) -> LessonPage:
    """Converts a suggested web business topic into a rich, interactive pedagogical LessonPage."""
    # Quantitative business formula for management students
    math_block = LessonBlock(
        title="2. Managerial Economics & Quantitative Formulation",
        block_type="proof_math",
        content_markdown=(
            "Evaluating the business viability and investment hurdle rate requires rigor in unit economics:"
        ),
        latex_formulas=[
            r"\text{Customer Lifetime Value (LTV)} = \frac{\text{Average Order Value} \times \text{Gross Margin \%}}{\text{Monthly Churn Rate}}",
            r"\text{Hurdle Condition}: \quad \frac{\text{LTV}}{\text{Customer Acquisition Cost (CAC)}} \ge 3.0",
            r"\text{Contribution Margin II} = \text{Revenue} - (\text{COGS} + \text{Packaging} + \text{Last-Mile Routing Costs})",
        ],
    )

    # Strategy / Value Chain Mermaid diagram
    diagram_block = LessonBlock(
        title="3. Strategic Value Chain & Market Flow",
        block_type="diagram",
        content_markdown="Organizational process and platform interaction:",
        mermaid_diagram=f"""flowchart LR
    Consumer([Target Customer in Bangalore]) --> Demand[Digital Discovery / Demand Channel]
    Demand --> Platform{{Marketplace / Algorithm Engine}}
    Platform --> Fulfillment[Fulfillment Hub / Dark Store Network]
    Platform --> Partner[Ecosystem Suppliers / FMCG Brands]
    Fulfillment --> Delivery([Hyper-local Delivery & Feedback Loop])
""",
    )

    # Case study block
    case_block = LessonBlock(
        title=f"4. Executive Case Study: {topic.suggested_case_study}",
        block_type="case_study",
        case_company=topic.suggested_case_study.split(":")[0],
        content_markdown=(
            f"**Context & Dilemma**: In this case study tailored for management students, "
            f"we analyze the strategic trade-offs faced by {topic.suggested_case_study}.\n\n"
            f"**Market Dynamics**: {topic.relevance_summary}\n\n"
            f"**Key Strategic Decision**: How can leadership balance aggressive market share expansion with positive unit economics "
            f"amid intense competitive rivalry in high-density urban corridors?"
        ),
    )

    # Formative Business Quiz
    quizzes = [
        QuizQuestion(
            question=f"In the context of {topic.title}, what is the primary business metric indicating sustainable competitive advantage?",
            options=[
                QuizOption(
                    text="Unit Contribution Margin II turning positive while preserving customer retention",
                    is_correct=True,
                    explanation="In modern platform and operational businesses, sustainable positive contribution margins after marketing and delivery reflect true economic moats.",
                ),
                QuizOption(
                    text="Gross Merchandise Value (GMV) subsidized purely by external venture capital burn",
                    is_correct=False,
                    explanation="Subsidized GMV without healthy unit economics leads to insolvency once capital tightens.",
                ),
                QuizOption(
                    text="Eliminating all human workforce dependencies regardless of customer friction",
                    is_correct=False,
                    explanation="Operational efficiency must be balanced with service quality and consumer trust.",
                ),
            ],
            hint="Differentiate between top-line subsidized vanity metrics and bottom-line economic value.",
            points=10,
            step_by_step_solution=(
                "1. Scrutinize the formula: Contribution Margin = Revenue - Variable Costs.\n"
                "2. When LTV:CAC exceeds 3.0 and Contribution Margin II is positive, the platform achieves operational profitability.\n"
                "3. Option A represents the foundational tenet of modern management strategy."
            ),
        )
    ]

    return LessonPage(
        title=f"Module {week_num}: {topic.title}",
        estimated_read_time_minutes=20,
        learning_objectives=[
            topic.target_learning_outcome,
            f"Analyze the strategic implications of {topic.suggested_case_study}.",
            f"Assess how Bangalore and Indian market conditions shape {topic.discipline}.",
        ],
        blocks=[
            LessonBlock(
                title=f"1. Strategic Overview & Industry Trends",
                block_type="concept",
                content_markdown=(
                    f"**Source Reference**: *{topic.source_website}* ([Read Source Article]({topic.source_url}))\n\n"
                    f"{topic.relevance_summary}\n\n"
                    f"**Regional & Industry Context**: {topic.why_relevant_for_bangalore_students}"
                ),
                applied_example=(
                    f"**Real-World Case Illustration ({topic.title})**:\n"
                    f"In {topic.suggested_case_study}, leadership confronted margin compression by re-evaluating distribution channel ROI, "
                    "shifting resource allocation towards higher-margin direct customer relationships while preserving operational liquidity."
                ),
            ),
            math_block,
            diagram_block,
            case_block,
        ],
        flashcards=[
            Flashcard(
                front=f"Core Insight: {topic.title}",
                back=topic.target_learning_outcome,
                category=topic.discipline
            ),
            Flashcard(
                front="Hurdle Condition for Sustainable Scale",
                back="Customer Lifetime Value (LTV) divided by Customer Acquisition Cost (CAC) must be >= 3.0x to avoid capital depletion.",
                category="Unit Economics"
            ),
            Flashcard(
                front=f"Case Benchmark: {topic.suggested_case_study.split(':')[0]}",
                back=topic.relevance_summary,
                category="Case Analysis"
            )
        ],
        practice_problems=quizzes,
        further_readings=[
            ResourceLink(
                title=f"{topic.source_website}: {topic.title}",
                url=topic.source_url,
                type="case_study",
                source_name=topic.source_website,
                description="Comprehensive industry briefing and management insights.",
            )
        ],
    )
