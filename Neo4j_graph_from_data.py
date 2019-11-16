from py2neo import Graph, Node, Relationship
import pickle
import pprint

# MATCH (n) DETACH DELETE n
# Threats created from Spreadsheet, order is Threat then the barriers

Undesired_event = Node("Undesired_event", name="Loss of containment of liquid")
with open('Threats.p', 'rb') as fp:
    Threats = pickle.load(fp)
with open('Consequences.p', 'rb') as fp:
    Consequences = pickle.load(fp)
with open('Undesired_events.p', 'rb') as fp:
    Undesired_events = pickle.load(fp)
with open('Hazards.p', 'rb') as fp:
    Hazards = pickle.load(fp)

graph = Graph(password="mAES12081604")


def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


# for key in Threats.items():
#     Threats_flat.append(flatten(key))


for event, e in enumerate(Undesired_events):
    TE_node = Node("Top Event", name=Undesired_events[event])
    # Create hazard
    HAZ_node = Node("Hazard", name=Hazards[event])
    # link hazard to top event
    HAZ = Relationship.type("Hazard")
    graph.merge(HAZ(HAZ_node, TE_node), "Undesired_event", "name")
    for item, i in enumerate(Threats_flat):
        print(Threats_flat[item])


        # TODO connect last barrier to top event here
        # TODO iterate over these threats and produce barriers
        # TODO iterate over consq as well and do the same
