import requests
import feedparser
from database.db import get_db_connection


# ----------------- HELPER FUNCTION -----------------
def insert_opportunity(title, type_, organizer, platform, domains, deadline, link):
    print(f"👉 Inserting: {title} | {type_} | {organizer}")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT IGNORE INTO opportunities
            (title, type, organizer, platform, domains, deadline, link, indexed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
        """, (title, type_, organizer, platform, domains, deadline, link))
        conn.commit()
        print("✅ Insert committed")
    except Exception as e:
        print(f"❌ DB Insert Error for {title}: {e}")
    finally:
        cursor.close()
        conn.close()


# ----------------- MLH HACKATHONS (OFFICIAL API) -----------------
def fetch_mlh_hackathons():
    print("\n🚀 Fetching MLH Hackathons (API)...")

    MLH_API = "https://mlh.io/api/v2/events"

    headers = {
        "User-Agent": "VerifyEdBot/1.0 (Student Research Project)",
        "Accept": "application/json"
    }

    try:
        response = requests.get(MLH_API, headers=headers, timeout=15)

        # 🔍 Check HTTP status
        if response.status_code != 200:
            print(f"❌ MLH API failed with status {response.status_code}")
            print(response.text[:300])
            return

        # 🔍 Try parsing JSON safely
        try:
            data = response.json()
        except Exception:
            print("❌ MLH did not return JSON")
            print("Response preview:")
            print(response.text[:500])
            return

        events = data.get("data", [])
        print(f"Found {len(events)} MLH events")

        for event in events:
            insert_opportunity(
                title=event.get("name"),
                type_="Hackathon",
                organizer="Major League Hacking (MLH)",
                platform="MLH",
                domains="General",
                deadline=event.get("registration_deadline"),
                link=event.get("url")
            )

        print("✅ MLH hackathons fetched!")

    except Exception as e:
        print(f"❌ MLH fetch error: {e}")


# ----------------- CONFERENCES VIA WIKICFP -----------------
def fetch_wikicfp_conferences():
    print("\n📄 Fetching Conferences from WikiCFP...")

    WIKICFP_RSS = "http://www.wikicfp.com/cfp/rss"
    feed = feedparser.parse(WIKICFP_RSS)

    print(f"Found {len(feed.entries)} CFP entries")

    for entry in feed.entries[:25]:
        insert_opportunity(
            title=entry.title,
            type_="Conference",
            organizer="Indexed via WikiCFP",
            platform="Global",
            domains="General",
            deadline=None,
            link=entry.link if hasattr(entry, "link") else "https://www.wikicfp.com"
        )

    print("✅ WikiCFP conferences fetched!")


# ----------------- MASTER FUNCTION -----------------
def fetch_opportunities():
    print("\n==============================")
    print("🚀 STARTING OPPORTUNITY PIPELINE")
    print("==============================")

    fetch_mlh_hackathons()
    fetch_wikicfp_conferences()

    print("\n✅ ALL OPPORTUNITIES FETCHED SUCCESSFULLY")


# ----------------- MAIN -----------------
if __name__ == "__main__":
    fetch_opportunities()