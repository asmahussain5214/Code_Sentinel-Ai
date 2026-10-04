from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.analysis import AnalysisResult
from app.models.snippet import CodeSnippet
from app.models.user import User
from app.schemas.analysis import AnalysisCreate, AnalysisResponse
from app.services.analyzer import analyze_code_snippet

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def analyze_snippet(
    analysis_in: AnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Runs automated static analysis & security check on a submitted snippet."""
    snippet = db.query(CodeSnippet).filter(CodeSnippet.id == analysis_in.snippet_id).first()
    if not snippet:
        raise HTTPException(status_code=404, detail="Code snippet not found")
    if snippet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to analyze this snippet")

    # Perform analysis
    analysis_data = analyze_code_snippet(snippet.code_content, snippet.language)

    # Save analysis result to Oracle DB
    result = AnalysisResult(
        snippet_id=snippet.id,
        quality_score=analysis_data["quality_score"],
        security_score=analysis_data["security_score"],
        summary=analysis_data["summary"],
        suggestions=analysis_data["suggestions"],
        detected_bugs=analysis_data["detected_bugs"],
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.get("/{snippet_id}", response_model=AnalysisResponse)
def get_analysis_result(
    snippet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves the latest analysis report for a given snippet."""
    result = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.snippet_id == snippet_id)
        .order_by(AnalysisResult.created_at.desc())
        .first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No analysis report found for this snippet")
    return result