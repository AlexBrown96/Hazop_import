from py2neo import Graph, Node, Relationship
import pickle
# MATCH (n) DETACH DELETE n
# Threats created from Spreadsheet, order is Threat then the barriers

with open('Data.p', 'rb') as fp:
    Data = pickle.load(fp)

graph = Graph("bolt://localhost:11002", password="12345")

for event, row in enumerate(Data):
    HAZ_node = Node("Hazard", name=(row[1][0]+" id: "+str(event)))
    TE_node = Node("Top_event", name=row[1][1]+" id: "+str(event))
    HAZ = Relationship.type("Hazard")
    graph.merge(HAZ(HAZ_node, TE_node), "Top_event", "name")
    for i, consq_row in enumerate(row[2]):
        if "Mitigations" in consq_row:
            consq_row.remove("Mitigations")
        num_Consq = len(row[2][i])
        print(consq_row, num_Consq)
        if num_Consq == 1:
            #If there is no Mitigations attach to top event
            CONSEQUENCE = Relationship.type("Consequence")
            graph.merge(CONSEQUENCE(Node("Consequence", name=consq_row[0]+" id: "+str(event)), TE_node),
                        "Consequence", "name")
        elif num_Consq > 1:
            for count in range(num_Consq):
                MIT_node = Node("Mitigation", name=consq_row[count])
                if (count < num_Consq)-1:
                    MITIGATION = Relationship.type("Mitigation")
                    graph.merge(MITIGATION(MIT_node, Node("Mitigation", name=consq_row[count - 1]+" id: "+str(event))),
                                "Mitigation", "name")
                elif count == num_Consq - 1:
                    CONSEQUENCE = Relationship.type("Consequence")
                    graph.merge(CONSEQUENCE(Node("Consequence", name=(consq_row[-1]+" id: "+str(event))), TE_node),
                                "Consequence", "name")

    for j, threat_row in enumerate(row[3]):
        if "Barriers" in threat_row:
            threat_row.remove("Barriers")
        num_threat = len(row[3][j])
        if num_threat == 1:
            #If there is no Barriers attach to top event
            THREAT = Relationship.type("Threat")
            graph.merge(THREAT(Node("Threat", name=threat_row[0]+" id: "+str(event)), TE_node),
                        "Threat", "name")
        elif num_threat > 1:
            for count in range(num_threat):
                if count < num_threat - 1:
                    BAR_node = Node("Barrier", name=threat_row[count])
                    BARRIER = Relationship.type("Barrier")
                    graph.merge(BARRIER(BAR_node, Node("Threat", name=threat_row[count - 1]+" id: "+str(event))),
                                "Barrier", "name")
                elif count == num_threat - 1:
                    THREAT = Relationship.type("Threat")
                    graph.merge(THREAT(Node("Threat", name=(threat_row[-1]+" id: "+str(event))), TE_node),
                                "Threat", "name")



