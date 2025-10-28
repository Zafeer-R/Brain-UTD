from playwright.sync_api import sync_playwright
import datetime
import os

# 1. Get slugs like "tuesday", "wednesday", etc.
def get_day_slugs():
    today = datetime.datetime.now()
    return [(today + datetime.timedelta(days=i)).strftime("%A").lower() for i in range(7)]

# 2. Main scraper logic
def scrape_dining_hours():
    base_url = "https://services.utdallas.edu/dining/#"
    all_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for day in get_day_slugs():
            url = f"{base_url}{day}"
            print(f"Scraping {day.capitalize()}...")
            page.goto(url)
            page.wait_for_selector("table", timeout=5000)

            rows = page.query_selector_all("table tbody tr")

            all_data.append(f"\n==== {day.upper()} ====\n")

            current_location = None

            for row in rows:
                columns = row.query_selector_all("td")

                if len(columns) < 5:
                    continue  # skip malformed rows

                # 0 = location (or blank), 1 = name, 2 = open, 3 = dash, 4 = close
                loc_candidate = columns[0].inner_text().strip()
                name = columns[1].inner_text().strip()
                open_time = columns[2].inner_text().replace("\xa0", " ").strip()
                close_time = columns[4].inner_text().replace("\xa0", " ").strip()

                # Track latest non-empty location
                if loc_candidate:
                    current_location = loc_candidate

                if not name:
                    continue  # skip empty rows

                if open_time and close_time:
                    hours = f"{open_time} - {close_time}"
                else:
                    hours = "closed"

                line = f"{current_location} — {name} — {hours}"
                all_data.append(line)

        browser.close()

    # Ensure directory exists
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    output_dir = os.path.join(project_root, "data/scraped_data")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "dining.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_data))

    print(f"✅ Scraped data saved to '{output_path}'")

# 3. Run it
if __name__ == "__main__":
    scrape_dining_hours()