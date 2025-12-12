from kivy.app import App
from kivy.lang import Builder

KV = """
BoxLayout:
    orientation: "vertical"
    padding: 20
    spacing: 15

    Label:
        text: "🎵 OSU Rate Changer Mobile"
        font_size: "24sp"
        bold: True
        size_hint_y: None
        height: 50

    Label:
        text: "Introduce tasas (ej: 1.2,1.3) o BPM:"
        size_hint_y: None
        height: 30

    TextInput:
        id: input_valores
        hint_text: "Ej: 1.2, 1.3 o 230"
        multiline: False
        size_hint_y: None
        height: 40

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: 40

        Label:
            text: "Activar cambio de tono"
        Switch:
            id: switch_pitch
            active: True

    BoxLayout:
        size_hint_y: None
        height: 50
        spacing: 10

        Button:
            text: "Ratear con Rates"
            on_press: app.ratear_con_rates()
        Button:
            text: "Ratear con BPM"
            on_press: app.ratear_con_bpm()

    Label:
        id: log
        text: "Esperando acción..."
        size_hint_y: None
        height: 40
        color: 0.8, 0.8, 0.8, 1
"""

class RateChangerApp(App):
    def build(self):
        return Builder.load_string(KV)

    def ratear_con_rates(self):
        valores = self.root.ids.input_valores.text
        activar = self.root.ids.switch_pitch.active
        # Aquí llamaríamos a procesar_mapas("rates", tasas=[...], activar_cambio_de_tono=activar)
        self.root.ids.log.text = f"Procesando con rates: {valores}, Pitch: {activar}"

    def ratear_con_bpm(self):
        valores = self.root.ids.input_valores.text
        activar = self.root.ids.switch_pitch.active
        # Aquí llamaríamos a procesar_mapas("bpm", bpm=float(valores), activar_cambio_de_tono=activar)
        self.root.ids.log.text = f"Procesando con BPM: {valores}, Pitch: {activar}"

if __name__ == "__main__":
    RateChangerApp().run()
