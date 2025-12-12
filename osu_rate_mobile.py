from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from threading import Thread
import os
import subprocess
from pydub import AudioSegment  # puede quedarse aunque no lo usemos aquí

Window.size = (520, 720)

KV = """
BoxLayout:
    orientation: 'vertical'
    padding: 25
    spacing: 18
    canvas.before:
        Color:
            rgba: 0.07, 0.07, 0.09, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "🎵 [b]OSU Rate Changer[/b]"
        markup: True
        font_size: "26sp"
        color: 1, 1, 1, 1
        size_hint_y: None
        height: 60

    Label:
        text: "📁 Selecciona carpeta base:"
        color: 0.9, 0.9, 0.9, 1
        size_hint_y: None
        height: 25

    Button:
        text: "Seleccionar carpeta"
        background_color: 0.2, 0.4, 0.9, 1
        color: 1, 1, 1, 1
        size_hint_y: None
        height: 45
        on_release: app.seleccionar_carpeta()

    Label:
        id: label_carpeta
        text: "[i]Ninguna carpeta seleccionada[/i]"
        markup: True
        color: 0.8, 0.8, 0.8, 1
        text_size: self.width, None
        size_hint_y: None
        height: 80
        halign: "center"
        valign: "middle"

    Label:
        text: "🎚️ Ingresa rates o BPM (separados por coma):"
        color: 0.9, 0.9, 0.9, 1
        size_hint_y: None
        height: 25

    TextInput:
        id: input_valores
        hint_text: "Ejemplo: 1.1, 1.2 o 230, 240"
        background_color: 0.15, 0.15, 0.18, 1
        foreground_color: 1, 1, 1, 1
        cursor_color: 1, 1, 1, 1
        multiline: False
        size_hint_y: None
        height: 45
        font_size: 16

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: 35
        spacing: 10
        CheckBox:
            id: switch_pitch
            active: True
            size_hint_x: None
            width: 40
            on_active: app.cambiar_estado_tono(self.active)
        Label:
            id: label_tono
            text: "🔊 Tono activado"
            color: 0.9, 0.9, 0.9, 1
            halign: "left"
            valign: "middle"

    BoxLayout:
        size_hint_y: None
        height: 50
        spacing: 12

        Button:
            text: "Ratear con RATE"
            background_color: 0.25, 0.5, 1, 1
            color: 1, 1, 1, 1
            on_release: app.ratear_con_rate()

        Button:
            text: "Ratear con BPM"
            background_color: 0.25, 0.5, 1, 1
            color: 1, 1, 1, 1
            on_release: app.ratear_con_bpm()

    Label:
        id: log
        text: "Esperando acción..."
        color: 0.8, 0.8, 0.8, 1
        text_size: self.width - 20, None
        halign: "center"
        valign: "top"
        size_hint_y: None
        height: 120
"""

