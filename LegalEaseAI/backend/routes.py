
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import Optional

router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str = "Non-Disclosure Agreement"
    jurisdiction: str = "Tamil Nadu, India"
    first_party: str
    second_party: str
    important_terms: str = "Confidentiality, non-disclosure, data protection"
    agreement_date: Optional[str] = None
    additional_requirements: Optional[str] = ""


@router.get("/")
def home():
    return {
        "message": "Welcome to LegalEaseAI API",
        "status": "running"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "LegalEaseAI"
    }


@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        if not request.first_party.strip():
            raise HTTPException(
                status_code=400,
                detail="First party name is required"
            )

        if not request.second_party.strip():
            raise HTTPException(
                status_code=400,
                detail="Second party name is required"
            )

        agreement_date = request.agreement_date or date.today().isoformat()

        document = f"""
{request.document_type.upper()}

JURISDICTION: {request.jurisdiction}
DATE: {agreement_date}

This Agreement is made between:

FIRST PARTY:
{request.first_party}

AND

SECOND PARTY:
{request.second_party}

1. PURPOSE
The parties enter into this agreement to protect confidential
information shared between them.

2. CONFIDENTIALITY
The receiving party agrees to keep confidential information
private and not disclose it to unauthorized persons.

3. PERMITTED USE
Confidential information shall only be used for the purpose
agreed upon by the parties.

4. DATA PROTECTION
Both parties shall take reasonable measures to protect
confidential information from unauthorized access or disclosure.

5. RETURN OF INFORMATION
Upon termination of the agreement, confidential materials
shall be returned or securely deleted, subject to applicable
legal retention requirements.

6. DURATION
The confidentiality obligations shall continue for the period
specified in the executed agreement, subject to applicable law.

7. BREACH AND REMEDIES
Any breach may give rise to remedies available under
applicable law.

8. GOVERNING LAW
This agreement shall be governed by the applicable laws of India.
The parties specify the jurisdiction of {request.jurisdiction},
subject to applicable law.

9. IMPORTANT TERMS
{request.important_terms}

10. ADDITIONAL REQUIREMENTS
{request.additional_requirements or "None specified"}

SIGNATURES

First Party: {request.first_party}

Signature: ____________________

Date: _________________________


Second Party: {request.second_party}

Signature: ____________________

Date: _________________________


Note: This is a basic draft for demonstration.
Have the agreement reviewed for legal suitability
before signing.
"""

        return {
            "success": True,
            "message": "Document generated successfully",
            "document_type": request.document_type,
            "document": document
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {str(e)}"
        )