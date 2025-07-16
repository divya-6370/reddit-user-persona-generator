import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_username(url):
    match = re.search(r'reddit\.com/user/([^/]+)/?', url)
    return match.group(1) if match else None

def fetch_user_data(username):
    json_url = f"https://www.reddit.com/user/{username}.json"
    res = requests.get(json_url, headers=headers)
    if res.status_code != 200:
        print("❌ Could not fetch user data")
        return []
    data = res.json()
    posts_comments = []

    for item in data["data"]["children"]:
        kind = item["kind"]
        content = item["data"]
        if kind == "t1":  # Comment
            text = content.get("body", "")
            permalink = "https://www.reddit.com" + content.get("permalink", "")
            posts_comments.append(f"COMMENT:\n{text}\n🔗 {permalink}")
        elif kind == "t3":  # Post
            title = content.get("title", "")
            selftext = content.get("selftext", "")
            permalink = "https://www.reddit.com" + content.get("permalink", "")
            posts_comments.append(f"POST:\n{title}\n{selftext}\n🔗 {permalink}")
    return posts_comments

def generate_persona(entries, username):
    text_blob = "\n".join(entries).lower()
    persona = []

    # Age Estimate
    if "college" in text_blob or "school" in text_blob:
        persona.append("Age: Likely 18-24 (mentions school or college)")
    elif "career" in text_blob or "work" in text_blob:
        persona.append("Age: Likely 25-35 (discusses work)")

    # Location
    if "india" in text_blob:
        persona.append("Location: Possibly India")
    elif "california" in text_blob:
        persona.append("Location: Possibly California")

    # Interests
    interests = []
    if "ai" in text_blob or "openai" in text_blob:
        interests.append("AI/Technology")
    if "politics" in text_blob:
        interests.append("Politics")
    if "crypto" in text_blob:
        interests.append("Crypto")
    if interests:
        persona.append(f"Interests: {', '.join(interests)}")

    # Personality
    if "i think" in text_blob or "imo" in text_blob:
        persona.append("Personality: Reflective/Opinionated")
    if "thanks" in text_blob or "help" in text_blob:
        persona.append("Personality: Helpful")

    output = f"Reddit User Persona for u/{username}\n\n"
    output += "\n".join(persona)
    output += "\n\nSample Posts/Comments:\n\n"

    for i in range(min(3, len(entries))):
        output += f"---\n{entries[i][:500]}...\n\n"

    return output

def main():
    url = input("Enter Reddit Profile URL: ").strip()
    username = extract_username(url)
    if not username:
        print("❌ Invalid Reddit URL")
        return

    print(f"🔍 Fetching JSON data for u/{username}...")
    entries = fetch_user_data(username)

    if not entries:
        print("⚠️ No content found or user is private.")
        return

    result = generate_persona(entries, username)

    filename = f"{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"✅ Persona saved to {filename}")

if __name__ == "__main__":
    main()
