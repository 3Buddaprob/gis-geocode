import json
from pathlib import Path
import xml.etree.ElementTree as ET
from qgis.PyQt.QtWidgets import QFileDialog

KML_NS = "http://www.opengis.net/kml/2.2"

def create_kml_root():
    ET.register_namespace("", KML_NS)
    kml = ET.Element("{%s}kml" % KML_NS)
    doc = ET.SubElement(kml, "Document")
    return kml, doc

def coords_to_kml_str(coords):
    return " ".join([f"{lon},{lat},0" for lon, lat in coords])

def add_point(doc, name, coord, description):
    placemark = ET.SubElement(doc, "Placemark")
    ET.SubElement(placemark, "name").text = name
    ET.SubElement(placemark, "description").text = description
    point = ET.SubElement(placemark, "Point")
    ET.SubElement(point, "coordinates").text = f"{coord[0]},{coord[1]},0"

def convert_geojson_to_kml(geojson_path, kml_path):
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    kml, doc = create_kml_root()

    for feature in data.get("features", []):
        geometry = feature.get("geometry")
        props = feature.get("properties", {})
        name = props.get("name", "Unnamed Feature")
        description = props.get("description", "")

        if not geometry or geometry.get("type") != "Point":
            continue

        coords = geometry["coordinates"]
        add_point(doc, name, coords, description)

    tree = ET.ElementTree(kml)
    tree.write(kml_path, xml_declaration=True, encoding='utf-8')

# === Set up paths ===
print("📂 Please select the folder containing your GeoJSON files...")
input_dir = QFileDialog.getExistingDirectory(None, "Select Folder Containing GeoJSON Files")

print("📁 Please select the folder where KML files will be saved...")
output_dir = QFileDialog.getExistingDirectory(None, "Select Output Folder for KML Files")

if not input_dir or not output_dir:
    raise Exception("Input or output folder not selected. Script cancelled.")

input_folder = Path(input_dir)
output_folder = Path(output_dir)
output_folder.mkdir(parents=True, exist_ok=True)


# === Batch conversion ===
for geojson_file in input_folder.glob("*.geojson"):
    kml_file = output_folder / (geojson_file.stem + ".kml")
    print(f"Converting {geojson_file.name} → {kml_file.name}")
    try:
        convert_geojson_to_kml(geojson_file, kml_file)
    except Exception as e:
        print(f"Error converting {geojson_file.name}: {e}")
