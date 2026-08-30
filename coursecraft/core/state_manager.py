"""
state_manager.py
Handles loading, saving, and generating default starter academic course portals.
Specifically tailored for Management Students (MBA/BBA programs).
"""

import json
from pathlib import Path
from typing import Optional
from coursecraft.core.models import (
    CoursePortal,
    CourseWeek,
    LessonPage,
    LessonBlock,
    QuizQuestion,
    QuizOption,
    ResourceLink,
    Flashcard,
)


def create_sample_course() -> CoursePortal:
    """Generates an executive MBA/BBA course in Strategic Management."""
    # Week 1
    w1_quiz = QuizQuestion(
        question="In platform economics, what distinguishes a two-sided marketplace (e.g. Swiggy/Zomato) from a traditional pipeline business?",
        question_type="multiple_choice",
        options=[
            QuizOption(
                text="Cross-side network effects where value for consumers increases as restaurant/merchant density grows",
                is_correct=True,
                explanation="Two-sided platforms derive defensibility through indirect (cross-side) network effects rather than physical asset ownership.",
            ),
            QuizOption(
                text="Direct linear ownership of raw ingredient manufacturing and physical kitchens",
                is_correct=False,
                explanation="Pipeline businesses rely on vertical linear supply chains; platforms coordinate third parties.",
            ),
            QuizOption(
                text="Complete immunity to regulatory interventions and municipal licensing",
                is_correct=False,
                explanation="Platforms remain heavily subject to municipal and labor regulations.",
            ),
        ],
        hint="Consider the dynamic between diner availability and restaurant participation.",
        points=10,
        step_by_step_solution=(
            "1. Pipeline firms produce goods linearly (Supplier -> Manufacturer -> Distributor -> Consumer).\n"
            "2. Platforms create value by orchestrating interactions between two distinct user groups.\n"
            "3. More restaurants attract more diners (direct effect), and more diners attract more restaurants (cross-side network effect)."
        ),
    )

    w1_blocks = [
        LessonBlock(
            title="1. Foundations of Platform Strategy & Ecosystem Competition",
            block_type="concept",
            content_markdown=(
                "Modern management in high-growth markets like India has fundamentally shifted from traditional "
                "Porterian value chains to multi-sided platform ecosystems. In Bengaluru's competitive landscape, "
                "firms like Swiggy, Zepto, and Flipkart win not through physical assets, but through network density, "
                "data feedback loops, and frictionless participant onboarding."
            ),
            applied_example=(
                "**Swiggy's Cross-Subsidization in Bangalore**:\n"
                "In Bengaluru's Koramangala and Indiranagar corridors, Swiggy subsidizes consumer delivery fees during non-peak lunch hours (11:00 AM – 12:30 PM) to generate consistent order volume for partnered cloud kitchens. In return, Swiggy charges restaurants a 22–26% commission on order value, using corporate take-rates to offset lower delivery fees."
            ),
        ),
        LessonBlock(
            title="2. Unit Economics & Contribution Margin Modeling",
            block_type="proof_math",
            content_markdown=(
                "For hyper-local delivery platforms, sustaining investor returns requires rigorous contribution margin analysis:"
            ),
            applied_example=(
                "**Blinkit vs. Zepto Dark Store Economics**:\n"
                "A dark store in HSR Layout Bangalore handling 1,200 daily orders achieves Contribution Margin II profitability once Average Order Value (AOV) crosses ₹480 and rider batching reaches 1.6 orders per dispatch."
            ),
            latex_formulas=[
                r"\text{Contribution Margin II} = \text{AOV} \times \text{Take Rate \%} + \text{Delivery Fee} - (\text{Rider Payout} + \text{Packaging} + \text{Payment Gateway})",
                r"\text{Unit Breakeven}: \quad \frac{\text{Customer Lifetime Value (LTV)}}{\text{Customer Acquisition Cost (CAC)}} \ge 3.5",
            ],
        ),
        LessonBlock(
            title="3. Platform Market Dynamics",
            block_type="diagram",
            content_markdown="Cross-side network interaction between consumers and merchants:",
            mermaid_diagram="""graph LR
    subgraph Diners ["Bangalore Urban Consumers"]
        C1["Household Customers"]
        C2["Corporate Offices"]
    end
    subgraph PlatformLayer ["Digital Orchestration Layer"]
        Algo["Dynamic Pricing & Routing Engine"]
        Payment["UPI & Gateway Settlement"]
    end
    subgraph Merchants ["Supply Side Partners"]
        R1["Cloud Kitchens"]
        R2["FMCG Brands & Dark Stores"]
    end
    Diners <--> PlatformLayer
    PlatformLayer <--> Merchants
""",
        ),
        LessonBlock(
            title="4. Executive Case Study: Swiggy vs. Zomato vs. Blinkit in Bangalore",
            block_type="case_study",
            case_company="Swiggy & Zomato",
            content_markdown=(
                "**Executive Management Field Study**:\n\n"
                "Bengaluru represents India's highest-density food delivery and quick-commerce testing market. "
                "With Zomato acquiring Blinkit and Swiggy expanding Instamart, students analyze how dark store "
                "real estate in neighborhoods like Indiranagar, Koramangala, and Yelahanka achieves profitability "
                "despite steep rider incentives and fluctuating weather conditions."
            ),
        ),
    ]

    lesson1 = LessonPage(
        title="Lecture 1: Platform Ecosystems & Unit Economics in Emerging Markets",
        estimated_read_time_minutes=25,
        learning_objectives=[
            "Evaluate two-sided network effects in digital platforms.",
            "Calculate Contribution Margin II and LTV:CAC ratios for consumer internet firms.",
            "Deconstruct the competitive rivalry between Swiggy and Zomato in Bengaluru.",
        ],
        blocks=w1_blocks,
        flashcards=[
            Flashcard(
                front="Two-Sided Network Effects",
                back="An economic dynamic where value increases for one user segment (e.g. diners) as the number and density of participants on the other side (e.g. restaurants) expands.",
                category="Platform Economics"
            ),
            Flashcard(
                front="Contribution Margin II Formula",
                back="Contribution Margin II = (AOV × Take Rate %) + Delivery Fees - (Rider Payout + Packaging + Payment Gateway Charges). It measures per-order operational viability before fixed corporate overhead.",
                category="Managerial Accounting"
            ),
            Flashcard(
                front="LTV : CAC Benchmark",
                back="Customer Lifetime Value (LTV) divided by Customer Acquisition Cost (CAC) should exceed 3.0x for sustainable consumer internet businesses; below 1.0x indicates value destruction.",
                category="Unit Economics"
            ),
            Flashcard(
                front="Cross-Subsidization Strategy",
                back="Pricing practice where profits from high-margin transactions (e.g. premium restaurant delivery or sponsored ads) offset losses in customer acquisition or hyper-local delivery.",
                category="Pricing Strategy"
            )
        ],
        practice_problems=[w1_quiz],
        further_readings=[
            ResourceLink(
                title="Pipelines, Platforms, and the New Rules of Strategy (Harvard Business Review)",
                url="https://hbr.org/2016/04/pipelines-platforms-and-the-new-rules-of-strategy",
                type="case_study",
                source_name="Harvard Business Review",
                description="Seminal HBR article on the transition from traditional value chains to platforms.",
            ),
            ResourceLink(
                title="Quick Commerce Boom in Indian Metros (The Economic Times)",
                url="https://economictimes.indiatimes.com",
                type="reading",
                source_name="The Economic Times",
                description="Analysis of 10-minute grocery delivery economics and logistics.",
            ),
        ],
    )

    week1 = CourseWeek(
        week_number=1,
        title="Week 1: Strategic Foundations of Digital Platforms & Unit Economics",
        theme="Platform Competition & Consumer Economics",
        dates="Term Week 1",
        overview="Introduction to multi-sided platforms, cross-side network effects, and unit economics modeling in Indian consumer tech.",
        lessons=[lesson1],
        assignments=["HBR Case Analysis: Swiggy's Diversification into Instamart & Dineout"],
        readings=["HBR: Pipelines to Platforms", "Economic Times Quick Commerce Briefing"],
    )

    # Week 2
    w2_quiz = QuizQuestion(
        question="How does India's Digital Public Infrastructure (UPI and ONDC) alter the competitive moat of proprietary tech giants?",
        question_type="multiple_choice",
        options=[
            QuizOption(
                text="By unbundling discovery, payment, and fulfillment into open protocols, lowering entry barriers for smaller merchants",
                is_correct=True,
                explanation="DPI commoditizes the rails (payment and discovery), preventing single platforms from monopolizing transactions.",
            ),
            QuizOption(
                text="By mandating that all software must be closed-source and owned by foreign conglomerates",
                is_correct=False,
                explanation="DPI is open-source and built on public rails.",
            ),
            QuizOption(
                text="By eliminating all demand for digital credit and working capital",
                is_correct=False,
                explanation="DPI actually expands digital lending access through Account Aggregators.",
            ),
        ],
        hint="Think about what happens when rails (like UPI) are public rather than owned by a single private app.",
        points=10,
        step_by_step_solution="DPI decouples transactions from walled gardens, shifting competitive advantage toward superior customer service and supply density.",
    )

    w2_blocks = [
        LessonBlock(
            title="1. India Stack: UPI, Account Aggregator & ONDC Architecture",
            block_type="concept",
            content_markdown=(
                "India Stack has emerged as a global benchmark for digital financial inclusion. "
                "By decoupling payment identity from proprietary bank interfaces, Unified Payments Interface (UPI) "
                "processes over 14 billion monthly transactions. For management students, the strategic question is "
                "how fintechs (PhonePe, CRED, Razorpay) build sustainable monetization when basic payment rail fees are zero."
            ),
        ),
        LessonBlock(
            title="2. Fintech Monetization & Risk Valuation",
            block_type="proof_math",
            content_markdown=(
                "Fintech lending margins are governed by risk-adjusted return on capital (RAROC):"
            ),
            latex_formulas=[
                r"\text{Net Interest Margin (NIM)} = \frac{\text{Investment Returns} - \text{Cost of Funds}}{\text{Average Earning Assets}}",
                r"\text{Credit Loss Adjusted Spread} = \text{APR} - (\text{Cost of Funds} + \text{Operating Expense} + \text{Expected Default Loss})",
            ],
        ),
        LessonBlock(
            title="3. Open Network for Digital Commerce (ONDC) Unbundled Flow",
            block_type="diagram",
            content_markdown="Buyer App to Seller App protocol communication:",
            mermaid_diagram="""sequenceDiagram
    autonumber
    actor Consumer as Bangalore Consumer
    participant BuyerApp as Buyer App (Pincode / Paytm)
    participant Gateway as ONDC Open Gateway
    participant SellerApp as Seller App (Kirana Partner)
    participant Logistics as Logistics Provider (Shadowfax)

    Consumer->>BuyerApp: Searches for local groceries
    BuyerApp->>Gateway: Broadcasts open search request
    Gateway->>SellerApp: Matches local neighborhood stores
    SellerApp-->>BuyerApp: Returns catalog, pricing and inventory
    Consumer->>BuyerApp: Places order and pays via UPI
    BuyerApp->>Logistics: Allocates last-mile delivery partner
    Logistics-->>Consumer: Dispatches order to customer
""",
        ),
    ]

    lesson2 = LessonPage(
        title="Lecture 2: Fintech Disruption, DPI & Digital Lending Models",
        estimated_read_time_minutes=30,
        learning_objectives=[
            "Analyze the strategic business models of PhonePe, CRED, and Razorpay.",
            "Formulate credit risk spreads and calculate Net Interest Margins (NIM).",
            "Evaluate ONDC's threat to incumbent e-commerce monopolies.",
        ],
        blocks=w2_blocks,
        flashcards=[
            Flashcard(
                front="Digital Public Infrastructure (DPI)",
                back="Open, interoperable digital rails (e.g. UPI, Aadhaar, ONDC) that separate payment and identity verification from proprietary apps, preventing walled-garden monopolies.",
                category="Fintech Rails"
            ),
            Flashcard(
                front="Net Interest Margin (NIM)",
                back="NIM = (Investment Returns - Cost of Funds) / Average Earning Assets. Key profitability metric for NBFCs and digital lending apps.",
                category="Financial Metrics"
            ),
            Flashcard(
                front="Account Aggregator (AA) Framework",
                back="RBI-regulated financial data sharing protocol enabling consent-based, encrypted sharing of financial statements between banks and fintech lenders for instant digital underwriting.",
                category="Regulatory Tech"
            ),
            Flashcard(
                front="Unbundled Commerce Architecture (ONDC)",
                back="Decoupling discovery (Buyer App), order matching (Gateway), merchant inventory (Seller App), and last-mile delivery (Logistics Partner) across open protocols.",
                category="Platform Strategy"
            )
        ],
        practice_problems=[w2_quiz],
        further_readings=[
            ResourceLink(
                title="Fintech Revolution in India: The Public Rail Paradigm (McKinsey Insights)",
                url="https://www.mckinsey.com",
                type="case_study",
                source_name="McKinsey Insights",
                description="Strategic analysis of India's DPI and fintech innovation.",
            )
        ],
    )

    week2 = CourseWeek(
        week_number=2,
        title="Week 2: Digital Public Infrastructure, Fintech & ONDC",
        theme="Financial Technology & Open Rail Business Models",
        dates="Term Week 2",
        overview="Examination of UPI, digital lending, ONDC, and fintech unit economics in Bangalore's startup corridor.",
        lessons=[lesson2],
        assignments=["Valuation Exercise: Credit Risk Spreads for MSME Digital Lending"],
        readings=["McKinsey Insights on India Fintech", "RBI Whitepaper on DPI"],
    )

    return CoursePortal(
        course_code="MBA-602",
        course_title="Strategic Management & Digital Business Models",
        university="Department of Management Studies, School of Business",
        professor_name="Prof. Rajesh Sharma, Ph.D.",
        semester="Trimester III / Academic Year 2026-27",
        office_hours="Monday & Wednesday 2:30 PM - 4:30 PM (Management Block, Cabin 304)",
        prerequisites=[
            "Principles of Management",
            "Managerial Economics",
            "Business Analytics & Statistics",
        ],
        syllabus_summary=(
            "Designed specifically for Management Students (MBA/BBA), this course "
            "bridges foundational business strategy with digital platform ecosystems, India's thriving startup and "
            "fintech ecosystem, AI-driven corporate transformation, and real-world Harvard Business Review style case studies."
        ),
        grading_policy={
            "HBR Case Study Analyses (3x)": "30%",
            "Mid-Trimester Examination": "20%",
            "Corporate Industry Capstone Project": "35%",
            "Classroom Discussion & Quizzes": "15%",
        },
        weeks=[week1, week2],
        theme_palette="oxford_navy",
    )


def save_course_to_file(course: CoursePortal, filepath: str | Path) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(course.model_dump(), f, indent=2)


def load_course_from_file(filepath: str | Path) -> Optional[CoursePortal]:
    path = Path(filepath)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return CoursePortal.model_validate(data)
