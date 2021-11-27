import xml.etree.ElementTree as ET

def getSetting(setting: str):
    file = open("./setup.xml")
    tree = ET.parse(file)
    root = tree.getroot() 
    result = root.iter(setting)
    return next(result).text