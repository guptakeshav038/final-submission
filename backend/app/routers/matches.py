from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Campaign, CreatorProfile, Match, User
from ..schemas import MatchOut, MatchStatusIn
from ..security import current_user, require_role

router = APIRouter(prefix="/api/matches", tags=["matches"])


def _load(db: Session, match_id: int) -> Match | None:
    q = (
        select(Match)
        .options(joinedload(Match.creator).joinedload(CreatorProfile.user), joinedload(Match.campaign).joinedload(Campaign.brand))
        .where(Match.id == match_id)
    )
    return db.scalar(q)


@router.get("/me", response_model=list[MatchOut])
def my_offers(user: User = Depends(require_role("creator")), db: Session = Depends(get_db)):
    profile = db.scalar(select(CreatorProfile).where(CreatorProfile.user_id == user.id))
    if not profile:
        return []
    q = (
        select(Match)
        .options(joinedload(Match.creator).joinedload(CreatorProfile.user), joinedload(Match.campaign).joinedload(Campaign.brand))
        .where(Match.creator_id == profile.id, Match.status != "pending")
        .order_by(Match.created_at.desc())
    )
    return list(db.scalars(q).unique())


@router.patch("/{match_id}", response_model=MatchOut)
def update_status(match_id: int, body: MatchStatusIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    match = _load(db, match_id)
    if not match:
        raise HTTPException(404, "Match not found")

    if user.role == "brand":
        if match.campaign.brand_id != user.id:
            raise HTTPException(404, "Match not found")
        if body.status not in ("pending", "invited") or match.status in ("accepted", "declined"):
            raise HTTPException(400, "Brands can send or withdraw an offer until the creator responds")
    else:
        if match.creator.user_id != user.id:
            raise HTTPException(404, "Match not found")
        if match.status != "invited" or body.status not in ("accepted", "declined"):
            raise HTTPException(400, "Creators can accept or decline an offer they have received")

    match.status = body.status
    db.commit()
    return match
