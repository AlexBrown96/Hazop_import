import gspread
import pickle
from oauth2client.service_account import ServiceAccountCredentials

# https://docs.google.com/spreadsheets/d/1B9ZVkqULJcgF_PpkMap1fGj-hAowC1EIhO4wVeY7LBg/edit?usp=sharing
# Generic Google drive API access
# Format:
# [Hazard][]
# [Undesired_event][]
# [Consequences][]...[Mitigations][m2][m3]...
# [C2]...
# [Threats][]...[Barriers][b2][b3]...
# [Threats]...
# ...
# [Hazard]...
#
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('jsonsecretdata.json', scope)
gc = gspread.authorize(creds)
wks = gc.open("HAZOP_DATA").worksheet('Sheet3')

# Find guide words and deviation words from columns in HAZOP spreadsheet
guide = wks.col_values(1)

temp_Threats = []
temp_Consq = []
temp_Hazards = []
data = []
num_Hazards = 0
#Loop over the google sheets first row and write data such the data is
# [[Threats & Barriers][Consequences & Mitigations]][TE, HAZ]
for row, i in enumerate(guide, 1):
    if i == "Hazard":
        # Find the Hazard and top event
        temp_Hazards = [wks.cell(row, 2).value, wks.cell(row+1, 2).value]
        num_Hazards += 1
    if i == "Consequences":
        # Append the row in which Consequences is found,
        temp_Consq.append(wks.row_values(row)[1:])
    if i == "Threats":
        temp_Threats.append(wks.row_values(row)[1:])
        if wks.cell(row+1, 1).value != 'Threats':
            data.append([num_Hazards, temp_Hazards, temp_Consq, temp_Threats])
            temp_Consq = []
            temp_Threats = []

print(data
      )
with open('Data.p', 'wb') as fp:
    pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
