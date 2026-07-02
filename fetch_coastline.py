"""
One-shot script: fetches OSM coastline for the area east of the existing
GeoJSON (-133.5W to -128W) and merges it into coastline_data.geojson.
Run once via GitHub Actions, then the updated file is committed and this
script can be removed.
"""
import json
import requests
import time

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

QUERY = """
[out:json][timeout:60];
way[natural=coastline](67.5,-133.5,71.5,-128.0);
out geom;
"""

def overpass_to_linestrings(data):
    features = []
    for element in data.get("elements", []):
        if element.get("type") != "way":
            continue
        coords = [[pt["lon"], pt["lat"]] for pt in element.get("geometry", [])]
        if len(coords) >= 2:
            features.append({
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "LineString", "coordinates": coords}
            })
    return features

print("Fetching eastern coastline from Overpass...")
for attempt in range(3):
    try:
        r = requests.post(OVERPASS_URL, data={"data": QUERY}, timeout=90,
                          headers={"User-Agent": "dashboard-coastline-fetch/1.0 (arctic-monitoring)"})
        r.raise_for_status()
        data = r.json()
        break
    except Exception as e:
        print(f"Attempt {attempt+1} failed: {e}")
        time.sleep(10)
else:
    print("All attempts failed — coastline_data.geojson not updated")
    raise SystemExit(1)

new_features = overpass_to_linestrings(data)
print(f"Fetched {len(new_features)} new coastline segments")

with open("coastline_data.geojson") as f:
    existing = json.load(f)

existing["features"].extend(new_features)

with open("coastline_data.geojson", "w") as f:
    json.dump(existing, f, separators=(",", ":"))

print(f"coastline_data.geojson now has {len(existing['features'])} total features")
