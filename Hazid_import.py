import gspread
import pickle
from oauth2client.service_account import ServiceAccountCredentials
from py2neo import Graph, Node, Relationship
from collections import defaultdict

## TODO ; Create a non local host for the graph database
# graph = Graph(password="mAES12081604")

# https://docs.google.com/spreadsheets/d/1B9ZVkqULJcgF_PpkMap1fGj-hAowC1EIhO4wVeY7LBg/edit?usp=sharing
# Generic Google drive API access
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('jsonsecretdata.json', scope)
gc = gspread.authorize(creds)
wks = gc.open("HAZOP_DATA").worksheet('Sheet3')

# Find guide words and deviation words from columns in HAZOP spreadsheet
guide = wks.col_values(1)

temp_Threats = []
temp_Consq = []
data = []
num_Hazards = 0
for row, i in enumerate(guide, 1):
    if i == "Hazard":
        temp_Hazards = [wks.cell(row, 2).value, wks.cell(row+1, 2).value]
        num_Hazards += 1
    if i == "Consequences":
        temp_Consq.append(wks.row_values(row)[1:])
        # temp_Consq.remove("Mitigations")
    if i == "Threats":
        temp_Threats.append(wks.row_values(row)[1:])
        # temp_Threats.remove("Barriers")
        if wks.cell(row+1, 1).value != 'Threats':
            # print([num_Hazards, temp_Hazards,temp_Consq,temp_Threats])
            data.append([num_Hazards, temp_Hazards,temp_Consq,temp_Threats])
            temp_Consq = []
            temp_Threats = []

with open('Data.p', 'wb') as fp:
    pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
