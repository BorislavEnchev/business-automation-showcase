"""
AutoMate — LangGraph Conditional Routing

Demonstrates how the pipeline branches based on process type,
extraction results, QA validation, and review outcomes.
"""

from langgraph.graph import END, START, StateGraph


# ── Conditional Routing Functions ──
# Each function receives the current state and returns the name of
# the next node to execute. LangGraph uses the return value to follow
# the correct edge in the graph.

def route_after_start(state: dict) -> str:
    """
    START route depends on process_type:
    - "personal" → extractor node
    - "company"  → scraper node (skip extraction)
    - "full"     → extractor node
    """
    if state.get("process_type") == "company":
        return "scraper"
    return "extractor"


def route_after_extraction(state: dict) -> str:
    """
    After extraction:
    - Success → verification_gate (human review)
    - Failure → END
    """
    if state.get("status") == "failed":
        return END
    return "verification_gate"


def route_after_verification(state: dict) -> str:
    """
    After human verification:
    - Personal-only → END (no company lookup needed)
    - Full pipeline → scraper
    """
    if state.get("process_type") == "personal":
        return END
    return "scraper"


def route_after_scraping(state: dict) -> str:
    """
    After company registry lookup:
    - Company-only or failure → END
    - Full pipeline → qa_inspector
    """
    if state.get("status") == "failed" or state.get("process_type") == "company":
        return END
    return "qa_inspector"


def route_after_qa(state: dict) -> str:
    """
    After QA cross-check:
    - Passed → scribe (document generation)
    - Failed with retries remaining → scraper (retry)
    - Failed permanently → END
    """
    if state.get("qa_passed"):
        return "scribe"
    if state.get("status") == "failed":
        return END
    return "scraper"  # Retry


def route_after_review(state: dict) -> str:
    """
    After final review:
    - Passed → END
    - Failed → scribe (regenerate)
    """
    if state.get("review_passed"):
        return END
    return "scribe"


# ── Graph Construction ──

def build_graph() -> StateGraph:
    """
    Construct the multi-agent pipeline graph.
    
    Flow:
        START ──► extractor ──► verification_gate ──► scraper
              ──► qa_inspector ──► scribe ──► final_review ──► END
    
    With conditional edges for:
    - Extraction failure → immediate END
    - QA failure → scraper retry or permanent END
    - Review failure → scribe regeneration
    - Process type shortcuts (personal-only, company-only)
    """
    
    graph = StateGraph(GraphState)
    
    # ── Add agent nodes ──
    graph.add_node("extractor", extractor_node)
    graph.add_node("verification_gate", verification_gate_node)
    graph.add_node("scraper", scraper_node)
    graph.add_node("qa_inspector", qa_inspector_node)
    graph.add_node("scribe", scribe_node)
    graph.add_node("final_review", final_review_node)
    
    # ── Define conditional edges ──
    graph.add_conditional_edges(START, route_after_start)
    graph.add_conditional_edges("extractor", route_after_extraction)
    graph.add_conditional_edges("verification_gate", route_after_verification)
    graph.add_conditional_edges("scraper", route_after_scraping)
    graph.add_conditional_edges("qa_inspector", route_after_qa)
    
    # ── Fixed edges ──
    graph.add_edge("scribe", "final_review")
    
    # ── Conditional end ──
    graph.add_conditional_edges("final_review", route_after_review)
    
    return graph


"""
Routing Visualization:

                    ┌──────────┐
                    │  START   │
                    └────┬─────┘
                         │ (process_type)
              ┌──────────┼──────────┐
              │          │          │
         personal     full      company
              │          │          │
              ▼          ▼          ▼
         extractor   extractor   scraper
              │          │          │
              │          ▼          │
              │   verification      │
              │     gate            │
              │          │          │
              └──────────┤          │
                    (personal)      │
                         │          │
                         ▼          │
                     scraper ◄──────┘
                         │
                         ▼
                    qa_inspector
                     │        │
                (pass)     (fail)
                     │        │
                     ▼        ▼
                  scribe   scraper (retry)
                     │
                     ▼
               final_review
                     │
                     ▼
                    END
"""
