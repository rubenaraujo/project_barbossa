import requests
import datetime
import zoneinfo

json_url = "https://streamed.su/api/matches/all"
default_poster = 'https://streamed.su/api/images/poster/fallback.webp'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5"
}

response = requests.get(json_url, headers=headers)
if not response.ok:
    print('Request error:', response.text)
    exit(1)

try:
    data = response.json()
except Exception as e:
    print('Failed to decode JSON:', str(e))
    exit(1)

def should_skip_event(event_date, current_datetime):
    if event_date == 0:
        return False
    event_datetime = datetime.datetime.utcfromtimestamp(event_date / 1000).replace(tzinfo=datetime.timezone.utc)
    event_lisbon = event_datetime.astimezone(zoneinfo.ZoneInfo("Europe/Lisbon"))
    hours_diff = (event_lisbon - current_datetime).total_seconds() / 3600
    return hours_diff < -4 or hours_diff > 24

# Set current datetime to Europe/Lisbon time (with DST support)
tz_lisbon = zoneinfo.ZoneInfo("Europe/Lisbon")
current_datetime = datetime.datetime.now(tz_lisbon)

m3u8_content = "#EXTM3U\n\n"

for match in data:
    if should_skip_event(match['date'], current_datetime):
        continue

    poster = 'https://streamed.su' + match['poster'] if 'poster' in match and match['poster'] else default_poster
    category = "24/7 Live" if match['date'] == 0 else match['category']
    category_formatted = "24/7 Live" if category == "24/7 Live" else category.replace('-', ' ').title()

    for source in match['sources']:
        source_name = source['source'].lower().title()
        id_ = source['id']
        event_datetime = datetime.datetime.utcfromtimestamp(match['date'] / 1000).replace(tzinfo=datetime.timezone.utc)
        event_datetime_lisbon = event_datetime.astimezone(tz_lisbon)
        formatted_time = event_datetime_lisbon.strftime('%I:%M %p')
        formatted_date = event_datetime_lisbon.strftime('%d/%m/%Y')

        if category == "24/7 Live":
            m3u8_content += f'#EXTINF:-1 tvg-name="{match["title"]}" tvg-logo="{poster}" group-title="{category_formatted}",{match["title"]}\n'
        else:
            match_name = f"{formatted_time} - {match['title']} [{source_name}] - ({formatted_date})"
            m3u8_content += f'#EXTINF:-1 tvg-name="{match["title"]}" tvg-logo="{poster}" group-title="{category_formatted}",{match_name}\n'

        m3u8_content += f'https://rr.vipstreams.in/{source_name}/stream/{id_}/1/playlist.m3u8\n'

with open('streamed.m3u8', 'w', encoding='utf-8') as f:
    f.write(m3u8_content)

print("M3U8 file has been saved as streamed.m3u8.")
