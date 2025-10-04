import matplotlib.pyplot as plt
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.image import Image as CoreImage
from io import BytesIO

class MatplotlibKivyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.button = Button(text='Tampilkan Grafik', size_hint=(1, 0.2))
        self.button.bind(on_press=self.plot_graph)

        self.image = Image()
        self.image.allow_stretch = True  # agar gambar menyesuaikan ukuran

        self.layout.add_widget(self.button)
        self.layout.add_widget(self.image)

        return self.layout

    def plot_graph(self, instance):
        # Membuat data contoh
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # Membuat figure matplotlib
        plt.figure(figsize=(5, 3))
        plt.plot(x, y, label='sin(x)')  # label huruf kecil
        plt.title('Grafik sin(x)')
        plt.legend()
        plt.tight_layout()

        # Simpan figure ke buffer bytes
        buf = BytesIO()
        plt.savefig(buf, format='png')  # gunakan buf, bukan buff
        buf.seek(0)
        plt.close()

        # Load gambar ke core image kivy
        core_image = CoreImage(buf, ext='png')

        # Set texture ke widget Image
        self.image.texture = core_image.texture

if __name__ == '__main__':
    MatplotlibKivyApp().run()