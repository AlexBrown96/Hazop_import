from py2neo import Graph, Node, Relationship
import pickle
# MATCH (n) DETACH DELETE n
# Threats created from Spreadsheet, order is Threat then the barriers

with open('Data.p', 'rb') as fp:
    Data = pickle.load(fp)

graph = Graph("bolt://localhost:11012", password="12345")

for event, row in enumerate(Data):
    HAZ_node = Node("Hazard", name=("Hazard: "+row[1][0]+" id: "+str(event)))
    TE_node = Node("Undesired_event", name=("Undesired_event: "+row[1][1]+" id: "+str(event)))
    HAZ = Relationship.type("Hazard")
    CONSQ = Relationship.type("Consequence")
    THREAT = Relationship.type("Threat")
    graph.merge(HAZ(HAZ_node, TE_node), "Undesired_event", "name")
    for i, consq_row in enumerate(row[2]):
        if "Mitigations" in consq_row:
            consq_row.remove("Mitigations")
        num_Consq = len(row[2][i])
        Consq_node = Node("Consequence", name=(consq_row[0]+" id: "+str(event)))
        if len(consq_row) == 1:
            graph.merge(CONSQ(Consq_node, TE_node), "Consequence", "name")
        elif len(consq_row) > 1:
            for num, val in enumerate(consq_row):
                if 1 <= num < (len(consq_row)):
                    MIT = Relationship.type("Mitigation")
                    MIT_node = Node("Mitigation", name=(val+" id: "+str(event)))
                    # print(num)
                    MIT_node2 = Node("Mitigation", name=(consq_row[num-1]+" id: "+str(event)))
                    graph.merge(MIT(MIT_node2, MIT_node), "Mitigation", "name")
                if num == len(consq_row)-1:
                    # print(consq_row[num])
                    MIT_node3 = Node("Mitigation", name=(consq_row[num]+" id: "+str(event)))
                    graph.merge(CONSQ(MIT_node3, TE_node), "Mitigation", "name")

    for j, threat_row in enumerate(row[3]):
        if "Barriers" in threat_row:
            threat_row.remove("Barriers")
        num_threat = len(row[3][j])
        Threat_node = Node("Threat", name=(threat_row[0]+" id: "+str(event)))
        if len(threat_row) == 1:
            graph.merge(THREAT(Threat_node, TE_node), "Threat", "name")
        elif len(threat_row) > 1:
            for num, val in enumerate(threat_row):
                if 1 <= num < (len(threat_row)):
                    BAR = Relationship.type("Barrier")
                    BAR_node = Node("Barrier", name=(val+" id: "+str(event)))
                    BAR_node2 = Node("Barrier", name=(threat_row[num-1]+" id: "+str(event)))
                    graph.merge(BAR(BAR_node2, BAR_node), "Barrier", "name")
                if num == len(threat_row)-1:
                    BAR_node3 = Node("Barrier", name=(threat_row[num]+" id: "+str(event)))
                    graph.merge(THREAT(BAR_node3, TE_node), "Barrier", "name")
