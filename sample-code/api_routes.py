"""
AutoMate — Clean REST API Route Design

Demonstrates FastAPI patterns used throughout the codebase:
- Async endpoints with dependency injection
- Pydantic request/response models
- Proper HTTP status codes
- Error handling with structured responses
"""

import uuid
import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

# ── Pydantic Request/Response Models ──

from pydantic import BaseModel, Field, StrictStr, field_validator


class StartProcessRequest(BaseModel):
    """Request body for starting a new automation process."""
    
    input_type: StrictStr = Field(
        default="json",
        description="'image' for passport scan, 'json' for manual input",
    )
    input_data: StrictStr = Field(
        default="",
        description="Base64-encoded image or JSON string",
    )
    company_number: StrictStr | None = Field(
        None,
        description="Company registration number (EIK/UIC) for registry lookup",
    )
    process_type: StrictStr = Field(
        default="full",
        description="'full', 'personal', or 'company'",
    )

    @field_validator("input_type")
    @classmethod
    def validate_input_type(cls, v: str) -> str:
        if v not in ("image", "json"):
            raise ValueError("input_type must be 'image' or 'json'")
        return v


class ProcessStatusResponse(BaseModel):
    """Response returned when checking process status."""
    
    process_id: str
    status: str                       # Current pipeline stage
    current_agent: str | None = None  # Currently executing agent
    person: dict[str, Any] | None = None
    company: dict[str, Any] | None = None
    is_verified: bool = False
    logs: list[dict[str, Any]] = []
    errors: list[str] = []


# ── API Router ──

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/start",
    response_model=ProcessStatusResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start a new automation process",
)
async def start_process(
    request: StartProcessRequest,
    session=Depends(get_async_session),  # Injected dependency
):
    """
    Initialize a new multi-agent pipeline run.
    
    Accepts passport image data or manual JSON, optionally a company
    registration number, and returns immediately with a process_id
    for status polling.
    """
    process_id = str(uuid.uuid4())
    
    # Build initial graph state
    initial_state = {
        "process_id": process_id,
        "status": "extracting",
        "current_agent": "extractor",
        "input_type": request.input_type,
        "input_data": request.input_data,
        "company_number": request.company_number,
        "process_type": request.process_type,
        "is_verified": False,
        "person": None,
        "company": None,
        "logs": [],
        "errors": [],
        "qa_passed": None,
        "review_passed": None,
        "retry_count": 0,
        "max_retries": 3,
    }
    
    try:
        # Execute the LangGraph pipeline
        graph_config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        result = await compiled_graph.ainvoke(initial_state, config=graph_config)
        
        return ProcessStatusResponse(
            process_id=process_id,
            status=result.get("status", "pending"),
            current_agent=result.get("current_agent"),
            person=result.get("person"),
            company=result.get("company"),
            is_verified=result.get("is_verified", False),
            logs=result.get("logs", []),
            errors=result.get("errors", []),
        )
        
    except Exception as e:
        logger.error(f"Failed to start process: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start process: {str(e)}",
        )


@router.get(
    "/{process_id}/status",
    response_model=ProcessStatusResponse,
    summary="Check process status for polling",
)
async def get_process_status(
    process_id: str,
    session=Depends(get_async_session),
):
    """
    Retrieve the current state of a running or completed process.
    
    Used by the frontend for polling-based status updates.
    """
    record = await get_process_record(session, process_id)
    
    return ProcessStatusResponse(
        process_id=record.process_id,
        status=record.status,
        current_agent=record.current_agent,
        person=record.get_person(),
        company=record.get_company(),
        is_verified=record.is_verified,
        logs=record.get_logs(),
        errors=record.get_errors(),
    )


@router.post(
    "/{process_id}/verify",
    response_model=ProcessStatusResponse,
    summary="Verify extracted data and resume pipeline",
)
async def verify_process(
    process_id: str,
    request: VerifyRequest,  # Contains is_verified + optional corrections
    session=Depends(get_async_session),
):
    """
    Human-in-the-loop verification endpoint.
    
    After extraction, the pipeline pauses. Call this to approve
    or reject the extracted data and resume execution.
    """
    record = await get_process_record(session, process_id)
    
    if record.status != "awaiting_verification":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Process is in '{record.status}' state, not awaiting verification",
        )
    
    # Resume the graph with the verification decision
    resume_input = {
        "is_verified": request.is_verified,
        "corrections": request.corrections,
    }
    
    result = await compiled_graph.ainvoke(
        Command(resume=resume_input),
        config={"configurable": {"thread_id": record.thread_id}},
    )
    
    return ProcessStatusResponse(
        process_id=process_id,
        status=result.get("status", "pending"),
        current_agent=result.get("current_agent"),
        ...
    )


@router.post(
    "/{process_id}/cancel",
    response_model=ProcessStatusResponse,
    summary="Cancel a running process",
)
async def cancel_process(
    process_id: str,
    session=Depends(get_async_session),
):
    """Cancel an active extraction process and clean up resources."""
    # Cancel the background task if running
    task = active_tasks.get(process_id)
    if task and not task.done():
        task.cancel()
    
    # Update database state
    return ProcessStatusResponse(
        process_id=process_id,
        status="canceled",
        ...
    )


"""
API Design Principles:

1. Consistent prefix: All routes under /api/v1/
2. Proper HTTP methods: POST for actions, GET for queries
3. Correct status codes: 201 for creation, 409 for conflicts
4. Pydantic everywhere: Request and response models at every boundary
5. Dependency injection: DB sessions injected via Depends()
6. Structured errors: Consistent error format with detail field
"""
