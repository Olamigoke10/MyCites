from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import CitationResponse, CitationStyle
from app.services.document_parser import DocumentParser

router = APIRouter()
document_parser = DocumentParser()


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "citations route ready"}


@router.post("/generate", response_model=CitationResponse)
async def generate_citations(
    file: UploadFile = File(...),
    style: CitationStyle = "APA",
) -> CitationResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        extracted_text = document_parser.extract_text(file.filename or "", content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to parse uploaded document.") from exc

    warning = []
    if not extracted_text:
        warning.append("No readable text found in the uploaded document.")

    # Placeholder output for citation generation in next todo.
    return CitationResponse(references=[], annotated_text=extracted_text, warnings=warning)
