import os
import json
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.PyQt.QtGui import QIcon
import shutil
from qgis.core import QgsVectorLayer, QgsProject, QgsEditorWidgetSetup

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
        networks = QgsVectorLayer(filename+"|layername=networks", "Networks",  "ogr")
        QgsProject.instance().addMapLayer(networks)

        nodes = QgsVectorLayer(filename+"|layername=nodes", "Nodes",  "ogr")
        QgsProject.instance().addMapLayer(nodes)
        nodes.setEditorWidgetSetup(
            4, 
            QgsEditorWidgetSetup(
                'ValueMap',
                {'map': [{'Decommissioned': 'decommissioned'}, {'Inactive': 'inactive'}, {'Operational': 'operational'}, {'Planned': 'planned'}, {'Proposed': 'proposed'}, {'Under construction': 'underConstruction'}]}
            )
        )

        spans = QgsVectorLayer(filename+"|layername=spans", "Spans",  "ogr")
        QgsProject.instance().addMapLayer(spans)

        phases = QgsVectorLayer(filename+"|layername=phases", "Phases",  "ogr")
        QgsProject.instance().addMapLayer(phases)

        spans_networkProviders = QgsVectorLayer(filename+"|layername=spans_networkProviders", "spans_networkProviders",  "ogr")
        QgsProject.instance().addMapLayer(spans_networkProviders)

        phases_funders = QgsVectorLayer(filename+"|layername=phases_funders", "phases_funders",  "ogr")
        QgsProject.instance().addMapLayer(phases_funders)

        organisations = QgsVectorLayer(filename+"|layername=organisations", "organisations",  "ogr")
        QgsProject.instance().addMapLayer(organisations)

        nodes_networkProviders = QgsVectorLayer(filename+"|layername=nodes_networkProviders", "nodes_networkProviders",  "ogr")
        QgsProject.instance().addMapLayer(nodes_networkProviders)

        nodes_internationalConnections = QgsVectorLayer(filename+"|layername=nodes_internationalConnections", "nodes_internationalConnections",  "ogr")
        QgsProject.instance().addMapLayer(nodes_internationalConnections)

        links = QgsVectorLayer(filename+"|layername=links", "links",  "ogr")
        QgsProject.instance().addMapLayer(links)

        contracts_relatedPhases = QgsVectorLayer(filename+"|layername=contracts_relatedPhases", "contracts_relatedPhases",  "ogr")
        QgsProject.instance().addMapLayer(contracts_relatedPhases)

        contracts_documents = QgsVectorLayer(filename+"|layername=contracts_documents", "contracts_documents",  "ogr")
        QgsProject.instance().addMapLayer(contracts_documents)

        contracts = QgsVectorLayer(filename+"|layername=contracts", "contracts",  "ogr")
        QgsProject.instance().addMapLayer(contracts)
    
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
            if isinstance(v, QgsVectorLayer):
                print("LAYER {}".format(k))
                for f in v.getFeatures():
                    print("FEATURE")
                    for f_k, f_v in f.attributeMap().items():
                        # TODO actually have to turn this into the right structures
                        out[f_k] = str(f_v)
                    # TODO save f.geometry().asJson() for nodes and spans too
        # Save JSON
        with open(filename, "w") as fp:
            json.dump(out, fp, indent=2)
