from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
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
    def build(self):
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('test1.kv')

    def logger(self):
        self.root.ids.welcome_label.text = f'Sup {self.root.ids.user.text}!'

    def clear(self):
        self.root.ids.welcome_label.text = "WELCOME"
        self.root.ids.user.text = ""
        self.root.ids.password.text = ""


MainApp().run()
