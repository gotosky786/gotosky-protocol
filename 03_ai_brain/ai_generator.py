import requests
from bs4 import BeautifulSoup
import json
import re

class OmniAIBrain:
    """
    OmniFlow AI Brain:
    Kisi bhi Movie, App ya Brand ke link se khud ba khud
    Viral Hooks, Multi-lingual Scripts aur Ad Data tayyar karta hai.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def scrape_url_metadata(self, target_url: str):
        """Website ya Brand ke page se Safe OpenGraph data nikaalna"""
        print(f"\n🔍 [AI SCRAPER] Link analyze ho raha hai: {target_url} ...")
        try:
            response = requests.get(target_url, headers=self.headers, timeout=8)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Title nikaalna
            title = ""
            og_title = soup.find("meta", property="og:title")
            if og_title and og_title.get("content"):
                title = og_title["content"]
            elif soup.title and soup.title.string:
                title = soup.title.string.strip()
            else:
                title = "Global Featured Brand"

            # Description nikaalna
            desc = ""
            og_desc = soup.find("meta", property="og:description")
            if og_desc and og_desc.get("content"):
                desc = og_desc["content"]
            else:
                meta_desc = soup.find("meta", attrs={"name": "description"})
                if meta_desc and meta_desc.get("content"):
                    desc = meta_desc["content"]
                else:
                    desc = "Experience world-class innovation and premium entertainment with this exclusive launch."

            # Clean up title
            title = re.sub(r'[\r\n\t]+', ' ', title)[:60]
            desc = re.sub(r'[\r\n\t]+', ' ', desc)[:160]

            return {"success": True, "title": title, "desc": desc, "url": target_url}

        except Exception as e:
            print(f"⚠️ Warning: Direct scraping bypass -> Fallback mode: {str(e)}")
            return {
                "success": False,
                "title": "Blockbuster Worldwide Premiere",
                "desc": "Official trailer and global digital release. Watch now exclusively.",
                "url": target_url
            }

    def generate_viral_ad_package(self, url_data: dict, category="Entertainment"):
        """AI Copywriting Engine: 3-Second Hooks aur Scripts banana"""
        title = url_data.get("title", "Worldwide Brand")
        desc = url_data.get("desc", "")

        print("⚡ [AI COPYWRITER] Psychology-based viral hooks aur scripts generate ho rahe hain...\n")

        # 3-Second Attention Grabber Hooks
        viral_hooks = [
            f"Wait! Don't scroll past this — {title} is finally here! 🔥",
            f"Dunya bhar mein dhoom machane wala: {title}! Dekhein abhi 🎬",
            f"The future is now! Discover {title} before everyone else 🚀"
        ]

        # Multi-Language Voiceover Scripts (8-Second Ad ke liye)
        scripts = {
            "english": f"Attention! Experience {title}. {desc} Click the link now to explore more!",
            "urdu": f"Rukye! Kya aapne dekha {title}? Abhi visit link par click karein aur dunya ke sath jur jayein!",
            "arabic": f"انتبه! اكتشف الآن {title}. اضغط على الرابط للمزيد من التفاصيل الحصرية."
        }

        # Ready-to-Use Ad Package (JSON structure jo humare API server ke sath connect hoga)
        ad_package = {
            "title": title,
            "targetUrl": url_data.get("url"),
            "category": category,
            "hook_headline": viral_hooks[0],
            "scripts": scripts,
            "hashtags": ["#viral", f"#{re.sub(r'[^a-zA-Z0-9]', '', title)[:15]}", "#trending", "#omniflow", "#global"]
        }

        return ad_package

# --- TEST RUNNER (Jab script chalegi toh yeh live test karega) ---
if __name__ == "__main__":
    ai = OmniAIBrain()

    # Misaal ke tor par hum kisi bhi famous brand ya movie ka link check karte hain:
    test_link = "https://www.apple.com"  # Kal ko yahan movie link ya koi bhi app ho sakti hai

    # Step 1: Scrape
    extracted_data = ai.scrape_url_metadata(test_link)
    print(f"✅ Data Extracted: {extracted_data['title']}")

    # Step 2: AI Generate
    final_ad = ai.generate_viral_ad_package(extracted_data, category="Tech & Mobile")

    # Final Output Display
    print("=" * 60)
    print("🎉 [OMNIFLOW AI CAMPAIGN ASSETS GENERATED] 🎉")
    print("=" * 60)
    print(f"📌 Ad Title      : {final_ad['title']}")
    print(f"🎯 3-Sec Hook    : {final_ad['hook_headline']}")
    print(f"🌐 English Script: {final_ad['scripts']['english']}")
    print(f"🇵🇰 Urdu Script   : {final_ad['scripts']['urdu']}")
    print(f"🇸🇦 Arabic Script : {final_ad['scripts']['arabic']}")
    print(f"🏷️ Hashtags     : {' '.join(final_ad['hashtags'])}")
    print("=" * 60)