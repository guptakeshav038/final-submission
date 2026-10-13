from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from .models import Campaign, CreatorProfile, Match
from .scoring import score_creator

CANDIDATE_LIMIT = 100  # deck: score the top 100 screened candidates


def run_matching(db: Session, campaign: Campaign, limit: int = 20) -> list[Match]:
    # 1. Candidate screening with plain SQL filters
    q = select(CreatorProfile).options(joinedload(CreatorProfile.user)).where(CreatorProfile.followers > 0)
    if campaign.min_followers:
        q = q.where(CreatorProfile.followers >= campaign.min_followers)
    if campaign.max_followers:
        q = q.where(CreatorProfile.followers <= campaign.max_followers)
    if campaign.budget:
        q = q.where(CreatorProfile.price_per_post <= campaign.budget)
    q = q.order_by(CreatorProfile.engagement_rate.desc()).limit(CANDIDATE_LIMIT)
    candidates = db.scalars(q).all()

    # 2. Weighted scoring
    scored = sorted((score_creator(c, campaign) + (c,) for c in candidates), key=lambda t: t[0], reverse=True)[:limit]

    # 3. Upsert matches, keeping any status a brand or creator already set
    existing = {m.creator_id: m for m in db.scalars(select(Match).where(Match.campaign_id == campaign.id))}
    for score, breakdown, creator in scored:
        m = existing.get(creator.id)
        if m:
            m.score, m.breakdown = score, breakdown
        else:
            db.add(Match(campaign_id=campaign.id, creator_id=creator.id, score=score, breakdown=breakdown))
    db.commit()
    return list_matches(db, campaign.id)


def list_matches(db: Session, campaign_id: int) -> list[Match]:
    q = (
        select(Match)
        .options(joinedload(Match.creator).joinedload(CreatorProfile.user), joinedload(Match.campaign).joinedload(Campaign.brand))
        .where(Match.campaign_id == campaign_id)
        .order_by(Match.score.desc())
    )
    return list(db.scalars(q).unique())
