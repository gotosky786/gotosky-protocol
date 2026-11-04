import datetime
import urllib.parse

class AutonomousDispatcher:
    """
    OmniFlow Autonomous Dispatcher:
    AI ke tayyar karda Ads ko Creator Kits aur 
    Fraud-Proof Affiliate/Tracking Links ke sath distribute karta hai.
    """
    def __init__(self, base_tracking_url="http://127.0.0.1:8000"):
        self.base_url = base_tracking_url

    def generate_smart_partner_link(self, target_url: str, partner_id: str, campaign_name: str) -> str:
        """Har Creator ya Group Admin ke liye alag fraud-proof tracking link banana"""
        params = {
            "target": target_url,
            "ref_partner": partner_id,
            "campaign": campaign_name,
            "utm_source": "omniflow_partner_network",
            "utm_medium": "creator_dispatch"
        }
        smart_link = f"{self.base_url}/api/track/redirect?{urllib.parse.urlencode(params)}"
        return smart_link

    def create_creator_broadcast_kit(self, ad_package: dict, partner_id: str) -> dict:
        """
        Telegram, Discord aur Media Admins ke liye 
        Ready-to-Post High-Value Kit generate karna
        """
        campaign_slug = ad_package["title"].lower().replace(" ", "_")[:15]
        partner_link = self.generate_smart_partner_link(
            target_url=ad_package["targetUrl"],
            partner_id=partner_id,
            campaign_name=campaign_slug
        )

        # Telegram / Discord Formatted Message (Emojis aur professional layout ke sath)
        broadcast_message = (
            f"🎬 **EXCLUSIVE MEDIA PROMOTION: {ad_package['title'].upper()}**\n\n"
            f"🔥 **Hook:** {ad_package['hook_headline']}\n\n"
            f"📖 **Story / Overview:**\n{ad_package['scripts']['english']}\n\n"
            f"🇵🇰 **Urdu Summary:**\n{ad_package['scripts']['urdu']}\n\n"
            f"🔗 **Official Link & Access:**\n👉 {partner_link}\n\n"
            f"💰 *Partner ID:* `{partner_id}` | *Tracked by OmniFlow Protocol*\n"
            f"{' '.join(ad_package['hashtags'])}"
        )

        return {
            "partner_id": partner_id,
            "smart_link": partner_link,
            "dispatch_ready_message": broadcast_message,
            "status": "DISPATCH_READY",
            "timestamp": str(datetime.datetime.now())
        }

# --- TEST RUNNER (Live Check) ---
if __name__ == "__main__":
    dispatcher = AutonomousDispatcher()

    # Module 3 (AI Brain) ka sample output
    sample_ai_ad = {
        "title": "Apple iPhone & Ecosystem",
        "targetUrl": "https://www.apple.com",
        "hook_headline": "Wait! Don't scroll past this — Apple is finally here! 🔥",
        "scripts": {
            "english": "Attention! Experience Apple. Discover innovative technology and shop now.",
            "urdu": "Rukye! Kya aapne dekha Apple ka naya launch? Abhi link par click karein!",
            "arabic": "اكتشف الآن أحدث تقنيات أبل الحصرية."
        },
        "hashtags": ["#viral", "#Apple", "#trending", "#omniflow"]
    }

    print("\n🚀 [DISPATCHER ENGINE] Media Creators aur Group Admins ke liye Campaign Kit ban rahi hai...\n")

    # Misaal ke tor par 2 Creators ko kit dispatch karni hai:
    partners = ["creator_karachi_01", "admin_dubai_vip"]

    for pid in partners:
        kit = dispatcher.create_creator_broadcast_kit(sample_ai_ad, partner_id=pid)
        print("=" * 65)
        print(f"📦 DISPATCH KIT FOR PARTNER: [{kit['partner_id'].upper()}]")
        print("=" * 65)
        print(kit["dispatch_ready_message"])
        print("\n🎯 SMART TRACKING URL GENERATED:")
        print(f"   {kit['smart_link']}")
        print("=" * 65 + "\n")