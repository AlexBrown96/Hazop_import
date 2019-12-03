from py2neo import Graph, Node, Relationship
import pickle
import time
# MATCH (n) DETACH DELETE n
# Threats created from Spreadsheet, order is Threat then the barriers

with open('Data.p', 'rb') as fp:
    Data = pickle.load(fp)
graph = Graph("bolt://localhost:7687", password="mAES12081604")

### TODO This line of code erases the current graph if it exists. Comment it out if this is not required
graph.run("MATCH (n) DETACH DELETE n")
###

for event, row in enumerate(Data):
    HAZ_node = Node("Hazard", name=("Hazard: "+row[1][0]))
    TE_node = Node("Undesired_event", name=("Undesired_event: "+row[1][1]))
    HAZ = Relationship.type("Hazard")
    CONSQ = Relationship.type("Consequence")
    THREAT = Relationship.type("Threat")
    graph.merge(HAZ(HAZ_node, TE_node), "Undesired_event", "name")
    for i, consq_row in enumerate(row[2]):
        if "Mitigations" in consq_row:
            consq_row.remove("Mitigations")
        num_Consq = len(row[2][i])
        Consq_node = Node("Consequence", name=(consq_row[0]))
        if len(consq_row) == 1:
            graph.merge(CONSQ(Consq_node, TE_node), "Consequence", "name")
        elif len(consq_row) > 1:
            for num, val in enumerate(consq_row):
                if 1 <= num < (len(consq_row)):
                    MIT = Relationship.type("Mitigation")
                    MIT_node = Node("Mitigation", name=val)
                    # print(num)
                    MIT_node2 = Node("Mitigation", name=(consq_row[num-1]))
                    graph.merge(MIT(MIT_node2, MIT_node), "Mitigation", "name")
                if num == len(consq_row)-1:
                    # print(consq_row[num])
                    MIT_node3 = Node("Mitigation", name=(consq_row[num]))
                    graph.merge(CONSQ(MIT_node3, TE_node), "Mitigation", "name")

    for j, threat_row in enumerate(row[3]):
        if "Barriers" in threat_row:
            threat_row.remove("Barriers")
        num_threat = len(row[3][j])
        Threat_node = Node("Threat", name=(threat_row[0]))
        if len(threat_row) == 1:
            graph.merge(THREAT(Threat_node, TE_node), "Threat", "name")
        elif len(threat_row) > 1:
            for num, val in enumerate(threat_row):
                if 1 <= num < (len(threat_row)):
                    BAR = Relationship.type("Barrier")
                    BAR_node = Node("Barrier", name=val)
                    BAR_node2 = Node("Barrier", name=(threat_row[num-1]))
                    graph.merge(BAR(BAR_node2, BAR_node), "Barrier", "name")
                if num == len(threat_row)-1:
                    BAR_node3 = Node("Barrier", name=(threat_row[num]))
                    graph.merge(THREAT(BAR_node3, TE_node), "Barrier", "name")

# time.sleep(10)
# graph.run("MATCH (n) RETURN n LIMIT 40")