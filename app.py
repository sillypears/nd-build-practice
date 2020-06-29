import os, sys
import xml.etree.ElementTree as ET
from pprint import pprint

from config import app_config

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

ALLOWED_ITEMS = ["weapon", "scroll", "armor", "feet", "head", "bag", "misc", "hud", "spell", "charm", "ring", "shovel", "pickaxe", "throwing", "familiar", "tome", "torch", "holy"]
ITEMS_TO_ADD = {
    "shovel": [],
    "weapon": [],
    "body": [],
    "misc": [],
    "feet": [],
    "ring": [],
    "torch": [],
    "spell": []
}

class Ui_MainWindow(object):
    def setup_ui(self, MainWindow, items, config):
        self.item_dict = items
        MainWindow.setObjectName("Ahhh")
        MainWindow.resize(480, 240)

        base = 20
        offset = 40
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralpark")
        self.items = QComboBox(self.centralwidget)
        self.items.resize(200, 40)
        self.items.move(base+1, base)
        self.items.setObjectName("items")
        self.items.setPlaceholderText("Items")
        c = 0
        for i in self.item_dict:
            if items[i]["index"].split("_")[0] in ALLOWED_ITEMS:
                self.items.addItem(items[i]["name"])
                self.items.setItemData(c, self.item_dict[i]["index"])
                self.items.setItemIcon(c, QIcon(os.path.join(items[i]["path"])))
                # print(self.item_dict[i]["path"])
                self.items.setIconSize(QSize(self.item_dict[i]["imageW"], self.item_dict[i]["imageH"]))
                c += 1

        self.addButton = QPushButton("Add!", self.centralwidget)
        self.addButton.resize(80, 40)
        self.addButton.move(base, (base+offset+1))
        self.addButton.clicked.connect(self.add_button_clicked)
        
        self.removeButton = QPushButton("Remove :(", self.centralwidget)
        self.removeButton.resize(80, 40)
        self.removeButton.move(base+(offset*2), (base+offset+1))
        self.removeButton.clicked.connect(self.remove_button_clicked)
        
        self.buildButton = QPushButton("Build!", self.centralwidget)
        self.buildButton.resize(80, offset)
        self.buildButton.move(base, (base+(offset*2)+1))

    def add_button_clicked(self):
        if self.items.currentData() != "Items":
            print(f"Adding {self.items.currentData()}")
            ITEMS_TO_ADD[self.item_dict[self.items.currentData()]["slot"]] = self.item_dict[self.items.currentData()]
            pprint(ITEMS_TO_ADD, indent=4)

    def remove_button_clicked(self):
        if self.items.currentData() != "Items":
            print(f"Removing {self.items.currentData()}")
            ITEMS_TO_ADD[self.item_dict[self.items.currentData()]["slot"]] = []
            pprint(ITEMS_TO_ADD, indent=4)

    def build_button_clicked(self):
        pass

def get_items_from_xmldata(f, l):
    """get_items_from_xmldata builds out a dictionary with items from the xml file

    Args:
        f (Element): This is the data from the xml for items   
        l (str): This is the path to the folder that houses the data for images and xml file

    Returns:
        dict: dict containing the processed data from the items section of the xml file
    """
    items = {}
    for i in f:
        imageH = 24
        imageW = 24
        slot = ""
        for a in i.attrib:
            if a == "flyaway":
                try:
                    n = i.attrib[a].split("|")[2]
                except IndexError:
                    n = i.attrib[a]
            if a == "imageW":
                imageW = int(i.attrib[a])
            if a == "imageH":
                imageH = int(i.attrib[a])
            if a == "slot":
                slot = i.attrib[a]

        items[i.tag] = {
            "path": os.path.join(l, i.text),
            "filename": i.text,
            "name": n.title(),
            "index": i.tag,
            "imageH": imageH,
            "imageW": imageW,
            "slot": slot
        }
    return items

def main():
    try:
        if os.environ["BUILD_ENV"] == "prod" or os.path.exists("release.version"):
            config = app_config["prod"]
        else:
            config = app_config["dev"]
    except:
        config = app_config["dev"]
    print(os.path.join(config.ND_FOLDER, config.DATA_FOLDER, "necrodancer.xml"))
    nd_xml = ET.parse(os.path.join(config.ND_FOLDER, config.DATA_FOLDER, "necrodancer.xml")).getroot()
    xml_enums = {
        "items": 0,
        "enemies": 1,
        "characters": 2,
        "modes": 3,
    }
    items = get_items_from_xmldata(nd_xml[xml_enums["items"]], os.path.join("data", "edited"))
 
    app = QApplication([])
    app.setObjectName("Build Practice")

    # MainWindow = QMainWindow()
    window = QWidget()  
    window.setWindowTitle("NecroDancer Build Practice")
    ui = Ui_MainWindow()
    ui.setup_ui(window, items, config)
    window.show()  
    app.exec_()

if __name__ == "__main__":
    sys.exit(main())