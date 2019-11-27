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
wks = gc.open("HAZOP_DATA").worksheet('HAZID_CEXC')

for i in range(len(wks.col_values(1))):
    print(wks.cell(i+1,2))