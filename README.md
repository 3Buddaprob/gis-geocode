# GeoJSON to KML Batch Converter (for QGIS)

This Python script batch-converts multiple `.geojson` files into `.kml` format using only built-in Python libraries — no external dependencies required.

Designed to be run inside the **QGIS Python Console**, it supports:
- `Point`,`LineString` and `Polygon` geometries (no `multi` formats)
- Reading `name` and `description` fields from GeoJSON properties
- User-friendly folder selection for input and output directories
- Clean KML output suitable for use in Google Earth, MyMaps, etc.

---

## 📦 Features

- ✅ No external libraries required (no `geopandas`, `simplekml`, etc.)
- ✅ Automatically prompts for folder locations
- ✅ Reads `name` and `description` for each feature
- ✅ Compatible with QGIS 3.34+ (should work with most recent versions)

---

## 🛠️ How to Use

1. Open **QGIS**
2. Go to **Plugins → Python Console**
3. Click the **Show Editor** (notepad icon)
4. Load or paste the script
5. Click **Run Script (▶)**

You will be prompted to:
- Select a folder containing `.geojson` files
- Select an output folder for the resulting `.kml` files

Converted KML files will be saved in the output folder with matching filenames.

---

## 📁 Example GeoJSON Input

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "CDS 1 - GSM",
        "description": "Example description"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [-0.3873526, 51.5003413]
      }
    }
  ]
}