class OsuRateApp(App):
    def build(self):
        self.ruta_base = ""
        return Builder.load_string(KV)

    def cambiar_estado_tono(self, activo):
        # Texto claro y coherente
        if activo:
            self.root.ids.label_tono.text = "🔊 Tono activado"
        else:
            self.root.ids.label_tono.text = "🎵 Tono desactivado"

    def seleccionar_carpeta(self):
        from tkinter import Tk, filedialog
        root = Tk()
        root.withdraw()
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.ruta_base = carpeta
            self.root.ids.label_carpeta.text = f"[b]Carpeta seleccionada:[/b]\\n{carpeta}"
            self.log("✅ Carpeta cargada correctamente.")
        else:
            self.log("❌ No se seleccionó ninguna carpeta.")

    def log(self, texto):
        self.root.ids.log.text = texto

    def ratear_con_rate(self):
        if not self.ruta_base:
            self.root.ids.log.text = "Primero selecciona la carpeta base."
            return
        valores = self.root.ids.input_valores.text
        mantener_tono = self.root.ids.switch_pitch.active
        try:
            rates = [float(v.strip()) for v in valores.split(",")]
        except:
            self.root.ids.log.text = "Error: ingresa números separados por coma."
            return
        Thread(target=self.procesar_rates, args=(rates, mantener_tono)).start()

    def procesar_rates(self, rates, mantener_tono):
        for rate in rates:
            self.ratear_archivos_osu(rate, self.ruta_base, mantener_tono, modo_bpm=False)
        self.log("✅ Rateo completado.")

    def ratear_con_bpm(self):
        if not self.ruta_base:
            self.root.ids.log.text = "Primero selecciona la carpeta base."
            return
        valores = self.root.ids.input_valores.text
        mantener_tono = self.root.ids.switch_pitch.active
        try:
            bpms = [float(v.strip()) for v in valores.split(",")]
        except:
            self.root.ids.log.text = "Error: ingresa BPM separados por coma."
            return
        Thread(target=self.procesar_bpms, args=(bpms, mantener_tono)).start()

    def procesar_bpms(self, bpms, mantener_tono):
        for bpm in bpms:
            self.ratear_archivos_osu(bpm, self.ruta_base, mantener_tono, modo_bpm=True)
        self.log("✅ Rateo con BPMs completado.")

    # --- helper para atempo compuesto (FFmpeg necesita atempo entre 0.5 y 2.0) ---
    def _atempo_filter(self, factor: float) -> str:
        """
        Devuelve un string de filtro atempo compuesto para aproximarse al factor dado.
        """
        parts = []
        # Evitar factor == 0
        if factor <= 0:
            factor = 1.0
        # Romper factor en productos entre 0.5 y 2.0
        f = factor
        while f > 2.0:
            parts.append("atempo=2.0")
            f /= 2.0
        while f < 0.5:
            parts.append("atempo=0.5")
            f /= 0.5
        # Añadir el resto (puede ser 1.0)
        parts.append(f"atempo={f:.6f}")
        return ",".join(parts)

    def ratear_archivos_osu(self, valor, carpeta, mantener_tono, modo_bpm=False):
        salida = os.path.join(carpeta, f"MapasRateados_{valor}{'BPM' if modo_bpm else 'x'}")
        os.makedirs(salida, exist_ok=True)
        archivos = [f for f in os.listdir(carpeta) if f.endswith(".osu")]
        if not archivos:
            self.log("⚠️ No se encontraron archivos .osu.")
            return
        for archivo in archivos:
            ruta_osu = os.path.join(carpeta, archivo)
            nombre_base = os.path.splitext(archivo)[0]
            ruta_dest = os.path.join(salida, archivo)

            with open(ruta_osu, "r", encoding="utf-8", errors="ignore") as f:
                contenido = f.readlines()

            nuevo_contenido = []
            for linea in contenido:
                if "SliderMultiplier" in linea:
                    nuevo_contenido.append(linea)
                elif "AudioFilename" in linea:
                    nuevo_contenido.append(linea)
                    nombre_audio = linea.split(":")[1].strip()
                    ruta_audio = os.path.join(carpeta, nombre_audio)
                    if os.path.exists(ruta_audio):
                        # Determinar factor: para BPM usamos valor/ (bpm_original) si quieres,
                        # aquí mantenemos la lógica previa: modo_bpm usa valor/100.0 (como antes)
                        if modo_bpm:
                            factor = valor / 100.0
                        else:
                            factor = valor
                        # preparar nombre de salida
                        nombre_salida = f"{nombre_base}_{valor}{'BPM' if modo_bpm else 'x'}.mp3"
                        ruta_salida_audio = os.path.join(salida, nombre_salida)

                        # Si mantener_tono == True => mantener tono original (usar atempo)
                        # Si mantener_tono == False => cambiar tono (usar asetrate)
                        try:
                            if mantener_tono:
                                # atempo puede requerir cadena compuesta
                                filtro = self._atempo_filter(factor)
                                cmd = [
                                    "ffmpeg", "-y", "-i", ruta_audio,
                                    "-filter:a", filtro,
                                    "-vn", ruta_salida_audio
                                ]
                            else:
                                # asetrate cambia tono y velocidad
                                cmd = [
                                    "ffmpeg", "-y", "-i", ruta_audio,
                                    "-filter:a", f"asetrate=44100*{factor},aresample=44100",
                                    "-vn", ruta_salida_audio
                                ]
                            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        except Exception as e:
                            self.log(f"❌ Error procesando audio: {e}")
                else:
                    nuevo_contenido.append(linea)

            # escribir el .osu modificado (si deseas actualizar audio filename, ya lo deja igual que antes)
            with open(ruta_dest, "w", encoding="utf-8") as f:
                f.writelines(nuevo_contenido)
        self.log(f"✅ Procesado: {valor}{' BPM' if modo_bpm else 'x'}")

if __name__ == "__main__":
    OsuRateApp().run()



