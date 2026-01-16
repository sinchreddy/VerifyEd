import requests
import feedparser
from database.db import get_db_connection


# ----------------- HELPER FUNCTION -----------------
def insert_opportunity(title, type_, organizer, platform, domains, deadline):
    print(f"👉 Inserting: {title} | {type_} | {organizer}")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO opportunities
            (title, type, organizer, platform, domains, deadline, indexed)
            VALUES (%s, %s, %s, %s, %s, %s, 1)
        """, (title, type_, organizer, platform, domains, deadline))
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

    try:
        response = requests.get(MLH_API, timeout=10)
        data = response.json()

        events = data.get("data", [])
        print(f"Found {len(events)} MLH events")

        for event in events:
            title = event.get("name")
            insert_opportunity(
                title=title,
                type_="Hackathon",
                organizer="Major League Hacking (MLH)",
                platform="Global",
                domains="General",
                deadline=None
            )

        print("✅ MLH hackathons fetched!")

    except Exception as e:
        print(f"❌ MLH API error: {e}")


# ----------------- CONFERENCES VIA WIKICFP -----------------
def fetch_wikicfp_conferences():
    print("\n📄 Fetching Conferences from WikiCFP...")

    WIKICFP_RSS = "http://www.wikicfp.com/cfp/rss"
    feed = feedparser.parse(WIKICFP_RSS)

    print(f"Found {len(feed.entries)} CFP entries")

    for entry in feed.entries[:25]:  # limit to avoid noise
        insert_opportunity(
            title=entry.title,
            type_="Conference",
            organizer="Indexed via WikiCFP",
            platform="Global",
            domains="General",
            deadline=None
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