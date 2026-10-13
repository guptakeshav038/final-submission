from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..matching import list_matches, run_matching
from ..models import Campaign, User
from ..schemas import CampaignIn, CampaignOut, MatchOut
from ..security import require_role

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])


def _own_campaign(db: Session, user: User, campaign_id: int) -> Campaign:
    campaign = db.scalar(select(Campaign).options(joinedload(Campaign.brand)).where(Campaign.id == campaign_id))
    if not campaign or campaign.brand_id != user.id:
        raise HTTPException(404, "Campaign not found")
    return campaign


@router.post("", response_model=CampaignOut, status_code=201)
def create_campaign(body: CampaignIn, user: User = Depends(require_role("brand")), db: Session = Depends(get_db)):
    campaign = Campaign(brand_id=user.id, **body.model_dump())
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("", response_model=list[CampaignOut])
def my_campaigns(user: User = Depends(require_role("brand")), db: Session = Depends(get_db)):
    q = select(Campaign).options(joinedload(Campaign.brand)).where(Campaign.brand_id == user.id).order_by(Campaign.created_at.desc())
    return db.scalars(q).all()


@router.get("/{campaign_id}", response_model=CampaignOut)
def get_campaign(campaign_id: int, user: User = Depends(require_role("brand")), db: Session = Depends(get_db)):
    return _own_campaign(db, user, campaign_id)


@router.post("/{campaign_id}/match", response_model=list[MatchOut])
def find_matches(campaign_id: int, user: User = Depends(require_role("brand")), db: Session = Depends(get_db)):
    campaign = _own_campaign(db, user, campaign_id)
    return run_matching(db, campaign)


@router.get("/{campaign_id}/matches", response_model=list[MatchOut])
def campaign_matches(campaign_id: int, user: User = Depends(require_role("brand")), db: Session = Depends(get_db)):
    campaign = _own_campaign(db, user, campaign_id)
    return list_matches(db, campaign.id)
