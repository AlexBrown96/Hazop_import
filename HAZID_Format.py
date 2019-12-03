import gspread
import pickle
from oauth2client.service_account import ServiceAccountCredentials
import itertools

# https://docs.google.com/spreadsheets/d/1B9ZVkqULJcgF_PpkMap1fGj-hAowC1EIhO4wVeY7LBg/edit?usp=sharing
# Generic Google drive API access
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('jsonsecretdata.json', scope)
gc = gspread.authorize(creds)
wks = gc.open("HAZOP_DATA").worksheet('HAZID_CEXC')

Procedures = wks.col_values(1)
Hazards = wks.col_values(2)
Undesired_events = wks.col_values(3)
Consequences = wks.col_values(4)
Threats = wks.col_values(6)
temp_Mits = wks.col_values(5)
temp_Bars = wks.col_values(7)
temp_guide = []
Consq = []
Threat = []
# TODO process this file in the same way Hazard_import does

guide = wks.col_values(2)
guide_length = len(guide)
wks.update_cell(guide_length + 1, 2, "'")

Haz_UE = []
flat_list = []
for i, e in enumerate(Hazards):
    Haz_UE.append([Hazards[i], Undesired_events[i]])

for i, Mitigation in enumerate(temp_Mits):
    temp_Consq = Consequences[i]
    if "." in Mitigation:
        temp = [[temp_Consq], list(filter(None, Mitigation.split(".")))]
        for sublist in temp:
            for item in sublist:
                flat_list.append(item)
        Consq.append(flat_list)
    else:
        temp = [temp_Consq, Mitigation]
        Consq.append(temp)
    flat_list = []

for j, Barrier in enumerate(temp_Bars):
    temp_Threats = Threats[j]
    if "." in Barrier:
        temp1 = [[temp_Threats], list(filter(None, Barrier.split(".")))]
        for sublist in temp1:
            for item in sublist:
                flat_list.append(item)
        Threat.append(flat_list)
    else:
        temp1 = [temp_Threats, Barrier]
        Threat.append(temp1)

data = []
for item in range(len(Hazards)):
    if item > 0:
        data.append([item, Haz_UE[item], [Consq[item]], [Threat[item]]])

for mylist in data:
    for sublist in mylist:
        if type(sublist) == type(list()):
            for key, val in enumerate(sublist[0]):
                if sublist[0][key] == '':
                    sublist[0].remove('')
print(data[15:19])

with open('Data.p', 'wb') as fp:
    pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
