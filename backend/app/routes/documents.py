import os
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.pdf_service import pdf_service
from app.services.chunking_service import chunking_service
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as temp_file:
            temp_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        extracted_text = pdf_service.extract_text(temp_path)

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in PDF",
            )

        chunks = chunking_service.chunk_text(extracted_text)

        embeddings = [
            embedding_service.embed_text(chunk)
            for chunk in chunks
        ]

        stored_count = vector_service.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
            document_name=file.filename,
        )

        return {
            "message": "Document uploaded successfully",
            "filename": file.filename,
            "chunks_created": len(chunks),
            "chunks_stored": stored_count,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(error)}",
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)