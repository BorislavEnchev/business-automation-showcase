"""
AutoMate — LangGraph Agent Node Pattern (Extractor)

Demonstrates the standard agent node structure used throughout the pipeline.

Every agent follows this pattern:
1. Read state
2. Execute domain logic
3. Return state updates
4. Log everything with confidence scores
"""

import logging
from datetime import datetime
from typing import Any

# Agent nodes are simple async functions that receive state and return state updates.
# They don't need to inherit from any base class or implement any interface.
# LangGraph merges the returned dict into the shared GraphState.

logger = logging.getLogger(__name__)


# Log entries follow a standardized format for full traceability
def _build_log_entry(
    agent_name: str,
    action: str,
    confidence: float,
    details: dict | None = None,
) -> dict[str, Any]:
    """
    Create a structured log entry for the audit trail.
    
    Every agent action is recorded with:
    - agent_name: which agent acted
    - action: human-readable description
    - confidence_score: how reliable the result is (0.0 - 1.0)
    - timestamp: when it happened
    - details: optional metadata for debugging
    """
    return {
        "agent_name": agent_name,
        "action": action,
        "confidence_score": confidence,
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {},
    }


async def extractor_node(state: dict[str, Any]) -> dict[str, Any]:
    """
    LangGraph Node: Extractor Agent
    
    Reads the input data from state, extracts structured person information,
    and returns the updated state with person data and confidence score.
    
    Args:
        state: The current GraphState dict
        
    Returns:
        Dict of state fields to update (LangGraph merges these into state)
    """
    logger.info("ExtractorAgent: Starting extraction")
    
    # ── 1. Read state ──
    input_type = state.get("input_type", "json")
    input_data = state.get("input_data", "")
    logs = list(state.get("logs", []))
    errors = list(state.get("errors", []))
    
    try:
        # ── 2. Execute domain logic ──
        if input_type == "image":
            person_data, confidence = await extract_from_image(input_data)
            logs.append(_build_log_entry(
                agent_name="ExtractorAgent",
                action="Extracted person data from passport/ID via vision model",
                confidence=confidence,
                details={"mode": "vision", "source": "image"},
            ))
        else:
            person_data, confidence = await extract_from_json(input_data)
            logs.append(_build_log_entry(
                agent_name="ExtractorAgent",
                action="Validated person data from manual JSON input",
                confidence=confidence,
                details={"mode": "manual"},
            ))
        
        logger.info(f"ExtractorAgent: Extraction complete (confidence={confidence})")
        
        # ── 3. Return state updates ──
        return {
            "person": person_data,
            "status": "awaiting_verification",  # Next stage
            "current_agent": "verification_gate",
            "logs": logs,
            "errors": errors,
        }
        
    except Exception as e:
        # ── Error handling: record and fail gracefully ──
        error_msg = f"ExtractorAgent: Extraction failed — {str(e)}"
        logger.error(error_msg, exc_info=True)
        errors.append(error_msg)
        logs.append(_build_log_entry(
            agent_name="ExtractorAgent",
            action=f"Extraction failed: {type(e).__name__}",
            confidence=0.0,
            details={"error": str(e)},
        ))
        return {
            "status": "failed",
            "current_agent": None,
            "logs": logs,
            "errors": errors,
        }


"""
Key Patterns:

1. State is a plain dict — no class instances to serialize
2. Errors are accumulated, not thrown — one failure doesn't lose state
3. Logs provide a complete audit trail for debugging
4. Status transitions make the graph's progress explicit
5. Every agent returns the subset of fields it changed
"""
