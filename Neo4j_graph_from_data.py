from py2neo import Graph, Node, Relationship
import pickle
import time
# MATCH (n) DETACH DELETE n
# Threats created from Spreadsheet, order is Threat then the barriers

with open('Data.p', 'rb') as fp:
    Data = pickle.load(fp)
graph = Graph("bolt://localhost:11002", password="12345")

### TODO This line of code erases the current graph if it exists. Comment it out if this is not required
graph.run("MATCH (n) DETACH DELETE n")
### TODO do nodes need explicit labels?

for event, row in enumerate(Data):
    HAZ_node = Node("Hazard", name=("Hazard: "+row[0][0]))
    UE_node = Node("Undesired_event", name=("U_e: "+row[0][1]))
    HAZ = Relationship.type("Hazard")
    # CONSQ = Relationship.type("Consequence")
    THREAT = Relationship.type("Threat")
    temp_rel = Relationship(HAZ_node, "Undesired_Event", UE_node)
    graph.merge(temp_rel, "Undesired_event", "name")
    # graph.merge(HAZ(HAZ_node, UE_node), "Undesired_event", "name")
    Consq_node = Node("Consequence", name=(row[1][0]))
    Threat_node = Node("Threat", name=row[2][0])
# Consequences at mitigations

    if row[1][1] == '':
        # If there is no Mitigation, then connect to UE
        temp_rel = Relationship(Consq_node, "Consequence Severity rating: {}".format(row[2][2]), UE_node)
        graph.merge(temp_rel, "Consequence", "name")
    elif '.' not in row[1][1]:
        # If there is 1 Mitigation then Connect the mitigation to the UE and the Consq to the mitigation
        Mit_node = Node("Mitigation", name=(row[1][1]))
        temp_rel = Relationship(Consq_node, "Consequence Severity rating: {}".format(row[2][2]), Mit_node)
        temp_rel2 = Relationship(Mit_node, "Mitigation", UE_node)
        graph.merge(temp_rel, "Mitigation", "name")
        graph.merge(temp_rel2, "Mitigation", "name")
    elif '.' in row[1][1]:
        # If there is more than one Mitigation, split them up and chain them together. Length should always be > 2
        temp = list(filter(None, row[1][1].split('.')))
        for j in range(len(temp)):
            if j == 0:
                Mit_node = Node("Mitigation", name=temp[j])
                temp_rel = Relationship(Mit_node, "Consequence Severity rating: {}".format(row[2][2]), UE_node)
                graph.merge(temp_rel, "Mitigation", "name")
            elif j <= len(temp)-1:
                Mit_node = Node("Mitigation", name=temp[j])
                Mit_node2 = Node("Mitigation", name=temp[j-1])
                temp_rel = Relationship(Mit_node, "Mitigation", Mit_node2)
                graph.merge(temp_rel, "Mitigation", "name")
                if j == len(temp)-1:
                    temp_rel = Relationship(Consq_node, "Consequence", Mit_node)
                    graph.merge(temp_rel, "Consequence", "name")


    if row[2][1] == '':
        # If there is no Barrier, then connect to UE
        temp_rel = Relationship(Threat_node, "Threat severity: {}".format(row[2][3]), UE_node)
        graph.merge(temp_rel, "Threat", "name")
    elif '.' not in row[2][1]:
        # If there is 1 Barrier then Connect the barrier to the UE and the Threat to the barrier
        Bar_node = Node("Barrier", name=(row[2][1]))
        temp_rel = Relationship(Threat_node, "Threat severity: {}".format(row[2][3]), Bar_node)
        temp_rel2 = Relationship(Bar_node, "Barrier", UE_node)
        graph.merge(temp_rel, "Barrier", "name")
        graph.merge(temp_rel2, "Barrier", "name")
    elif '.' in row[2][1]:
        # If there is more than one Barrier, split them up and chain them together. Length should always be > 2
        temp = list(filter(None, row[2][1].split('.')))
        for j in range(len(temp)):
            if j == 0:
                Bar_node = Node("Barrier", name=temp[j])
                temp_rel = Relationship(Bar_node, "Threat severity: {}".format(row[2][3]), UE_node)
                graph.merge(temp_rel, "Barrier", "name")
            elif j <= len(temp):
                Bar_node = Node("Barrier", name=temp[j])
                Bar_node2 = Node("Barrier", name=temp[j-1])
                temp_rel = Relationship(Bar_node, "Barrier", Bar_node2)
                graph.merge(temp_rel, "Barrier", "name")
                if j == len(temp)-1:
                    temp_rel = Relationship(Threat_node, "Threat", Bar_node)
                    graph.merge(temp_rel, "Threat", "name")

