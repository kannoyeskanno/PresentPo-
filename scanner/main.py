
from kivy.app import App
from kivy.lang import Builder

DEMO_APP_KV_LANG = """
#:import ZBarCam kivy_garden.zbarcam.ZBarCam
BoxLayout:
    name: "scanner"
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
        # optional, override the camera index (default 0)
        camera_index: 0     # or try a different value
        # optional, by default checks all types
        code_types: 'QRCODE', 'EAN13'
    Label:
        id: qr
        size_hint: None, None
        size: self.texture_size[0], 50
        text: ', '.join([str(symbol.data) for symbol in zbarcam.symbols])
    
    Button:
        text: "Scan"
        on_press: app.println()
"""


class DemoApp(App):

    def build(self):
        return Builder.load_string(DEMO_APP_KV_LANG)

    def println(self):
        print(str(self.root.ids.qr.text).strip("b'"))


if __name__ == '__main__':
    DemoApp().run()
