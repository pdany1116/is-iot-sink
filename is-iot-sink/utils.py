import xml.etree.ElementTree as ET

def get_setting(setting: str):
    file = open("./setup.xml")
    tree = ET.parse(file)
    root = tree.getroot() 
    if setting.startswith("./") == False:
        setting = "./" + setting
    return root.findall(setting)[0].text

def get_settings(settings: str):
    file = open("./setup.xml")
    tree = ET.parse(file)
    root = tree.getroot() 
    if settings.startswith("./") == False:
        settings = "./" + settings
    results = []
    for setting in list(root.find(settings)):
        results.append(setting.text)
    return results
