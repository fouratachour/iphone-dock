"""Télécharge les horaires de la mosquée (Mawaqit) indiquée dans mosque.txt
et les enregistre dans mosque.json, lu par le dock."""
import json
import re
import sys
import urllib.request

slug = open("mosque.txt", encoding="utf-8").read().strip()
slug = slug.rstrip("/").split("/")[-1]  # accepte aussi un lien complet
if not slug:
    sys.exit("mosque.txt est vide")

req = urllib.request.Request(
    "https://mawaqit.net/fr/" + slug,
    headers={"User-Agent": "Mozilla/5.0 (iphone-dock)"},
)
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
m = re.search(r"(?:let|var|const)\s+confData\s*=\s*(\{.*?\});\s*\n", html, re.S)
if not m:
    sys.exit("Données introuvables pour " + slug)
d = json.loads(m.group(1))

out = {
    "slug": slug,
    "name": d.get("name") or d.get("label") or slug,
    "timezone": d.get("timezone"),
    "latitude": d.get("latitude"),
    "longitude": d.get("longitude"),
    "jumua": d.get("jumua"),
    # calendar[mois 0-11][jour "1".."31"] = [fajr, shuruq, dhuhr, asr, maghrib, isha]
    "calendar": d.get("calendar"),
    "iqamaCalendar": d.get("iqamaCalendar"),
}
with open("mosque.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
print("OK :", out["name"])
