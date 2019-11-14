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

print(Top_events)

graph = Graph(password="mAES12081604")
for event, e in enumerate(Top_events):
    TE_node = Node("Top Event", name=Top_events[event])
    # Create hazard
    HAZ_node = Node("Hazard", name=Hazards[event])
    # link hazard to top event
    HAZ = Relationship.type("Hazard")
    graph.merge(HAZ(HAZ_node, TE_node), "Top_event", "name")
    for i in Threats:
        print(i, Threats[i])
        #TODO iterate over these threats and produce barriers
        #TODO iterate over consq as well and do the same 
