import os
import json
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.PyQt.QtGui import QIcon
import shutil
from qgis.core import QgsVectorLayer, QgsProject

plugin_dir = os.path.dirname(__file__)

class BasemapLoaderPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        # --------------------- Add Layers
        icon = os.path.join(os.path.join(plugin_dir, 'logo.png'))
        self.action_add_layers = QAction(QIcon(icon), 'Add Layers', self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action_add_layers)
        self.action_add_layers.triggered.connect(self.add_layers)
        # --------------------- Export JSON
        icon = os.path.join(os.path.join(plugin_dir, 'logo.png'))
        self.action_export_json = QAction(QIcon(icon), 'Export JSON', self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action_export_json)
        self.action_export_json.triggered.connect(self.export_json)


    def unload(self):
        self.iface.removeToolBarIcon(self.action_add_layers)
        del self.action_add_layers
        self.iface.removeToolBarIcon(self.action_export_json)
        del self.action_export_json
        
    def add_layers(self):
        filename_details = QFileDialog.getSaveFileName(None, "Select output file ","", '*.gpkg')
        # catch cancel being pressed
        if not filename_details[0]:
            return
        # Get new filenme
        filename = filename_details[0] + ".gpkg"
        # Copy template to desired location
        shutil.copyfile(os.path.join(plugin_dir, "template.gpkg"), filename)
        # Add vector Layers for it 
        vector_layers = [
            QgsVectorLayer(filename+"|layername=networks", "Networks",  "ogr"),
            QgsVectorLayer(filename+"|layername=nodes", "Nodes",  "ogr"),
            QgsVectorLayer(filename+"|layername=spans", "Spans",  "ogr"),
            QgsVectorLayer(filename+"|layername=phases", "Phases",  "ogr"),
            QgsVectorLayer(filename+"|layername=spans_networkProviders", "spans_networkProviders",  "ogr"),
            QgsVectorLayer(filename+"|layername=phases_funders", "phases_funders",  "ogr"),
            QgsVectorLayer(filename+"|layername=organisations", "organisations",  "ogr"),
            QgsVectorLayer(filename+"|layername=nodes_networkProviders", "nodes_networkProviders",  "ogr"),
            QgsVectorLayer(filename+"|layername=nodes_internationalConnections", "nodes_internationalConnections",  "ogr"),
            QgsVectorLayer(filename+"|layername=links", "links",  "ogr"),
            QgsVectorLayer(filename+"|layername=contracts_relatedPhases", "contracts_relatedPhases",  "ogr"),
            QgsVectorLayer(filename+"|layername=contracts_documents", "contracts_documents",  "ogr"),
            QgsVectorLayer(filename+"|layername=contracts", "contracts",  "ogr"),
        ]
        for vector_layer in vector_layers:
            QgsProject.instance().addMapLayer(vector_layer)
    
    def export_json(self):
        filename_details = QFileDialog.getSaveFileName(None, "Select output file ","", '*.json')
        # catch cancel being pressed
        if not filename_details[0]:
            return
        # Get new filenme
        filename = filename_details[0] + ".json"
        # Make JSON
        out = {}
        for k,v in QgsProject.instance().mapLayers().items():
            print(v)
            # TODO
        
        # Save JSON
        with open(filename, "w") as fp:
            json.dump(out, fp, indent=2)
