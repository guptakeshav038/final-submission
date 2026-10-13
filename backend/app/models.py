from datetime import datetime

from sqlalchemy import (JSON, DateTime, Enum, Float, ForeignKey, Integer, String,
                        Text, UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

GOALS = ("balanced", "awareness", "conversion", "local_launch")
MATCH_STATUSES = ("pending", "invited", "accepted", "declined")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(Enum("creator", "brand", name="user_role"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class CreatorProfile(Base):
    """Profile + metrics for a creator (the deck's Users/Profiles + CreatorMetrics)."""

    __tablename__ = "creator_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    handle: Mapped[str] = mapped_column(String(80), default="")
    bio: Mapped[str] = mapped_column(Text, default="")
    niche: Mapped[str] = mapped_column(String(255), default="")  # comma separated tags
    followers: Mapped[int] = mapped_column(Integer, default=0)
    engagement_rate: Mapped[float] = mapped_column(Float, default=0.0)  # percent
    genuine_engagement_ratio: Mapped[float] = mapped_column(Float, default=0.5)  # 0..1
    avg_reel_views: Mapped[int] = mapped_column(Integer, default=0)
    country: Mapped[str] = mapped_column(String(80), default="")
    city: Mapped[str] = mapped_column(String(80), default="")
    audience_age: Mapped[dict] = mapped_column(JSON, default=dict)  # {"18-24": 0.5, ...}
    audience_gender: Mapped[dict] = mapped_column(JSON, default=dict)  # {"female": 0.6, ...}
    audience_countries: Mapped[dict] = mapped_column(JSON, default=dict)  # {"India": 0.8, ...}
    content_quality: Mapped[float] = mapped_column(Float, default=50.0)  # 0..100
    past_roi: Mapped[float] = mapped_column(Float, default=50.0)  # 0..100
    price_per_post: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user: Mapped[User] = relationship()

    @property
    def name(self) -> str:
        return self.user.name


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    niche: Mapped[str] = mapped_column(String(255), default="")
    goal: Mapped[str] = mapped_column(Enum(*GOALS, name="campaign_goal"), default="balanced")
    target_age_buckets: Mapped[list] = mapped_column(JSON, default=list)
    target_gender: Mapped[str] = mapped_column(String(20), default="any")
    target_country: Mapped[str] = mapped_column(String(80), default="")
    target_city: Mapped[str] = mapped_column(String(80), default="")
    budget: Mapped[int] = mapped_column(Integer, default=0)  # max price per creator, 0 = no cap
    min_followers: Mapped[int] = mapped_column(Integer, default=0)
    max_followers: Mapped[int] = mapped_column(Integer, default=0)  # 0 = no limit
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    brand: Mapped[User] = relationship()

    @property
    def brand_name(self) -> str:
        return self.brand.name


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (UniqueConstraint("campaign_id", "creator_id", name="uq_campaign_creator"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id", ondelete="CASCADE"), index=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("creator_profiles.id", ondelete="CASCADE"), index=True)
    score: Mapped[float] = mapped_column(Float)
    breakdown: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(Enum(*MATCH_STATUSES, name="match_status"), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    campaign: Mapped[Campaign] = relationship()
    creator: Mapped[CreatorProfile] = relationship()
