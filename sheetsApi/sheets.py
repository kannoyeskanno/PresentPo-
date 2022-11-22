import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import time

scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
# scope = ["https://www.googleapis.com/auth/sprea...", "https://www.googleapis.com/auth/drive...", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Attendance').sheet1



# data_for_sheet_0 = sheet.get_worksheet(0)
# for i in sheet.col_values(1):
#     sheet.
#     print(sheet.define_named_range)
# word = "jomar"
# cell = sheet.find(word)
# key_X = cell.col
# key_Y = cell.row
# print(cell)
# print(key_X, key_Y)
# print(sheet.cell(2, 1))


def checkDate():
    cell = sheet.find(date.today().strftime('%B %d %Y'))
    if cell is not None:
        return cell.col

def checkName(word):
    cell = sheet.find(word)
    if cell is not None:
        return cell.row

def updateSheet():
    sheet.update_cell(checkName("asis"), checkDate(), time.strftime("%I : %M %p"))


updateSheet()

