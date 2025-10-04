from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from PIL import Image as PILImage
import os


class ImageConverterApp(App):
    def build(self):
        self.title = "Image Resize & Converter (JPG to PNG)"
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='Image Resize & Converter (JPG to PNG)',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True
        )
        
        # Area untuk menampilkan gambar
        self.image_display = Image(size_hint=(1, 0.5))
        
        # Input untuk lebar gambar
        width_layout = BoxLayout(size_hint=(1, 0.08), spacing=10)
        width_layout.add_widget(Label(text='Width (px):', size_hint=(0.3, 1)))
        self.width_input = TextInput(
            text='800',
            multiline=False,
            input_filter='int',
            size_hint=(0.7, 1)
        )
        width_layout.add_widget(self.width_input)
        
        # Input untuk tinggi gambar
        height_layout = BoxLayout(size_hint=(1, 0.08), spacing=10)
        height_layout.add_widget(Label(text='Height (px):', size_hint=(0.3, 1)))
        self.height_input = TextInput(
            text='600',
            multiline=False,
            input_filter='int',
            size_hint=(0.7, 1)
        )
        height_layout.add_widget(self.height_input)
        
        # Tombol-tombol
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        self.select_btn = Button(
            text='Select Image (JPG)',
            background_color=(0.2, 0.6, 1, 1)
        )
        self.select_btn.bind(on_press=self.select_image)
        
        self.convert_btn = Button(
            text='Resize & Convert to PNG',
            background_color=(0.2, 0.8, 0.2, 1),
            disabled=True
        )
        self.convert_btn.bind(on_press=self.convert_image)
        
        button_layout.add_widget(self.select_btn)
        button_layout.add_widget(self.convert_btn)
        
        # Status label
        self.status_label = Label(
            text='Please select an image...',
            size_hint=(1, 0.08),
            color=(0.5, 0.5, 0.5, 1)
        )
        
        # Menambahkan semua widget ke layout utama
        main_layout.add_widget(header)
        main_layout.add_widget(self.image_display)
        main_layout.add_widget(width_layout)
        main_layout.add_widget(height_layout)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(self.status_label)
        
        self.selected_image_path = None
        
        return main_layout
    
    def select_image(self, instance):
        # Membuat file chooser popup
        content = BoxLayout(orientation='vertical')
        
        file_chooser = FileChooserIconView(
            filters=['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']
        )
        
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        select_btn = Button(text='Select')
        cancel_btn = Button(text='Cancel')
        
        button_layout.add_widget(select_btn)
        button_layout.add_widget(cancel_btn)
        
        content.add_widget(file_chooser)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='Select JPG Image',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def on_select(btn):
            if file_chooser.selection:
                self.selected_image_path = file_chooser.selection[0]
                self.image_display.source = self.selected_image_path
                self.convert_btn.disabled = False
                self.status_label.text = f'Selected: {os.path.basename(self.selected_image_path)}'
                self.status_label.color = (0, 0.8, 0, 1)
            popup.dismiss()
        
        def on_cancel(btn):
            popup.dismiss()
        
        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=on_cancel)
        
        popup.open()
    
    def convert_image(self, instance):
        if not self.selected_image_path:
            self.status_label.text = 'No image selected!'
            self.status_label.color = (1, 0, 0, 1)
            return
        
        try:
            # Mendapatkan ukuran dari input
            width = int(self.width_input.text) if self.width_input.text else 800
            height = int(self.height_input.text) if self.height_input.text else 600
            
            # Membuka gambar dengan PIL
            img = PILImage.open(self.selected_image_path)
            
            # Resize gambar
            img_resized = img.resize((width, height), PILImage.Resampling.LANCZOS)
            
            # Membuat nama file output
            base_name = os.path.splitext(os.path.basename(self.selected_image_path))[0]
            output_path = os.path.join(
                os.path.dirname(self.selected_image_path),
                f"{base_name}_resized.png"
            )
            
            # Menyimpan sebagai PNG
            img_resized.save(output_path, 'PNG')
            
            # Update display dengan gambar hasil
            self.image_display.source = output_path
            self.image_display.reload()
            
            # Update status
            self.status_label.text = f'✓ Converted! Saved as: {os.path.basename(output_path)}'
            self.status_label.color = (0, 1, 0, 1)
            
            # Tampilkan popup sukses
            popup = Popup(
                title='Success!',
                content=Label(text=f'Image saved as:\n{output_path}'),
                size_hint=(0.8, 0.3)
            )
            popup.open()
            
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'
            self.status_label.color = (1, 0, 0, 1)


if __name__ == '__main__':
    ImageConverterApp().run()