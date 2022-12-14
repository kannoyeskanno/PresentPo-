import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import time
from main import DemoApp as a

scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Attendance').sheet1

def checkDate():
    cell = sheet.find(date.today().strftime('%B %d %Y'))
    if cell is not None:
        return cell.col

def checkName():
    cell = sheet.find(name)
    if cell is not None:
        return cell.row

def updateSheet():
    sheet.update_cell(checkName(), checkDate(), time.strftime("%I : %M %p"))


updateSheet()

