from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.core.audio import SoundLoader
import sqlite3

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import date
import time


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

sm = ScreenManager()
sm.add_widget(IntroScreen(name="intro_screen"))
sm.add_widget(LoginScreen(name="login_screen"))
sm.add_widget(SignupScreen(name="signup_screen"))
sm.add_widget(HomeScreen(name="home_screen"))


sm.add_widget(ScannerScreen(name="scanner_screen"))


class MainApp(MDApp):
    dialog = None

    def build(self):
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
            if i[1] == username:
                if i[2] == password:
                    self.root.current = "home_screen"
                    self.root.get_screen("home_screen").ids.username.text = username
                    break
                else:
                    self.show_login_denied_dialog()
            else:
                self.show_login_denied_dialog()

        db.commit()
        db.close()


    def get_qr_value(self):
        if str(self.root.get_screen("scanner_screen").ids.qr.text).strip("b'") != '':
            self.update_sheet(str(self.root.get_screen("scanner_screen").ids.qr.text).strip("b'"))

    def check_date(self):
        cell = sheet.find(date.today().strftime('%B%e %Y'))
        if cell is not None:
            return cell.col


    def check_name(self, name):
        cell = sheet.find(name)
        if cell is not None:
            sound = SoundLoader.load('beep.mp3')
            if sound:
                sound.play()
            return cell.row



    def update_sheet(self, name):
        sheet.update_cell(self.check_name(name), self.check_date(), time.strftime("%I : %M %p"))



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
    def logout(self, obj):
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

    def close_dialog(self, obj):
        self.dialog.dismiss()


MainApp().run()


