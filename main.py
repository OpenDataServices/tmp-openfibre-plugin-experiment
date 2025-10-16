import os
import json
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.PyQt.QtGui import QIcon
import shutil
from qgis.core import QgsVectorLayer, QgsProject, QgsEditorWidgetSetup, QgsVectorLayer, QgsLayerTreeLayer

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
        # Create a group
        groupName="Open Fibre"
        root = QgsProject.instance().layerTreeRoot()
        group = root.addGroup(groupName)
        # Add vector Layers for it 
        networks = QgsVectorLayer(filename+"|layername=networks", "Networks",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(networks))
        QgsProject.instance().addMapLayer(networks, False)

        nodes = QgsVectorLayer(filename+"|layername=nodes", "Nodes",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(nodes))
        QgsProject.instance().addMapLayer(nodes, False)
        nodes.setEditorWidgetSetup(
            4, 
            QgsEditorWidgetSetup(
                'ValueMap',
                {'map': [{'Decommissioned': 'decommissioned'}, {'Inactive': 'inactive'}, {'Operational': 'operational'}, {'Planned': 'planned'}, {'Proposed': 'proposed'}, {'Under construction': 'underConstruction'}]}
            )
        )

        spans = QgsVectorLayer(filename+"|layername=spans", "Spans",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(spans))
        QgsProject.instance().addMapLayer(spans, False)

        phases = QgsVectorLayer(filename+"|layername=phases", "Phases",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(phases))
        QgsProject.instance().addMapLayer(phases, False)

        spans_networkProviders = QgsVectorLayer(filename+"|layername=spans_networkProviders", "spans_networkProviders",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(spans_networkProviders))
        QgsProject.instance().addMapLayer(spans_networkProviders, False)

        phases_funders = QgsVectorLayer(filename+"|layername=phases_funders", "phases_funders",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(phases_funders))
        QgsProject.instance().addMapLayer(phases_funders, False)

        organisations = QgsVectorLayer(filename+"|layername=organisations", "organisations",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(organisations))
        QgsProject.instance().addMapLayer(organisations, False)

        nodes_networkProviders = QgsVectorLayer(filename+"|layername=nodes_networkProviders", "nodes_networkProviders",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(nodes_networkProviders))
        QgsProject.instance().addMapLayer(nodes_networkProviders, False)

        nodes_internationalConnections = QgsVectorLayer(filename+"|layername=nodes_internationalConnections", "nodes_internationalConnections",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(nodes_internationalConnections))
        QgsProject.instance().addMapLayer(nodes_internationalConnections, False)

        links = QgsVectorLayer(filename+"|layername=links", "links",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(links))
        QgsProject.instance().addMapLayer(links, False)

        contracts_relatedPhases = QgsVectorLayer(filename+"|layername=contracts_relatedPhases", "contracts_relatedPhases",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(contracts_relatedPhases))
        QgsProject.instance().addMapLayer(contracts_relatedPhases, False)

        contracts_documents = QgsVectorLayer(filename+"|layername=contracts_documents", "contracts_documents",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(contracts_documents))
        QgsProject.instance().addMapLayer(contracts_documents, False)

        contracts = QgsVectorLayer(filename+"|layername=contracts", "contracts",  "ogr")
        group.insertChildNode(-1, QgsLayerTreeLayer(contracts))
        QgsProject.instance().addMapLayer(contracts, False)
    
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
