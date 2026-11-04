from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime

app = FastAPI(title="GoToSky Protocol - Controller Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LIVE SYSTEM CONFIGURATION
SYSTEM_CONFIG = {
    "ad_duration": 12,        # Default Duration (Settings se update hoga)
    "auto_next_wait": 3,
    "budget_cap": 10.0
}

# LIVE ADS DATABASE
LIVE_ADS_DATABASE = [
    {
        "id": "ad_movie_01",
        "badge": "ORIGINAL 3D MOVIE",
        "rating": "⭐ 9.9 / 10",
        "category": "ACTION & SCI-FI CINEMA",
        "title": "THE LEGEND OF GALAXY: 3D MOVIE",
        "desc": "Official Worldwide Premiere. Witness groundbreaking visual effects exclusively on 3D screens.",
        "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "targetUrl": "https://www.youtube.com",
        "specs": "DOLBY VISION • 4K ULTRA • 2026",
        "lang": "English Master Audio (Urdu Dub)",
        "duration": "7 Days",
        "status": "ACTIVE"
    },
    {
        "id": "ad_cartoon_02",
        "badge": "3D ANIMATED CARTOON",
        "rating": "⭐ 9.7 / 10",
        "category": "KIDS & FAMILY 3D CARTOON",
        "title": "SUPER HEROES: HEROIC ADVENTURES",
        "desc": "A vibrant 3D animated universe packed with humor, bravery, and high-flying superhero missions.",
        "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "targetUrl": "https://www.disney.com",
        "specs": "FAMILY FRIENDLY • 3D CGI • 4K",
        "lang": "English / Multi-Language",
        "duration": "30 Days",
        "status": "ACTIVE"
    }
]

# Models
class TrackEvent(BaseModel):
    ad_id: str
    event_type: str

class NewCampaignPayload(BaseModel):
    title: str
    targetUrl: str
    category: str
    videoUrl: str
    duration: str = "7 Days"

class TogglePayload(BaseModel):
    ad_id: str

class SettingsPayload(BaseModel):
    ad_duration: int
    budget_cap: float

@app.get("/")
def home():
    return {"status": "Online", "engine": "GoToSky Protocol"}
@app.get("/gotosky.js")
def serve_embed_sdk():
    return FileResponse("gotosky.js", media_type="application/javascript")
# 1. LIVE ADS & DURATION RETRIEVE (Sirf ACTIVE ads bhejega, aur dynamic duration sath dega)
@app.get("/api/ads")
def get_live_ads():
    active_ads = [ad for ad in LIVE_ADS_DATABASE if ad.get("status") == "ACTIVE"]
    return {
        "success": True,
        "total_active": len(active_ads),
        "ad_duration": SYSTEM_CONFIG["ad_duration"],  # LIVE SECONDS (12s ya jo bhi set ho)
        "data": active_ads
    }

# 2. 1-CLICK CAMPAIGN LAUNCH
@app.post("/api/ads")
def create_new_campaign(payload: NewCampaignPayload):
    new_ad = {
        "id": f"ad_custom_{len(LIVE_ADS_DATABASE) + 1}",
        "badge": "OFFICIAL LAUNCH 2026",
        "rating": "⭐ 10 / 10",
        "category": payload.category.upper(),
        "title": payload.title.upper(),
        "desc": f"Official Campaign for {payload.title}. Tap 'Visit Link' to view official content.",
        "videoUrl": payload.videoUrl,
        "targetUrl": payload.targetUrl,
        "specs": "DOLBY ATMOS • 4K ULTRA • 2026",
        "lang": "English / Global Audio",
        "duration": payload.duration,
        "status": "ACTIVE"
    }
    LIVE_ADS_DATABASE.insert(0, new_ad)
    print(f"🚀 [NEW LAUNCH] -> {new_ad['title']} | Duration: {new_ad['duration']}")
    return {"success": True, "ad": new_ad}

# 3. ⏹️ EMERGENCY STOP & RESUME SWITCH
@app.post("/api/ads/toggle")
def toggle_ad_status(payload: TogglePayload):
    for ad in LIVE_ADS_DATABASE:
        if ad["id"] == payload.ad_id:
            ad["status"] = "PAUSED" if ad.get("status") == "ACTIVE" else "ACTIVE"
            print(f"⚡ [STATUS CHANGED] -> Ad '{ad['title']}' is now: {ad['status']}")
            return {"success": True, "ad_id": ad["id"], "new_status": ad["status"]}
    return {"success": False, "error": "Ad not found"}

# 4. ⚙️ SETTINGS DURATION SYNC (Dashboard se duration update karne ke liye)
@app.post("/api/settings")
def update_settings(payload: SettingsPayload):
    SYSTEM_CONFIG["ad_duration"] = payload.ad_duration
    SYSTEM_CONFIG["budget_cap"] = payload.budget_cap
    print(f"⏱️ [DURATION UPDATED] -> Timer ab set ho gaya: {payload.ad_duration} Seconds!")
    return {"success": True, "ad_duration": SYSTEM_CONFIG["ad_duration"]}

# 5. TRACKING
@app.post("/api/track")
def track_ad_activity(event: TrackEvent):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🔥 [TRACK] [{timestamp}] -> Ad: {event.ad_id} | Event: {event.event_type.upper()}")
    return {"status": "recorded"}