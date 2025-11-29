import os
import random
import requests
import hashlib

from time import sleep
from typing import List, Dict
from bs4 import BeautifulSoup
from ics import Calendar, Event
from gemini import process_event_data

base_url = "https://leekduck.com"
event_page_url = f"{base_url}/events/"
output_file = "events.ics"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
]

headers = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://leekduck.com/",
    "Origin": "https://leekduck.com",
    "Sec-CH-UA": '"Chromium";v="120", "Google Chrome";v="120", ";Not A Brand";v="99"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "DNT": "1",  # Do Not Track
    "Cache-Control": "max-age=0",
}


def get_events() -> List[Dict]:
    events = []
    try:
        response = requests.get(event_page_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        current_events = soup.find("div", class_="events-list current-events")
        wrappers = current_events.find_all("span", class_="event-header-item-wrapper")

        for wrapper in wrappers:
            event_url = base_url + wrapper.find("a", class_="event-item-link").get("href")
            data = wrapper.find("h5", class_="event-header-time-period")
            event = wrapper.find("div", class_="event-text").find("h2").text.strip()
            start = data.get("data-event-start-date-check")
            end = data.get("data-event-end-date")
            sleep(1)  # Be polite and avoid overwhelming the server
            event_response = requests.get(event_url, headers=headers)
            event_soup = BeautifulSoup(event_response.content, "html.parser")
            try:
                event_description = event_soup.find("div", class_="event-description").text.strip()
            except AttributeError:
                continue
            print(f"Event: {event}\nURL: {event_url}\nDescription: {event_description}\nStart: {start}\nEnd: {end}\n")
            events.append({
                "name": event,
                "url": event_url,
                "description": event_description,
                "start": start,
                "end": end
            })

    except Exception as e:
        print(f"Error fetching events: {e}")
    print(f"Total events fetched: {len(events)}")
    return events

def generate_uid(event_name: str, start_time: str) -> str:
    raw_string = f"{event_name}-{start_time}"
    return hashlib.md5(raw_string.encode('utf-8')).hexdigest() + "@pmgo-event-calendar"

def save_events_to_ics(events: List[Dict], output_file: str = output_file) -> None:
    print(f"📥 Saving events to {output_file}...")
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                old_content = f.read()
            cal = Calendar(old_content) # read old calendar
            print(f"📖 Old calendar read, there are {len(cal.events)} events")
        except:
            print("⚠️ Failed to read old calendar, creating a new one.")
            cal = Calendar()
    else:
        cal = Calendar()

    existing_uids = set(e.uid for e in cal.events)

    for event in events:
        event_uid = generate_uid(event.get('name', ''), event.get('start', ''))
        if event_uid in existing_uids:
            continue  # Skip duplicate
        try:
            e = Event()
            e.name = event.get('name', 'No Title')
            begin = event.get('start')
            if not begin:
                continue
            e.begin = begin
            e.end = event.get('end')
            e.uid = event_uid
            e.description = f"Detail in LeekDuck: {event.get('url', 'none')}"
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
    data = process_event_data(events)
    save_events_to_ics(data)