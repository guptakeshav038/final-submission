"""Load demo data:  python seed.py   (password for every demo account: password123)"""
from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Campaign, CreatorProfile, User
from app.security import hash_password

CREATORS = [
    # name, handle, niche, bio, followers, eng%, genuine, reel views, city, age, gender(f), india share, quality, roi, price
    ("Aanya Rao", "aanya.moves", "fitness, yoga, athleisure", "Pune-based trainer sharing home workouts, athleisure hauls and mobility routines.", 38000, 7.4, 0.93, 21000, "Pune", {"18-24": 0.46, "25-34": 0.40, "35-44": 0.10, "45+": 0.04}, 0.71, 0.88, 91, 82, 9000),
    ("Kabir Mehta", "kabir.lifts", "fitness, bodybuilding, nutrition", "Strength coach from Mumbai. Programs, meal prep and honest supplement reviews.", 142000, 4.1, 0.78, 64000, "Mumbai", {"18-24": 0.38, "25-34": 0.42, "35-44": 0.15, "45+": 0.05}, 0.12, 0.84, 80, 70, 45000),
    ("Isha Kulkarni", "isha.runs", "running, fitness, marathon", "Weekend marathoner in Pune. Shoe reviews, race recaps and training plans.", 21000, 8.2, 0.95, 12000, "Pune", {"18-24": 0.30, "25-34": 0.52, "35-44": 0.14, "45+": 0.04}, 0.55, 0.90, 86, 78, 5500),
    ("Rohan Iyer", "rohan.tech", "tech, gadgets, smartphones", "Bengaluru gadget reviewer: phones, laptops and audio gear explained simply.", 310000, 3.2, 0.69, 98000, "Bengaluru", {"18-24": 0.44, "25-34": 0.40, "35-44": 0.12, "45+": 0.04}, 0.05, 0.91, 85, 72, 90000),
    ("Meera Nair", "meera.eats", "food, recipes, street food", "Chennai home cook. Quick vegetarian recipes and regional street food guides.", 54000, 6.6, 0.90, 30000, "Chennai", {"18-24": 0.25, "25-34": 0.48, "35-44": 0.22, "45+": 0.05}, 0.62, 0.92, 87, 80, 12000),
    ("Zoya Khan", "zoya.styles", "fashion, streetwear, thrift", "Delhi stylist. Thrift flips, streetwear lookbooks and festive styling.", 87000, 5.3, 0.84, 41000, "Delhi", {"18-24": 0.55, "25-34": 0.35, "35-44": 0.08, "45+": 0.02}, 0.80, 0.93, 88, 74, 22000),
    ("Dev Malhotra", "dev.wanders", "travel, adventure, photography", "Jaipur-based travel storyteller covering offbeat Rajasthan and Himalayan treks.", 120000, 4.8, 0.81, 52000, "Jaipur", {"18-24": 0.35, "25-34": 0.45, "35-44": 0.15, "45+": 0.05}, 0.22, 0.86, 90, 76, 38000),
    ("Sana Qureshi", "sana.glow", "beauty, skincare, makeup", "Hyderabad skincare nerd. Ingredient breakdowns and budget routines.", 46000, 7.0, 0.92, 26000, "Hyderabad", {"18-24": 0.52, "25-34": 0.38, "35-44": 0.08, "45+": 0.02}, 0.85, 0.89, 84, 79, 10000),
    ("Arjun Das", "arjun.plays", "gaming, esports, streaming", "Valorant and mobile gaming streamer with a daily highlights channel.", 205000, 3.9, 0.74, 88000, "Mumbai", {"18-24": 0.62, "25-34": 0.30, "35-44": 0.06, "45+": 0.02}, 0.10, 0.88, 78, 68, 60000),
    ("Nisha Verma", "nisha.money", "personal finance, investing, careers", "Pune finance educator. Mutual funds, tax basics and first-job money tips.", 33000, 6.1, 0.94, 15000, "Pune", {"18-24": 0.28, "25-34": 0.54, "35-44": 0.14, "45+": 0.04}, 0.45, 0.90, 85, 83, 8000),
    ("Tara Joshi", "tara.green", "sustainable living, zero waste, home", "Mumbai zero-waste swaps, refill shopping and low-impact home ideas.", 29000, 7.8, 0.96, 17000, "Mumbai", {"18-24": 0.34, "25-34": 0.47, "35-44": 0.15, "45+": 0.04}, 0.70, 0.91, 89, 85, 7000),
    ("Vikram Sethi", "vik.parenting", "parenting, family, kids", "Delhi dad documenting school runs, weekend activities and gear reviews.", 62000, 5.0, 0.87, 24000, "Delhi", {"18-24": 0.08, "25-34": 0.44, "35-44": 0.40, "45+": 0.08}, 0.30, 0.95, 82, 77, 14000),
]


def main():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    if db.scalar(select(User).where(User.email == "brand@demo.com")):
        print("Demo data already loaded.")
        return

    pw = hash_password("password123")
    brand = User(email="brand@demo.com", password_hash=pw, name="Nimbus Athleisure", role="brand")
    db.add(brand)

    for name, handle, niche, bio, followers, eng, genuine, views, city, age, female, india, quality, roi, price in CREATORS:
        user = User(email=f"{handle.replace('.', '')}@demo.com", password_hash=pw, name=name, role="creator")
        db.add(user)
        db.flush()
        db.add(CreatorProfile(
            user_id=user.id, handle=handle, bio=bio, niche=niche, followers=followers,
            engagement_rate=eng, genuine_engagement_ratio=genuine, avg_reel_views=views,
            country="India", city=city, audience_age=age,
            audience_gender={"female": female, "male": round(1 - female, 2)},
            audience_countries={"India": india, "Other": round(1 - india, 2)},
            content_quality=quality, past_roi=roi, price_per_post=price,
        ))
    db.flush()
    db.add(Campaign(
        brand_id=brand.id, title="Pune store launch: monsoon running range",
        description="Launching our athleisure and running apparel in Pune. We want fitness creators with a local audience who review gear honestly.",
        niche="fitness, running, athleisure", goal="local_launch",
        target_age_buckets=["18-24", "25-34"], target_gender="any",
        target_country="India", target_city="Pune", budget=30000, min_followers=10000, max_followers=150000,
    ))
    db.commit()
    print("Seeded 1 brand, %d creators, 1 campaign." % len(CREATORS))
    print("Brand login: brand@demo.com / password123   Creator login: aanyamoves@demo.com / password123")


if __name__ == "__main__":
    main()
