"""
AutoMate — Pydantic v2 Validation Schema (Person)

Demonstrates strict-typed data contracts with runtime validation,
custom field validators, and comprehensive error messaging.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, StrictStr, field_validator


class PersonSchema(BaseModel):
    """
    Normalized data extracted from a passport or identity document.
    
    Every field is validated at runtime — dates must be in YYYY-MM-DD
    format, passport numbers must be alphanumeric, and required fields
    cannot be empty.
    """
    
    # ── Personal Identification ──
    first_name: StrictStr = Field(
        ...,
        description="First name as shown on the document",
        min_length=1,
    )
    middle_name: Optional[StrictStr] = Field(
        None,
        description="Middle name, if present on the document",
    )
    last_name: StrictStr = Field(
        ...,
        description="Last name as shown on the document",
        min_length=1,
    )
    
    # ── English/Latin Name Variants ──
    first_name_en: Optional[StrictStr] = Field(
        None,
        description="First name in Latin script exactly as on document",
    )
    middle_name_en: Optional[StrictStr] = Field(
        None,
        description="Middle name in Latin script, if present",
    )
    last_name_en: Optional[StrictStr] = Field(
        None,
        description="Last name in Latin script exactly as on document",
    )
    
    # ── Biographical Data ──
    date_of_birth: StrictStr = Field(
        ...,
        description="Date of birth in YYYY-MM-DD format",
    )
    place_of_birth: StrictStr = Field(
        ...,
        description="Place of birth (city/country)",
    )
    nationality: StrictStr = Field(
        ...,
        description="Nationality / citizenship",
    )
    
    # ── Document Details ──
    passport_number: StrictStr = Field(
        ...,
        description="Passport or national ID number",
    )
    passport_issue_date: StrictStr = Field(
        ...,
        description="Passport/ID issue date in YYYY-MM-DD format",
    )
    passport_issuing_authority: StrictStr = Field(
        ...,
        description="Authority that issued the document (e.g., MOFA, MVR)",
    )

    # ── Custom Validators ──
    
    @field_validator("date_of_birth", "passport_issue_date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Enforce YYYY-MM-DD format for all date fields."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                f"Date must be in YYYY-MM-DD format, got: '{v}'"
            )
        return v

    @field_validator("passport_number")
    @classmethod
    def validate_passport_number(cls, v: str) -> str:
        """Ensure passport number is non-empty and alphanumeric."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Passport number cannot be empty")
        if not cleaned.replace(" ", "").isalnum():
            raise ValueError(
                f"Passport number must be alphanumeric, got: '{v}'"
            )
        return cleaned
        
    @field_validator("first_name", "last_name", "nationality", 
                     "place_of_birth", "passport_issuing_authority")
    @classmethod
    def validate_required_strings(cls, v: str) -> str:
        """Ensure required string fields are not empty."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError(f"Field cannot be empty")
        return cleaned


"""
Schema Usage Example:

    # Valid data
    person = PersonSchema(
        first_name="John",
        last_name="Doe",
        date_of_birth="1990-01-15",
        place_of_birth="New York, USA",
        nationality="USA",
        passport_number="AB1234567",
        passport_issue_date="2020-06-01",
        passport_issuing_authority="US Department of State"
    )
    
    # Invalid date format — raises ValidationError
    person = PersonSchema(
        ...
        date_of_birth="15/01/1990",  # Error: must be YYYY-MM-DD
        ...
    )
"""
