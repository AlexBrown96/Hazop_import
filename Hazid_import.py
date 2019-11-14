import gspread
import pickle
from oauth2client.service_account import ServiceAccountCredentials
from py2neo import Graph, Node, Relationship
from collections import defaultdict

## TODO ; Create a non local host for the graph database
graph = Graph(password="mAES12081604")

# https://docs.google.com/spreadsheets/d/1B9ZVkqULJcgF_PpkMap1fGj-hAowC1EIhO4wVeY7LBg/edit?usp=sharing
# Generic Google drive API access
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('jsonsecretdata.json', scope)
gc = gspread.authorize(creds)
wks = gc.open("HAZOP_DATA").sheet1

# Find guide words and deviation words from columns in HAZOP spreadsheet
guide = wks.col_values(1)


Hazards = []
Barriers = []
Top_events = []
Consq = []
Threats = []
for row, e in enumerate(guide):
    if guide[row] == "Hazard":
        Hazards.append(wks.cell(row+1, 2).value)
    elif guide[row] == "Top_event":
        Top_events.append(wks.cell(row+1, 2).value)
    elif guide[row] == "Causes":
        temp_Causes = (wks.row_values(row+1))
        num_Causes = len(temp_Causes)
    elif guide[row] == "Barriers":
        for i in range(num_Causes):
            # print(wks.cell(row+1, i+1))
            if temp_Causes[i] != "Causes":
                # print(temp_Causes[i])
                # print(wks.cell(row+1, i+1).value)
                Threats.append([temp_Causes[i], wks.cell(row+1, i+1).value])
    elif guide[row] == "Consequences":
        temp_Conq = (wks.row_values(row+1))
        num_Conq = len(temp_Conq)
    elif guide[row] == "Mitigations":
        for i in range(num_Conq):
            if temp_Conq[i] != "Consequences":
                # print(temp_Conq[i])
                Consq.append([temp_Conq[i], wks.cell(row+1, i+1).value])

Threats_Out = defaultdict(list)
for key, val in Threats:
    Threats_Out[key].append(val)
Threats = dict(Threats_Out)

Consq_Out = defaultdict(list)
for key, val in Consq:
    Consq_Out[key].append(val)
Consq = dict(Consq_Out)
with open('Threats.p', 'wb') as fp:
    pickle.dump(Threats, fp, protocol=pickle.HIGHEST_PROTOCOL)
with open('Consequences.p', 'wb') as fp:
    pickle.dump(Consq, fp, protocol=pickle.HIGHEST_PROTOCOL)
with open('Top_events.p', 'wb') as fp:
    pickle.dump(Top_events, fp, protocol=pickle.HIGHEST_PROTOCOL)
with open('Hazards.p', 'wb') as fp:
    pickle.dump(Hazards, fp, protocol=pickle.HIGHEST_PROTOCOL)