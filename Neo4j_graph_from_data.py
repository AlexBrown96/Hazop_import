from py2neo import Graph, Node, Relationship
import pickle

# MATCH (n) DETACH DELETE n
# Threats created from Spreadsheet, order is Threat then the barriers

Top_event = Node("Top_event", name="Loss of containment of liquid")
with open('Threats.p', 'rb') as fp:
    Threats = pickle.load(fp)
with open('Consequences.p', 'rb') as fp:
    Consequences = pickle.load(fp)
with open('Top_events.p', 'rb') as fp:
    Top_events = pickle.load(fp)
with open('Hazards.p', 'rb') as fp:
    Hazards = pickle.load(fp)

# for threat in Threats:
#     print(Threats[threat][-1])
# breakpoint()
graph = Graph(password="mAES12081604")
for event, e in enumerate(Top_events):
    TE_node = Node("Top Event", name=Top_events[event])
    # Create hazard
    HAZ_node = Node("Hazard", name=Hazards[event])
    # link hazard to top event
    HAZ = Relationship.type("Hazard")
    graph.merge(HAZ(HAZ_node, TE_node), "Top_event", "name")
    for threat in Threats:
        temp_node = Node("Threat", name=threat)
        for bar, j in enumerate(Threats[threat]):
            # TODO connect barriers here
            if j != "":
                if bar == 0:
                    THREAT = Relationship.type("BARRIER")
                    temp_threat_node = Node("Barrier", name=j)
                    graph.merge(THREAT(temp_node, temp_threat_node), "Barrier", "name")
                elif bar < len(Threats[threat]):
                    # print(Threats[threat][bar])
                    BARRIER = Relationship.type("BARRIER")
                    temp_threat_node = Node("Barrier", name=Threats[threat][bar-1])
                    graph.merge(BARRIER(temp_threat_node, Node("Barrier", name=j)), "Barrier", "name")
                if bar == len(Threats[threat])-1:
                    THREAT = Relationship.type("THREAT")
                    graph.merge(THREAT(TE_node, Node("Barrier", name = Threats[threat][-1])), "Barrier", "name")

                # graph.merge(THREAT)
                # Threats[threat][bar]
                # THREAT = Relationship.type("THREAT")

        # TODO connect last barrier to top event here
        # TODO iterate over these threats and produce barriers
        # TODO iterate over consq as well and do the same
