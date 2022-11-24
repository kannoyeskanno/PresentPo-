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


class IntroScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class SignupScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(IntroScreen(name="intro_screen"))
sm.add_widget(LoginScreen(name="login_screen"))
sm.add_widget(SignupScreen(name="signup_screen"))
sm.add_widget(HomeScreen(name="home_screen"))


class MainApp(MDApp):
    dialog = None

    def build(self):
        self.icon = "presentpo_icon.png"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('test1.kv')

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
