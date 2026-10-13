from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import CreatorProfile, User
from ..schemas import CreatorOut, CreatorUpdate
from ..security import require_role

router = APIRouter(prefix="/api/creators", tags=["creators"])


def _own_profile(db: Session, user: User) -> CreatorProfile:
    profile = db.scalar(select(CreatorProfile).options(joinedload(CreatorProfile.user)).where(CreatorProfile.user_id == user.id))
    if not profile:
        raise HTTPException(404, "Creator profile not found")
    return profile


@router.get("", response_model=list[CreatorOut])
def list_creators(
    q: str = "",
    niche: str = "",
    country: str = "",
    min_followers: int = Query(0, ge=0),
    limit: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
):
    stmt = select(CreatorProfile).options(joinedload(CreatorProfile.user)).where(CreatorProfile.followers >= min_followers)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(CreatorProfile.handle.ilike(like), CreatorProfile.bio.ilike(like), CreatorProfile.niche.ilike(like)))
    if niche:
        stmt = stmt.where(CreatorProfile.niche.ilike(f"%{niche}%"))
    if country:
        stmt = stmt.where(CreatorProfile.country == country)
    stmt = stmt.where(CreatorProfile.followers > 0).order_by(CreatorProfile.engagement_rate.desc()).limit(limit)
    return db.scalars(stmt).all()


@router.get("/me", response_model=CreatorOut)
def my_profile(user: User = Depends(require_role("creator")), db: Session = Depends(get_db)):
    return _own_profile(db, user)


@router.put("/me", response_model=CreatorOut)
def update_profile(body: CreatorUpdate, user: User = Depends(require_role("creator")), db: Session = Depends(get_db)):
    profile = _own_profile(db, user)
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(profile, field, value)
    db.commit()
    return profile


@router.get("/{creator_id}", response_model=CreatorOut)
def get_creator(creator_id: int, db: Session = Depends(get_db)):
    profile = db.scalar(select(CreatorProfile).options(joinedload(CreatorProfile.user)).where(CreatorProfile.id == creator_id))
    if not profile:
        raise HTTPException(404, "Creator not found")
    return profile
