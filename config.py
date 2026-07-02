"""
config.py — Tuktoyaktuk site configuration.

Every value here is specific to this site. Shared logic lives in
dashboard_lib.py (the dashboard-lib repo, checked out alongside this one
in the GitHub Actions workflow — see .github/workflows/update.yml).

To add or remove a block from this site's dashboard, edit dashboard_update.py
in this repo — not this file and not dashboard_lib.py.
"""

import dashboard_lib as lib

# =========================================================
# CORE SITE IDENTITY
# =========================================================
SITE_DISPLAY_NAME = "Tuktoyaktuk"
LAT = 69.4541
LON = -133.0374
TZ_NAME = "America/Inuvik"

# =========================================================
# MODIS / EPSG:3413
# PROVISIONAL — estimated geometrically from neighbouring sites.
# Verify visually after first run; adjust MODIS_CENTER_X/Y and
# MODIS_ROTATION_DEG if the image is miscentred or rotated.
# To recompute precisely: lib.compute_3413_center(LAT, LON)
# =========================================================
_HALF_WIDTH_M = 150_000
_MODIS_OVERSIZE_HALF_WIDTH_M = _HALF_WIDTH_M * lib.MODIS_OVERSIZE_FACTOR

MODIS_CENTER_X, MODIS_CENTER_Y = -2332000, 117000  # PROVISIONAL

MODIS_BBOX_3413 = (
    f"{MODIS_CENTER_X - _MODIS_OVERSIZE_HALF_WIDTH_M:.0f},{MODIS_CENTER_Y - _MODIS_OVERSIZE_HALF_WIDTH_M:.0f},"
    f"{MODIS_CENTER_X + _MODIS_OVERSIZE_HALF_WIDTH_M:.0f},{MODIS_CENTER_Y + _MODIS_OVERSIZE_HALF_WIDTH_M:.0f}"
)

MODIS_ROTATION_DEG = 92.0  # PROVISIONAL — verify visually after first run

# =========================================================
# UTM (for Sentinel-1) — Tuktoyaktuk is zone 8.
# Verified via compute_utm_zone(LON=-133.0374).
# =========================================================
UTM_ZONE = 8
UTM_EPSG = "32608"
UTM_CENTER_X, UTM_CENTER_Y = lib.latlon_to_utm(LAT, LON, zone=UTM_ZONE)

# =========================================================
# MAP ANNOTATION
# =========================================================
MAP_POINTS = [
    (LAT, LON, SITE_DISPLAY_NAME, -28),
    (68.933333, -137.2, "Shingle Point", -10),
    (68.360741, -133.723022, "Inuvik", -10, -90),
    (68.226653, -135.003294, "Aklavik", -10),
]

MAP_REFERENCE_LINES = []

COASTLINE_GEOJSON_PATH = "coastline_data.geojson"

# =========================================================
# TIDE STATION (DFO IWLS) — forecast only, no gauge data yet.
# Station code for Tuktoyaktuk: verify at https://www.tides.gc.ca/en/stations
# =========================================================
TIDE_STATION_CODE = "06490"   # PROVISIONAL — verify on DFO IWLS
TIDE_STATION_NAME = "Tuktoyaktuk"

# =========================================================
# MARINE FORECAST ZONE (Environment Canada)
# Tuktoyaktuk sits on the Mackenzie Delta / NWT Beaufort coast.
# Look up the zone at https://weather.gc.ca/marine/index_e.html
# =========================================================
MARINE_ZONE_ID = "17000"     # PROVISIONAL — verify on EC marine forecast page
MARINE_ZONE_NAME = "Mackenzie Delta"  # PROVISIONAL

# =========================================================
# TOTAL WATER LEVEL (TOPAZ6 / CMEMS)
# Yearly mean must be computed once via build_yearly_mean_helper_script.py.
# Using Shingle Point's value as a provisional stand-in until computed.
# =========================================================
WATER_LEVEL_YEARLY_MEAN = -0.2668  # PROVISIONAL — recompute for this site

# =========================================================
# HYDROMETRIC STATIONS — none for Tuktoyaktuk (nearest gauges are too far)
# =========================================================
HYDROMETRIC_STATIONS = []

# =========================================================
# INSTITUTIONAL BRANDING
# =========================================================
LOGO_URL = None
INSTITUTION_TEXT = (
    "This dashboard is provided by the Alfred Wegener Institute Helmholtz Centre "
    "for Polar and Marine Research."
)
