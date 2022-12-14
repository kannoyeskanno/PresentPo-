from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import sqlite3

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import date
import time


from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.pickers import MDTimePicker

from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.audio import SoundLoader





scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Attendance').sheet1


class IntroScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class SignupScreen(Screen):
    pass


class HomeScreen(Screen):
    pass

class ScannerScreen(Screen):
    pass

class CreateClassScreen(Screen):
    pass

class ClassScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(IntroScreen(name="popup_screen"))
sm.add_widget(IntroScreen(name="intro_screen"))
sm.add_widget(LoginScreen(name="login_screen"))
sm.add_widget(SignupScreen(name="signup_screen"))
sm.add_widget(CreateClassScreen(name="create_class_screen"))


sm.add_widget(ScannerScreen(name="scanner_screen"))
sm.add_widget(ClassScreen(name="class_screen"))



class MainApp(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None

    def build(self):
        self.title = "Present Po!"
        self.icon = "presentpo_icon.png"
        self.theme_cls.theme_style = "Light"

        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("""CREATE TABLE if not exists users(
            email text,
            username text,
            password text)
        """)
        db.commit()
        db.close()
        return Builder.load_file('app.kv')

    def signup(self):
        db = sqlite3.connect('database.db')
        c = db.cursor()
        sql = ("INSERT INTO users(email, username, password) VALUES (?, ?, ?);")
        mydata = (self.root.get_screen("signup_screen").ids.signup_email.text, self.root.get_screen("signup_screen").ids.signup_username.text, self.root.get_screen("signup_screen").ids.signup_password.text)
        c.execute(sql, mydata)
        self.root.current = "home_screen"
        self.root.get_screen("home_screen").ids.username.text = self.root.get_screen("signup_screen").ids.signup_username.text
        db.commit()
        db.close()

    def login(self):
        db = sqlite3.connect('database.db')
        c = db.cursor()

        username = self.root.get_screen("login_screen").ids.login_username.text
        password = self.root.get_screen("login_screen").ids.login_password.text

        c.execute("SELECT * FROM users")
        records = c.fetchall()


        for i in records:
            if i[1] == username and i[2] == password:
                self.root.current = "home_screen"
                self.root.get_screen("home_screen").ids.username.text = f"                                        {username}"
                break
            elif i[1] == username and i[2] != password or i[1] != username and i[2] == password:
                self.show_login_denied_dialog()
        db.commit()
        db.close()


    def get_qr_value(self):
        if str(self.root.get_screen("scanner_screen").ids.qr.text).strip("b'") != '':
            self.update_sheet(str(self.root.get_screen("scanner_screen").ids.qr.text).strip("b'"))
            db = sqlite3.connect('database.db')
            c = db.cursor()
            c.execute("""CREATE TABLE if not exists attendance(
                        name text,
                        date text,
                        time text)
                    """)

            sql = ("INSERT INTO attendance(name, date, time) VALUES (?, ?, ?);")
            mydata = (str(self.root.get_screen("scanner_screen").ids.qr.text).strip("b'"),
                      date.today().strftime('%B %e %Y'),
                      time.strftime("%I : %M %p"))

            c.execute(sql, mydata)
            db.commit()
            db.close()

    def check_date(self):
        cell = sheet.find(date.today().strftime('%B %e %Y'))
        if cell is not None:
            return cell.col


    def check_name(self, name):
        cell = sheet.find(name)
        if cell is not None:
            sound = SoundLoader.load('beep.mp3')
            if sound:
                sound.play()
            return cell.row


    def class_list(self):
        tableName = self.root.get_screen("home_screen").ids.username.text + "Classes"
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute(f"SELECT * FROM [{tableName.replace(' ', '')}]")
        records = c.fetchall()

        for i in records:
            print(i)

        db.commit()
        db.close()

    def add_class(self):
        tableName = self.root.get_screen("home_screen").ids.username.text + "Classes"
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute(f"""CREATE TABLE if not exists [{tableName.replace(" ", "")}](
                                className text,
                                dateRange text,
                                classTime text,
                                dateCreated text)
                            """)

        sql = (f"INSERT INTO [{tableName.replace(' ', '')}](className, dateRange, classTime, dateCreated) VALUES (?, ?, ?, ?);")
        mydata = (self.root.get_screen("create_class_screen").ids.create_class.text,
                  self.root.get_screen("create_class_screen").ids.calendar_button.text,
                  self.root.get_screen("create_class_screen").ids.clock_button.text,
                  date.today().strftime('%B %e %Y'))

        c.execute(sql, mydata)
        db.commit()
        db.close()
        self.show_class_added_dialog()

    def update_sheet(self, name):
        time_in = time.strftime("%I : %M %p")

        pos = str(sheet.find(date.today().strftime('%B %e %Y')).address[0] + "" + sheet.find(name).address[1])
        sheet.update_cell(self.check_name(name), self.check_date(), time_in)

        if int(time.strftime("%H%M")) <= 1500:
            sheet.format(f"{pos}", {
                "backgroundColor": {
                    "red": 0,
                    "green": 20,
                    "blue": 0
                }
            })

        elif 1530 > int(time.strftime("%H%M")) > 1500 and int(time.strftime("%H%M")):
            sheet.format(f"{pos}", {
                "backgroundColor": {
                    "red": 20,
                    "green": 20,
                    "blue": 0
                }
            })

        else:
            sheet.format(f"{pos}", {
                "backgroundColor": {
                    "red": 20,
                    "green": 00,
                    "blue": 0
                }
            })


    def daily_time_in(self):
        qr_value = str(self.root.get_screen("scanner_screen").ids.qr.text).strip("b'")
        tableName = self.root.get_screen("home_screen").ids.username.text + "Daily"
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute(f"""CREATE TABLE if not exists [{tableName.replace(" ", "")}](
                                        name text,
                                        time text)
                                    """)

        if qr_value != '':
            sql = (f"INSERT INTO [{tableName.replace(' ', '')}](name, time) VALUES (?, ?);")
            mydata = (qr_value, time.strftime("%I : %M %p"))
            c.execute(f"SELECT * FROM [{tableName.replace(' ', '')}]")
            c.execute(sql, mydata)
            db.commit()
            db.close()

            sound = SoundLoader.load('beep.mp3')
            if sound:
                sound.play()

    def show_login_denied_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Incorrect Username Or Password",
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog,
                    ),
                ],
            )
        self.dialog.open()

    def sheet_link(self):
        import webbrowser
        webbrowser.open('https://docs.google.com/spreadsheets/d/1Uv4DABZ_HqvWJmFMZ8Unfh8DZFOXIlmMG_c3UykE_JQ/edit#gid=0')

    def on_save(self, instance, value, date_range):
        cal = date_range[0].strftime('%B%e %Y') + "-" + date_range[-1].strftime('%B %e %Y')
        btn = self.root.get_screen("create_class_screen").ids.calendar_button
        btn.text = f"{cal}"
        btn.size_hint = .40, 0

    def show_time_picker(self, *args):
        time_dialog = MDTimePicker(primary_color="#E4E2E5",
                                   accent_color="#C5C2BD",
                                   text_color="#000000",
                                   text_button_color="#222831",
                                   text_toolbar_color="#222831",
                                   selector_color="#EC994B")
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def show_date_picker(self, *args):
        date_dialog = MDDatePicker(mode="range",
                                   primary_color="#E4E2E5",
                                   accent_color="#C5C2BD",
                                   text_color="#000000",
                                   text_button_color="#222831",
                                   text_toolbar_color="#222831",
                                   selector_color="#EC994B")
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def get_time(self, instance, time_val):
        btn = self.root.get_screen("create_class_screen").ids.clock_button
        btn.text = f"{time_val}"
        btn.size_hint = .40, 0

    def logout(self, obj):
        self.close_dialog(obj)
        self.clear_text()
        self.root.current = "intro_screen"

    def show_logout_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Are you sure you want to logout?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog,
                    ),
                    MDFlatButton(
                        text="LOGOUT",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.logout,
                    ),
                ],
            )
        self.dialog.open()

    def show_class_added_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Class Added!",
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog,
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def clear_text(self):
        self.root.get_screen("login_screen").ids.login_username.text = ''
        self.root.get_screen("login_screen").ids.login_password.text = ''

    def show_attendance_table(self):
        tableName = self.root.get_screen("home_screen").ids.username.text + "Daily"
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute(f"""CREATE TABLE if not exists [{tableName.replace(" ", "")}](
                                                name text,
                                                time text)
                                            """)

        c.execute(f"SELECT * FROM [{tableName.replace(' ', '')}]")
        records = c.fetchall()

        self.data_tables = MDDataTable(
            background_color_header="#EC994B",
            elevation=1,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.9, .5),
            column_data=[
                ("No.", dp(15)),
                ("Name", dp(40)),
                (f"{date.today().strftime('%B %e %Y')}", dp(40))

            ]

        )

        display = []

        num = 1
        for i in records:
            display.append((num, i[0],
                            ("checkbox-blank-circle", [1, 0, 0, 1], i[1])))
            num += 1
        self.data_tables.row_data = display

        self.root.get_screen("class_screen").ids.data_layout.add_widget(self.data_tables)
        db.commit()
        db.close()

    def color_indicator(self, clock_in):
        if int(clock_in.strftime("%H%M")) <= 1500:
            return [39 / 256, 174 / 256, 96 / 256, 1]

        elif 1530 > int(clock_in.strftime("%H%M")) > 1500 and int(clock_in.strftime("%H%M")):
            return [255 / 256, 165 / 256, 0, 1]

        else:
            return [1, 0, 0, 1]


MainApp().run()


