"""
AutoMate — Shared Graph State (TypedDict)

This TypedDict is the contract every agent node reads from and writes to.
It flows through the entire LangGraph pipeline and provides full traceability.
"""

from typing import TypedDict, Optional, Any, List


class GraphState(TypedDict, total=False):
    """
    The shared state object passed between all nodes in the LangGraph.
    
    Every agent reads from and writes to this state, enabling:
    - Full audit trail with per-agent logs
    - Confidence scoring at each step
    - Error accumulation without state corruption
    - Retry counts for automatic recovery
    """
    
    # ── Identity ──
    process_id: str                          # Unique run identifier
    process_type: str                        # "personal" | "company" | "full"
    
    # ── Progress ──
    status: str                              # Current pipeline stage
    current_agent: Optional[str]             # Which agent is executing
    
    # ── Data payloads ──
    person: Optional[dict[str, Any]]         # Validated PersonSchema as dict
    company: Optional[dict[str, Any]]        # Validated CompanySchema as dict
    
    # ── Human-in-the-loop ──
    is_verified: bool                        # Has extracted data been approved?
    
    # ── Input ──
    input_data: Optional[str]                # Base64 image or JSON string
    input_type: Optional[str]                # "image" | "json"
    company_number: Optional[str]            # Registry ID to look up
    
    # ── Output ──
    output_path: Optional[str]               # Path to generated document bundle
    
    # ── Traceability ──
    logs: list[dict[str, Any]]               # Ordered agent audit log
    errors: list[str]                        # Accumulated error messages
    
    # ── QA / Retry ──
    qa_passed: Optional[bool]                # Did QA cross-check pass?
    review_passed: Optional[bool]            # Did final review pass?
    retry_count: int                         # Current retry attempt
    max_retries: int                         # Max retries before failing


"""
Agent Log Entry Structure

Each log entry captures a single action performed by an agent:
{
    "agent_name": "ExtractorAgent",          # Which agent acted
    "action": "Extracted person data...",    # What was done
    "confidence_score": 0.92,                # How confident (0.0 - 1.0)
    "timestamp": "2024-01-15T10:30:00Z",     # When it happened
    "details": { "mode": "vision", ... }     # Optional metadata
}
"""
