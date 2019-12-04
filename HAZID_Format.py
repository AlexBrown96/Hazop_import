import gspread
import pickle
from oauth2client.service_account import ServiceAccountCredentials
import time
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

temp = []
# Construct
num_Haz = len(Hazards)-1
for key in range(1, num_Haz+1):

    # Get slice
    # Ensure the last slice is obtained
    # temp.append([[Undesired_events[key], Hazards[key]],
    #              [Consequences[key], temp_Mits[key]],
    #              [Threats[key], temp_Bars[key]]])
    temp.append([[wks.cell(key+1, 2).value, wks.cell(key+1, 3).value],
                 [wks.cell(key+1, 4).value, wks.cell(key+1, 5).value],
                 [wks.cell(key+1, 6).value, wks.cell(key+1, 7).value]])

with open('Data.p', 'wb') as fp:
    pickle.dump(temp, fp, protocol=pickle.HIGHEST_PROTOCOL)
