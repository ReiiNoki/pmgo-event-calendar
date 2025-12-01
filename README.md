# 📅 Pokémon GO Event Calendar (Auto-Sync)

[![Auto Update Calendar](https://github.com/reiinoki/pmgo-event-calendar/actions/workflows/main.yml/badge.svg)](https://github.com/reiinoki/pmgo-event-calendar/actions/workflows/main.yml)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Never miss a Community Day, Raid Hour, or Spotlight Hour again!**

This project automatically scrapes the latest Pokémon GO event schedules and generates a subscribe-able `.ics` calendar file. Just subscribe once, and your phone's calendar will stay updated every day.

> **Data Source:** All event data is sourced from [Leek Duck](https://leekduck.com/). Big thanks to them for maintaining such a great resource for the community.

---

## ✨ Features

* **🤖 Fully Automated:** Powered by GitHub Actions, the calendar updates daily with the latest events.
* **🌍 Smart Filtering:** Keeps your calendar clean by only showing recent and upcoming events (Past 3 days to Future 60 days).
* **🔗 Rich Details:** Events include direct links to Leek Duck pages for reward details, shiny rates, and guides.
* **📱 Cross-Platform:** Works natively on iOS (iPhone/iPad), Google Calendar, Android, Outlook, and macOS.
* **🕒 Timezone Aware:** Supports both "Local Time" events (like Community Days) and global events.

---

## 🚀 How to Subscribe

Copy the **Subscription URL** below using your favorite calendar app:

```text
https://reiinoki.github.io/pmgo-event-calendar/events.ics
```

### 🍎 iOS (iPhone / iPad)

1.  Open the **Settings** app.
2.  Go to **Calendar** > **Accounts** > **Add Account**.
3.  Select **Other** at the bottom.
4.  Tap **Add Subscribed Calendar**.
5.  Paste the URL above and tap **Next**.
6.  (Optional) Rename it to "Pokémon GO" and tap **Save**.
    * *The events will now appear in your iPhone Calendar app.*

### 🗓️ Google Calendar (Android / Web)

*Note: It is recommended to set this up on a desktop browser. It will auto-sync to your Android phone.*

1.  Open [Google Calendar](https://calendar.google.com/) on your computer.
2.  On the left sidebar, find **Other calendars** and click the **+** icon.
3.  Select **From URL**.
4.  Paste the URL above.
5.  Click **Add calendar**.
    * *On your Android phone, open the Calendar app, go to Settings, and ensure the new calendar is checked to "Sync".*

### 💻 macOS / Outlook

* **macOS:** Open Calendar app -> **File** -> **New Calendar Subscription** -> Paste URL.
* **Outlook:** Add Calendar -> **Subscribe from web** -> Paste URL.

---

## 🧪 Beta Testing & Feedback

This calendar is currently in **Beta**! While the core synchronization is automated and stable, minor display issues (especially with complex time conversions or event links) might occur.

We welcome all Pokémon GO Trainers to subscribe and help test the stability and accuracy of the event times.

* **Found an error?** Please open an Issue on this GitHub repository detailing the event name and the incorrect time. Your feedback is highly appreciated!

---


## ⚠️ FAQ

**Q: Why isn't Google Calendar updating immediately?**
A: Google Calendar has a slow refresh rate for external subscriptions (updates can take 12-24 hours). This is a limitation on Google's side. If you need instant updates, iOS Calendar or Outlook are faster.

**Q: Are the times correct for my timezone?**
A: Yes. Most events (like Community Day) use "Floating Time," meaning they appear at 2:00 PM in your local time regardless of where you are. Global events are automatically adjusted to your local timezone.

## 🛠️ For Developers

This project runs entirely on GitHub Actions using Python.

1.  **Scraper**: Fetches HTML from Leek Duck using `requests` & `BeautifulSoup`.
2.  **Processing**: Filters events based on a time window using standard `datetime` libraries.
3.  **Generation**: Creates an RFC 5545 compliant `.ics` file using the `ics` library.
4.  **Deployment**: Commits the file back to the repo to be served via GitHub Pages.

Feel free to fork this repository and customize your own filters!

---

## 📝 Disclaimer

* This project is unofficial and is not affiliated with, endorsed, sponsored, or specifically approved by Niantic, Inc., The Pokémon Company, or Nintendo.
* Data is scraped from [Leek Duck](https://leekduck.com/) for personal informational purposes only.
* Pokémon and Pokémon character names are trademarks of Nintendo.