import gspread
import pandas as pd
from py2neo import Graph, Node, Relationship

# TODO check depreciation of py2neo and neo4j
# try:
#     graph = Graph("bolt://localhost:7687", password="12345")
# except ConnectionError:
#     print("Cannot connect to NEO4j")
# graph_write = False
#graph = Graph()

def get_hazid_data(gc, wks):
    '''
    :param gc: gspread.authorize(creds)
    :param wks: "HAZID_CEXC"
    :return: returns google sheets as dataframe
    '''
    file = pd.DataFrame(gc.open("HAZOP_DATA").worksheet(wks).get_all_values())
    file.columns = file.iloc[0]
    file = file.drop(file.index[0])
    return file


def data_to_neo4j(file=None):
    # if file is None:
    #     file = get_hazid_data(gspread.authorize(creds), sheet_name)
    #     file[file == ""] = None
    for undesired_event in file.Undesired_event.unique():
        df_hazard = file[file["Undesired_event"] == undesired_event]
        connect_branch(dict(zip(df_hazard.Consequences, df_hazard.Mitigations)), undesired_event, "Consequence", "Mitigation")
        connect_branch(dict(zip(df_hazard.Threats, df_hazard.Barriers)), undesired_event, "Threat", "Barrier", swap=True)
        connect_branch(dict(zip(df_hazard.Hazard, df_hazard.Undesired_event)), undesired_event, "Hazard", "Undesired_event")


def connect_haz_ue(df, undesired_event=None):
    if undesired_event:
        haz_dict = dict(zip(df.Undesired_event, df.Hazard))
        for ue in haz_dict:
            rel = create_relationship(create_node("Hazard", haz_dict.get(ue)), create_node("Undesired_event", ue), "Hazard")
            if graph_write: graph.merge(rel, "Hazard", "name")


def connect_branch(branch_dict, undesired_event=None, name=None, labels=None, swap=False):
    for item in branch_dict:
        current_node = create_node(name, item)
        if branch_dict.get(item) and name != "Hazard":
            for val in branch_dict.get(item).split(","):
                bar_node = create_node(labels, val)
                rel = create_relationship(bar_node, current_node, labels, swap)
                graph.merge(rel, labels, "name")
                current_node = bar_node
        rel_final = create_relationship(create_node("Undesired_event", undesired_event), current_node , "Undesired_event", swap)
        if current_node:
            graph.merge(rel_final, "Undesired_event", "name")


def create_node(node=None, val=None):
    if node:
        if val:
            return Node(node, name=val)


def create_relationship(node1, node2, name=None, swap=False):
    if swap:
        node1, node2 = node2, node1
    if name:
        return Relationship(node1, name, node2)


def main():
    # TODO blank values do not work with connect branch func
    # TODO ignore blank df values
    data_to_neo4j(pd.read_csv("HAZID.csv"))


if __name__ == "__main__":
    main()

