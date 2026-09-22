from fastapi import APIRouter
from db.qdrant import ( delete_document, list_documents)

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("/")
async def get_documents():
    return list_documents()

@router.delete("/{document_id}")
async def remove_document(document_id: str):
    delete_document(document_id)
    return {"message": f"Document with ID {document_id} deleted successfully."}
