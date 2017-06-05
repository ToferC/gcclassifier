import os
import xml.etree.ElementTree as ET


data_dir = "/home/chris/directory/data/Thesaurus"

xml = "CST20160704.xml"

tree = ET.parse(os.path.join(data_dir, xml))

root = tree.getroot()

for concept in root:
	print("\n****")
	for child in concept:
		if child.tag != "NON-DESCRIPTOR":
			print(f"{child.tag}: {child.text}")
		