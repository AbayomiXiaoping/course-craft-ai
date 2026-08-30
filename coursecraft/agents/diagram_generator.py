"""
diagram_generator.py
Generates valid, syntax-clean Mermaid.js diagrams to visualize strategic management models,
platform economics, value chains, and unit economics decision trees for MBA students.
"""

import re
from typing import Optional
from coursecraft.agents.llm_orchestrator import generate_structured_synthesis


def sanitize_mermaid_label(text: str) -> str:
    """Removes characters that break Mermaid.js parsing and limits label length."""
    if not text:
        return "Concept Analysis"
    # Remove quotes, parentheses, brackets, colons, slashes, and dashes that break Mermaid nodes
    clean = re.sub(r'[\"\'\`\(\)\[\]\{\}\<\>\:\/\—\-]', ' ', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:50]


def generate_mermaid_diagram(topic: str, description: str) -> str:
    """Generates a valid, beautifully structured Mermaid.js diagram definition for a management concept."""
    system_prompt = (
        "You are an academic management and business strategy visualizer for graduate MBA students. "
        "Create a clean, valid Mermaid.js diagram (e.g. flowchart TD, graph LR, or sequenceDiagram). "
        "CRITICAL SYNTAX RULES FOR MERMAID:\n"
        "1. ALL node labels MUST be enclosed in double quotes: NodeA[\"Text Here\"]\n"
        "2. Do NOT use colons, slashes, or special characters outside of double quotes.\n"
        "3. Return ONLY the raw Mermaid code inside ```mermaid ``` fences without any explanations."
    )
    user_prompt = f"Topic: {topic}\nDescription: {description[:1000]}"

    raw = generate_structured_synthesis(system_prompt, user_prompt, max_tokens=600)
    if raw and "```mermaid" in raw:
        code = raw.split("```mermaid")[1].split("```")[0].strip()
        # Verify valid header
        if any(code.startswith(k) for k in ["flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram"]):
            sg_count = len(re.findall(r"\bsubgraph\b", code))
            end_count = len(re.findall(r"\bend\b", code))
            if sg_count > end_count:
                code += "\n" + ("    end\n" * (sg_count - end_count))
            lines = [l.strip() for l in code.strip().split("\n") if l.strip()]
            # Must have at least 3 lines and valid terminal
            if len(lines) >= 3 and not lines[-1].startswith("subgraph"):
                return code

    # Deterministic fallback diagrams tailored for Management with 100% valid quotes
    clean_t = sanitize_mermaid_label(topic)
    topic_lower = topic.lower()

    if any(k in topic_lower for k in ["human resource", "hrm", "talent", "employee", "workforce", "turnover", "recruitment", "labor"]):
        return f"""flowchart TD
    Strategy["Corporate Business Strategy & Growth"] --> HRPlan["Strategic Workforce Planning & Competency Mapping"]
    HRPlan --> TalentAcq["Targeted Talent Acquisition & Employer Branding"]
    HRPlan --> PerfDev["Continuous Performance Appraisal & Upskilling"]
    TalentAcq --> Retain["Total Rewards, Incentive Banding & Retention"]
    PerfDev --> Retain
    Retain --> BusinessROI["Sustained Competitive Advantage & Higher Human Capital ROI"]
"""

    if any(k in topic_lower for k in ["platform", "network", "ecosystem", "marketplace", "swiggy", "zomato", "blinkit", "zepto"]):
        return f"""graph LR
    subgraph Diners ["Demand Side: Urban Consumers"]
        C1["Household Customers"]
        C2["Corporate Offices"]
    end
    subgraph PlatformLayer ["Digital Orchestration Engine"]
        Algo["Dynamic Pricing & Routing"]
        Settle["UPI & Gateway Settlement"]
    end
    subgraph SupplySide ["Supply Side: Partner Network"]
        R1["Cloud Kitchens & Restaurants"]
        R2["Dark Stores & Quick Commerce Hubs"]
    end
    Diners <--> PlatformLayer
    PlatformLayer <--> SupplySide
"""

    if any(k in topic_lower for k in ["fintech", "payment", "upi", "banking", "lending", "credit", "ondc"]):
        return f"""sequenceDiagram
    autonumber
    actor Customer as User / Borrower
    participant App as Fintech Interface
    participant Rail as UPI / DPI Gateway
    participant Bank as Partner NBFC / Bank
    Customer->>App: Submits Transaction / Credit Request
    App->>Rail: Validates Digital Identity & Consent
    Rail->>Bank: Verifies Real-Time Balances & Risk
    Bank-->>App: Approves Instant Settlement
    App-->>Customer: Transaction Confirmed
"""

    # Strategic Decision Tree Default (100% quoted nodes for syntax safety)
    return f"""flowchart TD
    Start["Strategic Context & Market Entry"] --> Step1["Deconstruct: {clean_t}"]
    Step1 --> Step2["Assess Unit Economics & CAC vs LTV"]
    Step2 --> Step3{{"Sustained Contribution Margin II >= 0?"}}
    Step3 -- "Yes (Viable)" --> Scale["Scale Operations & Expand Moat"]
    Step3 -- "No (Deficit)" --> Optimize["Re-engineer Pricing & Operating Costs"]
"""
