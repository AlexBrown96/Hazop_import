import pandas as pd
import numpy as np
from pathlib import Path
from Neo4j import data_to_neo4j
import networkx as nx
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 9))

class BowtieDataError(Exception):
    pass


class Bowtie:
    graph = nx.DiGraph()

    def __init__(self, data):
        self.hazard = data.hazard.dropna().iloc[0]
        self.undesired_event = data.undesired_event.dropna().iloc[0]
        self.consequences = data.consequences.fillna("None")
        self.mitigations = data.mitigations.fillna("None")
        self.threats = data.threats.fillna("None")
        self.barriers = data.barriers.fillna("None")
        self.bowtie_id = data.index[0]

    def create_bowtie(self):
        threats_bars = dict(zip(self.threats, [bar.split(",") for bar in self.barriers]))
        consequences_mits = dict(zip(self.consequences, [mit.split(",") for mit in self.mitigations]))
        width = len(sum([bar.split(",") for bar in self.barriers], [])) + len(self.threats) + \
            len(sum([mit.split(",") for mit in self.mitigations], [])) + len(self.consequences)
        hazards_ue = [self.hazard, self.undesired_event, self.bowtie_id]
        Bowtie.connect_nodes(branch=threats_bars, master=hazards_ue, labels=["threat", "barrier"], width=width)
        Bowtie.connect_nodes(branch=consequences_mits, master=hazards_ue, labels=["consequence", "mitigation"], width=width)
        pos = nx.multipartite_layout(Bowtie.graph, subset_key="layer")
        nx.draw_networkx_nodes(Bowtie.graph, pos, node_size=750)
        nx.draw_networkx_edges(Bowtie.graph, pos, edgelist=Bowtie.graph.edges(), edge_color="grey")
        nx.draw_networkx_labels(Bowtie.graph, pos, font_size=12, verticalalignment="top")
        plt.show()

    @classmethod
    def connect_nodes(cls, branch: dict, master: list, labels: list, width: int = 8):
        if labels == ["threat", "barrier"]:
            layer = 0
            itt = 1
        elif labels == ["consequence", "mitigation"]:
            layer = width
            itt = -1
        else:
            layer = 0
            itt = 0
        if width % 2 == 0: width += 1
        start_layer = layer
        Bowtie.graph.add_node(master[1], layer=width/2) # undesired event
        Bowtie.graph.add_node(master[0], layer=width/2) # hazard
        Bowtie.graph.add_edge(master[0], master[1])
        for parent, children in branch.items():
            if children != "None":
                current_node = parent
                Bowtie.graph.add_node(current_node, label=labels[0], layer=layer)
                for child in children:
                    layer += itt
                    Bowtie.graph.add_node(child, label=labels[1], layer=layer)
                    Bowtie.graph.add_edge(current_node, child)
                    current_node = child
                    # TODO below nodes need creating and layering
                layer += itt
                Bowtie.graph.add_edge(current_node, master[0])
            layer = start_layer
        Bowtie.graph.add_node(master[2], layer=width/2) # bowtie id

    @staticmethod
    def organise_data(bowtie_csv: str or object = None) -> object:
        '''
        :param bowtie_csv: Input=file name or file name.csv or file location
        :return: Valid bowtie_csv is returned.
        '''
        if isinstance(bowtie_csv, str):
            if ".csv" not in bowtie_csv:
                try:
                    bowtie_csv = pd.read_csv(bowtie_csv + ".csv")
                except FileNotFoundError:
                    bowtie_csv = pd.DataFrame()
            else:
                try:
                    bowtie_csv = pd.read_csv(bowtie_csv)
                except FileNotFoundError:
                    bowtie_csv = pd.DataFrame()
        heads = ["bowtie_id", "hazard", "undesired_event",
                 "consequences", "mitigations",
                 "threats", "barriers",
                 "consq_severity", "event_likelihood", "consq_rating",
                 "threat_severity", "threat_likelihood", "threat_rating"]
        bowtie_csv = pd.DataFrame(bowtie_csv)
        if bowtie_csv.empty:
            if not Path("../Hazop_import/hazid_format_example.csv").is_file():
                data_descriptions = {"bowtie_id": "alphanumeric id",
                                     "hazard": "Somthing within the organisation that has the potential to cause harm",
                                     "undesired_event": "Deviation caused by loss of control of hazard, does not describe damage",
                                     "consequence": "Description of a single outcome of the undesired event",
                                     "threat": "Action that may cause the undesired event",
                                     "mitigations": "soft or hard features of the system that prevent or minimise the effect of the consequence. Separate items with ','",
                                     "barriers": "soft or hard features of the system that prevent or minimise the chance of the undesired event occurring. Separate items with ','"}
                pd.DataFrame(data_descriptions, index=[0], columns=heads).fillna("values gathered from risk matrix").set_index(
                    "bowtie_id").to_csv("hazid_format_example.csv")
            else:
                raise BowtieDataError("See hazid_format_example.csv for construction of bowtie_csv")
        else:
            bowtie_csv.columns = heads
            return bowtie_csv.set_index("bowtie_id")

    @staticmethod
    def export_data_to_neo4j(bowtie_csv):
        bowtie_data = Bowtie.organise_data(bowtie_csv)
        data_to_neo4j(bowtie_data)

    @staticmethod
    def label_maker(labels):
        for l in labels:
            if len(labels[l]) > 55:
                indices = [i for i, x in enumerate(list(labels[l])) if x == ' ']
                indices = np.asarray(indices)
                try:
                    idx = indices[indices > 55][0]
                    newlabel = list(labels[l])
                    newlabel.insert(idx, ' \n')
                    newlabel = ''.join(newlabel)
                    labels[l] = newlabel
                except:
                    continue


if __name__ == "__main__":
    data2 = Bowtie.organise_data("hazid_test_file")
    bt2 = data2.loc[1]
    a = Bowtie(bt2).create_bowtie()