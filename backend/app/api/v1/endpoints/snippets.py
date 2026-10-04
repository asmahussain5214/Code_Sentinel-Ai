from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.snippet import CodeSnippet
from app.models.user import User
from app.schemas.snippet import SnippetCreate, SnippetResponse

router = APIRouter()


@router.post("/", response_model=SnippetResponse, status_code=status.HTTP_201_CREATED)
def create_snippet(
    snippet_in: SnippetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submits a new code snippet under the authenticated user account."""
    snippet = CodeSnippet(
        title=snippet_in.title,
        language=snippet_in.language,
        code_content=snippet_in.code_content,
        user_id=current_user.id,
    )
    db.add(snippet)
    db.commit()
    db.refresh(snippet)
    return snippet


@router.get("/", response_model=List[SnippetResponse])
def get_user_snippets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves all code snippets owned by the authenticated user."""
    return db.query(CodeSnippet).filter(CodeSnippet.user_id == current_user.id).all()


@router.get("/{snippet_id}", response_model=SnippetResponse)
def get_snippet_by_id(
    snippet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetches a specific code snippet by ID."""
    snippet = db.query(CodeSnippet).filter(CodeSnippet.id == snippet_id).first()
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    if snippet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this snippet")
    return snippet