import os, sys
import xml.etree.ElementTree as ET

from config import app_config

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

ALLOWED_ITEMS = ["weapon", "scroll", "armor", "feet", "head", "bag", "misc", "hud", "spell", "charm", "ring", "shovel", "pickaxe", "throwing", "familiar", "tome", "torch", "holy"]

class Ui_MainWindow(object):
    def setup_ui(self, MainWindow, items, config):
        MainWindow.setObjectName("Ahhh")
        MainWindow.resize(640, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralpark")
        self.items = QComboBox(self.centralwidget)
        self.items.resize(200, 40)
        self.items.move(10, 10)
        self.items.setObjectName("items")
        self.items.addItem("Items")
        c = 1
        for i in items:
            if items[i]["index"].split("_")[0] in ALLOWED_ITEMS:
                self.items.addItem(items[i]["name"])
                self.items.setItemIcon(c, QIcon(os.path.join(items[i]["path"])))
                print(items[i]["path"])
                self.items.setIconSize(QSize(items[i]["imageW"], items[i]["imageH"]))
                c += 1

def get_items_from_xmldata(f, l):
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
    # print(items)
    return items

if __name__ == "__main__":
    try:
        if os.environ["BUILD_ENV"] == "prod" or os.path.exists("release.version"):
            config = app_config["prod"]
        else:
            config = app_config["dev"]
    except:
        config = app_config["dev"]

    nd_xml = ET.parse(os.path.join(config.ND_FOLDER, "data", "necrodancer.xml")).getroot()
    xml_enums = {
        "items": 0,
        "enemies": 1,
        "characters": 2,
        "modes": 3,
    }
    items = get_items_from_xmldata(nd_xml[xml_enums["items"]], os.path.join(config.ND_FOLDER, "data", "edited"))

    app = QApplication([])
    # MainWindow = QMainWindow()
    window = QWidget()
    ui = Ui_MainWindow()
    ui.setup_ui(window, items, config)
    window.show()
    sys.exit(app.exec_())