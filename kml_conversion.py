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
    
def add_linestring(doc, name, coords, description):
    placemark = ET.SubElement(doc, "Placemark")
    ET.SubElement(placemark, "name").text = name
    ET.SubElement(placemark, "description").text = description
    linestring = ET.SubElement(placemark, "LineString")
    ET.SubElement(linestring, "tessellate").text = "1"
    ET.SubElement(linestring, "coordinates").text = coords_to_kml_str(coords)

def add_polygon(doc, name, outer_coords, description):
    placemark = ET.SubElement(doc, "Placemark")
    ET.SubElement(placemark, "name").text = name
    ET.SubElement(placemark, "description").text = description
    polygon = ET.SubElement(placemark, "Polygon")
    ET.SubElement(polygon, "tessellate").text = "1"
    outer = ET.SubElement(polygon, "outerBoundaryIs")
    ring = ET.SubElement(outer, "LinearRing")
    ET.SubElement(ring, "coordinates").text = coords_to_kml_str(outer_coords)
    
def convert_geojson_to_kml(geojson_path, kml_path):
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    kml, doc = create_kml_root()

    for feature in data.get("features", []):
        geometry = feature.get("geometry")
        props = feature.get("properties", {})
        name = str(props.get("name", "Unnamed Feature"))
        description = str(props.get("description", ""))

        if not geometry:
            continue

        gtype = geometry["type"]
        coords = geometry["coordinates"]

        if gtype == "Point":
            add_point(doc, name, coords, description)

        elif gtype == "LineString":
            add_linestring(doc, name, coords, description)

        elif gtype == "Polygon":
            add_polygon(doc, name, coords[0], description)  # Use outer ring only

        else:
            print(f"⚠️ Skipped unsupported geometry type: {gtype}")

    # Save the KML to file here — THIS IS MISSING
    tree = ET.ElementTree(kml)
    tree.write(kml_path, encoding="utf-8", xml_declaration=True)
    
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

print(f"Output folder is: {output_folder.resolve()}")

# === Batch conversion ===
for geojson_file in input_folder.glob("*.geojson"):
    print(f"Found GeoJSON file: {geojson_file.name}")
    kml_file = output_folder / (geojson_file.stem + ".kml")
    print(f"Will convert to: {kml_file.name}")
    try:
        convert_geojson_to_kml(geojson_file, kml_file)
        print(f"Successfully converted {geojson_file.name}")
    except Exception as e:
        print(f"Error converting {geojson_file.name}: {e}")


#for geojson_file in input_folder.glob("*.geojson"):
 #   kml_file = output_folder / (geojson_file.stem + ".kml")
  #  print(f"Converting {geojson_file.name} → {kml_file.name}")
   # try:
    #    convert_geojson_to_kml(geojson_file, kml_file)
    #except Exception as e:
     #   print(f"Error converting {geojson_file.name}: {e}")
