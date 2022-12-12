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
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp


class IntroScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class SignupScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class ClassScreen(Screen):
    pass


class CreateClassScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(IntroScreen(name="intro_screen"))
sm.add_widget(LoginScreen(name="login_screen"))
sm.add_widget(SignupScreen(name="signup_screen"))
sm.add_widget(HomeScreen(name="home_screen"))
sm.add_widget(ClassScreen(name="class_screen"))
sm.add_widget(CreateClassScreen(name="create_class_screen"))


class MainApp(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None

    def build(self):
        return Builder.load_file('main.kv')

    def show_attendance_table(self):
        self.data_tables = MDDataTable(
            background_color_header="#EC994B",
            elevation=1,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.9, .5),
            column_data=[
                ("No.", dp(15)),
                ("Name", dp(40)),
                ("Date", dp(15)),
                ("Date", dp(15))
            ],
            row_data=[
                ("1", "Bundalian, Julius Jervin V.",
                 ("checkbox-blank-circle", [39 / 256, 174 / 256, 96 / 256, 1], ""),
                 ("checkbox-blank-circle", [255 / 256, 165 / 256, 0, 1], "")),
                ("2", "Jomar", ("checkbox-blank-circle", [255 / 256, 165 / 256, 0, 1], ""),
                 ("checkbox-blank-circle", [1, 0, 0, 1], "")),
                ("3", "Kevs", ("checkbox-blank-circle", [1, 0, 0, 1], ""),
                 ("checkbox-blank-circle", [255 / 256, 165 / 256, 0, 1], "")),
            ]
        )

        self.root.get_screen("class_screen").ids.data_layout.add_widget(self.data_tables)

    def show_logout_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Confirm Logout",
                text="Are you sure you want to logout?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color="#79747E",
                        on_release=self.close_dialog,
                    ),
                    MDFlatButton(
                        text="LOGOUT",
                        theme_text_color="Custom",
                        text_color="#EC994B",
                        on_release=self.logout,
                    ),
                ],
            )
        self.dialog.open()

    def show_time_picker(self, *args):
        time_dialog = MDTimePicker(primary_color="#E4E2E5",
                                   accent_color="#C5C2BD",
                                   text_color="#000000",
                                   text_button_color="#222831",
                                   text_toolbar_color="#222831",
                                   selector_color="#EC994B")
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time_val):
        btn = self.root.get_screen("create_class_screen").ids.clock_button
        btn.text = f"{time_val}"
        btn.size_hint = .40, 0

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def logout(self, obj):
        self.root.current = "intro_screen"
        self.dialog.dismiss()


MainApp().run()
