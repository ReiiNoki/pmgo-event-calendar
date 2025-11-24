import requests
import hashlib

from typing import List, Dict

from bs4 import BeautifulSoup
from ics import Calendar, Event

base_url = "https://leekduck.com"
event_page_url = f"{base_url}/events/"
output_file = "events.ics"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_events() -> List[Dict]:
    events = []
    try:
        response = requests.get(event_page_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        for wrapper in soup.find_all("span", class_="event-header-item-wrapper"):
            data = wrapper.find("h5", class_="event-header-time-period")
            detail = base_url + wrapper.find("a", class_="event-item-link").get("href")
            start = data.get("data-event-start-date-check")
            end = data.get("data-event-end-date")
            event = wrapper.find("div", class_="event-text").find("h2").text.strip()

            events.append({
                "name": event,
                "start": start,
                "end": end,
                "detail": detail
            })
    except Exception as e:
        print(f"Error fetching events: {e}")

    return events

def generate_uid(event_name: str, start_time: str) -> str:
    raw_string = f"{event_name}-{start_time}"
    return hashlib.md5(raw_string.encode('utf-8')).hexdigest() + "@pmgo-event-calendar"

def save_events_to_ics(events: List[Dict], output_file: str = output_file) -> None:
    cal = Calendar()
    for event in events:
        event_uid = generate_uid(event["name"], event["start"])
        try:
            e = Event()
            e.name = event.get('name', 'No Title')
            begin = event.get('start')
            if not begin:
                continue
            e.begin = begin
            e.end = event.get('end')
            e.uid = event_uid
            e.description = f"Detail in LeekDuck: {event.get('detail', 'none')}"
            cal.events.add(e)
        except Exception as err:
            print(f"⚠️ Error in event [{event.get('name')}]: {err}")
            continue

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(cal.serialize_iter())
        print(f"✅ Events saved to {output_file}")
    except Exception as e:
        print(f"❌ Error saving ICS file: {e}")

if __name__ == "__main__":
    events = get_events()
    save_events_to_ics(events)