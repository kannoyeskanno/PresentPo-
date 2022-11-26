from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy_garden.zbarcam import ZBarCam
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory
import sqlite3
import os.path



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


        return Builder.load_file('PresentPoMobileApp.kv')

    def submit(self):

        db = sqlite3.connect('database.db')
        c = db.cursor()
        sql = ("INSERT INTO users(email, username, password) VALUES (?, ?, ?);")
        mydata = (self.root.get_screen("signup_screen").ids.signup_email.text, self.root.get_screen("signup_screen").ids.signup_username.text, self.root.get_screen("signup_screen").ids.signup_password.text)
        c.execute(sql, mydata)

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
                    break
                else:
                    self.show_login_denied_dialog()
            else:
                self.show_login_denied_dialog()



        db.commit()
        db.close()

    def scanner(self):
        pass

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
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()


MainApp().run()

# from kivy.lang import Builder
# from kivymd.app import MDApp
# from kivy.uix.screenmanager import Screen, ScreenManager
# from kivy.core.window import Window
# from kivymd.uix.button import MDFlatButton
# from kivymd.uix.dialog import MDDialog
# from kivy.uix.scrollview import ScrollView
# from kivy.uix.boxlayout import BoxLayout
# from kivy.factory import Factory
# # import mysql.connector
# import sqlite3
#
# #:import ZBarCam kivy_garden.zbarcam.ZBarCam
# # BoxLayout:
# # orientation: 'vertical'
# # ZBarCam:
# # id: zbarcam
# # size: 420, 400
# # # optional, override the camera index (default 0)
# # camera_index: 0  # or try a different value
# # # optional, by default checks all types
# # code_types: 'QRCODE', 'EAN13'
# # Label:
# # id: input
# # size_hint: None, None
# # size: self.texture_size[0], 50
# # text: ', '.join([str(symbol.data) for symbol in zbarcam.symbols])
#
# Window.size = (420,600)
#
# class IntroScreen(Screen):
#     pass
#
#
# class LoginScreen(Screen):
#     pass
#
#
# class SignupScreen(Screen):
#     pass
#
#
# class HomeScreen(Screen):
#     pass
#
#
# sm = ScreenManager()
# sm.add_widget(IntroScreen(name="intro_screen"))
# sm.add_widget(LoginScreen(name="login_screen"))
# sm.add_widget(SignupScreen(name="signup_screen"))
# sm.add_widget(HomeScreen(name="home_screen"))
#
#
# class MainApp(MDApp):
#     dialog = None
#
    # def build(self):
    #     self.theme_cls.theme_style = "Light"
    #     db = sqlite3.connect('database.db')
    #     c = db.cursor()
    #     c.execute("""CREATE TABLE if not exists users(
    #         email text,
    #         username text,
    #         password text)
    #     """)
    #     db.commit()
    #     db.close()


       # return Builder.load_file('PresentPoMobileApp.kv')
    #
    # def submit(self):
    #     db = sqlite3.connect('database.db')
    #     c = db.cursor()
    #     sql = ("INSERT INTO database(email, username, password) VALUES (?, ?, ?);")
    #     mydata = (self.root.ids.signup_email.text, self.root.ids.signup_username.text, self.root.ids.signup_password.text)
    #     c.execute(sql, mydata)
    #
    #     db.commit()
    #     db.close()

    # def show_records(self):
    #     db = sqlite3.connect('database.db')
    #     c = db.cursor()
    #
    #     c.execute("SELECT * FROM email")
    #     records = c.fetchall()
    #     word = ''
    #
    #     for i in records:
    #         word = f'{word}\n{i}'
    #         print(word)
    #
    #     db.commit()
    #     db.close()

#
#     def show_logout_dialog(self):
#             if not self.dialog:
#                 self.dialog = MDDialog(
#                     text="Are you sure you want to logout?",
#                     buttons=[
#                         MDFlatButton(
#                             text="CANCEL",
#                             theme_text_color="Custom",
#                             text_color=self.theme_cls.primary_color,
#                             on_release=self.close_dialog,
#                         ),
#                         MDFlatButton(
#                             text="LOGOUT",
#                             theme_text_color="Custom",
#                             text_color=self.theme_cls.primary_color,
#
#                         ),
#                     ],
#                 )
#
#             self.dialog.open()
#
#         def close_dialog(self, obj):
#             self.dialog.dismiss()
#
#
# MainApp().run()