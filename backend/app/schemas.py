from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Goal = Literal["balanced", "awareness", "conversion", "local_launch"]
MatchStatus = Literal["pending", "invited", "accepted", "declined"]


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserOut(ORM):
    id: int
    email: str
    name: str
    role: str


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    name: str = Field(min_length=1, max_length=120)
    role: Literal["creator", "brand"]


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class CreatorOut(ORM):
    id: int
    name: str
    handle: str
    bio: str
    niche: str
    followers: int
    engagement_rate: float
    genuine_engagement_ratio: float
    avg_reel_views: int
    country: str
    city: str
    audience_age: dict
    audience_gender: dict
    audience_countries: dict
    content_quality: float
    past_roi: float
    price_per_post: int


class CreatorUpdate(BaseModel):
    handle: Optional[str] = Field(None, max_length=80)
    bio: Optional[str] = Field(None, max_length=2000)
    niche: Optional[str] = Field(None, max_length=255)
    followers: Optional[int] = Field(None, ge=0)
    engagement_rate: Optional[float] = Field(None, ge=0, le=100)
    genuine_engagement_ratio: Optional[float] = Field(None, ge=0, le=1)
    avg_reel_views: Optional[int] = Field(None, ge=0)
    country: Optional[str] = Field(None, max_length=80)
    city: Optional[str] = Field(None, max_length=80)
    audience_age: Optional[dict] = None
    audience_gender: Optional[dict] = None
    audience_countries: Optional[dict] = None
    price_per_post: Optional[int] = Field(None, ge=0)


class CampaignIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field("", max_length=4000)
    niche: str = Field("", max_length=255)
    goal: Goal = "balanced"
    target_age_buckets: list[str] = []
    target_gender: Literal["any", "female", "male", "other"] = "any"
    target_country: str = Field("", max_length=80)
    target_city: str = Field("", max_length=80)
    budget: int = Field(0, ge=0)
    min_followers: int = Field(0, ge=0)
    max_followers: int = Field(0, ge=0)


class CampaignOut(ORM):
    id: int
    brand_id: int
    brand_name: str
    title: str
    description: str
    niche: str
    goal: str
    target_age_buckets: list
    target_gender: str
    target_country: str
    target_city: str
    budget: int
    min_followers: int
    max_followers: int


class MatchOut(ORM):
    id: int
    campaign_id: int
    score: float
    breakdown: dict
    status: str
    creator: CreatorOut
    campaign: CampaignOut


class MatchStatusIn(BaseModel):
    status: MatchStatus
