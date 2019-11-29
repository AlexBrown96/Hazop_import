import gspread
import pickle
from oauth2client.service_account import ServiceAccountCredentials

# https://docs.google.com/spreadsheets/d/1B9ZVkqULJcgF_PpkMap1fGj-hAowC1EIhO4wVeY7LBg/edit?usp=sharing
# Generic Google drive API access
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('jsonsecretdata.json', scope)
gc = gspread.authorize(creds)
wks = gc.open("HAZOP_DATA").worksheet('HAZID_CEXC')
hazid_wks = gc.open("HAZOP_DATA").worksheet('HAZID')

Procedures = wks.col_values(1)
Hazards = wks.col_values(2)
Undesired_events = wks.col_values(3)
Consequences = wks.col_values(4)
Threats = wks.col_values(6)
temp_Mits = wks.col_values(5)
temp_Bars = wks.col_values(7)
temp_guide = []
Consq = []
Bar = []
# TODO process this file in the same way Hazard_import does

guide = wks.col_values(2)
guide_length = len(guide)
wks.update_cell(guide_length+1, 2, "'")



for i, Mitigation in enumerate(temp_Mits):
    temp_Consq = Consequences[i]
    # print(Mitigation)
    if "." in Mitigation:
        temp = list(filter(None, Mitigation.split(".")))
    else:
        temp = Mitigation
    Consq.append([temp_Consq, temp])

for j, Barrier in enumerate(temp_Bars):
    temp_Threats = Threats[j]
    if "." in Barrier:
        temp1 = list(filter(None, Barrier.split(".")))
    else:
        temp1 = Barrier
    Bar.append([temp_Threats, temp1])

for i in range(1, guide_length):
    temp_guide.append([[wks.cell(i+1, 1).value + ": " + guide[i], wks.cell(i+1, 3).value], Bar[i], Consq[i]])

print(temp_guide)


# hazid_wks.update_cell(j+1, i+1, wks.cell(j+1, i+1).value)