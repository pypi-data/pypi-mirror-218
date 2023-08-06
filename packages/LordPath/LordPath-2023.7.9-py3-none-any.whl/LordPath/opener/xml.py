from pathlib import Path
from xml.dom import minidom
import xml.etree.ElementTree as ET
from LordPath.opener import Opener


def load_xml(file, default=None):
    return XmlOpener.load(file, default)


def save_xml(obj, file):
    return XmlOpener.save(obj, file)


class XmlOpener(Opener):
    compatible_endings = ['xml']

    @staticmethod
    def load(file, default=None) -> ET.Element:
        tree = ET.parse(file)
        root = tree.getroot()
        return root

    @staticmethod
    def save(obj: ET.Element, file):
        xml_str = ET.tostring(obj, encoding='utf-8')
        # Erzeuge eine formatierte Version des XML-Strings
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="\t")
        with Path(file).open('w') as f:
            f.write(pretty_xml)
