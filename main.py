import os
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.PyQt.QtGui import QIcon
import shutil
from qgis.core import QgsVectorLayer, QgsProject

plugin_dir = os.path.dirname(__file__)

class BasemapLoaderPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        # Create an action (i.e. a button) with Logo
        icon = os.path.join(os.path.join(plugin_dir, 'logo.png'))
        self.action = QAction(QIcon(icon), 'Test', self.iface.mainWindow())
        # Add the action to the toolbar
        self.iface.addToolBarIcon(self.action)
        # Connect the run() method to the action
        self.action.triggered.connect(self.run)
      
    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action
        
    def run(self):
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
    
