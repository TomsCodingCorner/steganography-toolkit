"""Original Kivy interface for TABS and PNG steganography."""
from functools import wraps

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from plyer import filechooser

from STEGANOGRAPHY import BASE_DIR, OUTPUT_DIR, Obfuscate, Deobfuscate
from TABS import EN_TABS, DE_TABS

resource_add_path(str(BASE_DIR))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def report_errors(method):
    @wraps(method)
    def run(self, *args):
        try:
            return method(self, *args)
        except (ValueError, OSError, AttributeError, IndexError) as error:
            Popup(title="Input error", content=Label(text=str(error)),
                  size_hint=(0.85, 0.35)).open()
    return run

kivy.require('1.9.0')

Builder.load_string("""
<ScreenOne>:
    canvas.before:
        Color:
            rgba: 0.204, 0.204, 0.212, 0.5
        Rectangle:
            size: self.size
            pos: self.pos

    RelativeLayout:
        orientation: 'vertical'
        Button:
            padding: 10
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.0, 'y': 0.875}
            text: "Encrypt"
            background_color: 0.292, 0.292, 0.295, 1
            
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 0.3 
                Line:
                    width: 2
                    rounded_rectangle: self.x, self.y, self.width, self.height, 10
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_one'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.15, 'y': 0.875}
            text: "Decrypt"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_two'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.3, 'y': 0.875} 
            text: "String to binary"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_three'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.45, 'y': 0.875}
            text: "Binary to string"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_four'
                
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.25, 0.18
            pos_hint: {'x': 0.75, 'y': 0.827}
            background_normal: "Assisting_Files//image.png"
            background_down: "Assisting_Files//image.png" 
            on_press:
                app.stop()
                
        Button:
            size_hint: 0.868, 0.0000001
            pos_hint: {'x': 0.0, 'y': 0.8569}
            background_color: 233, 234, 232, 1
            
        Button:
            size_hint: 1.1, 0.005
            pos_hint: {'x': 0.0, 'y': 0.8350}
            background_color: 0.292, 0.292, 0.295, 1
            
        TextInput:
            id: textinput
            multiline: True
            size_hint: 0.40, 0.25
            pos_hint: {'x': 0.3, 'y': 0.425}
            background_color: 1, 1, 1, 0.1

        Button:
            size_hint: 0.15, 0.09
            pos_hint: {'x': 0.75, 'y': 0.5}
            text: "Hide"
            background_color: 0.051, 0.278, 0.631, 1
            on_press: root.extract_widget_info()
            
        Button:
            size_hint: 0.15, 0.09
            pos_hint: {'x': 0.1, 'y': 0.5}
            text: "Select Image"
            background_color: 0.051, 0.278, 0.631, 1
            on_press: root.open_filechooser()
            
        TextInput: 
            id: passinput
            multiline: False
            size_hint: 0.25, 0.05
            pos_hint: {'x': 0.375, 'y': 0.3}
            background_color: 1, 1, 1, 0.1
            
        Button:
            size_hint: 0.25, 0.05
            pos_hint: {'x': 0.375, 'y': 0.35}
            text: "Password"
            color: 1, 1, 1, 1
            background_color: 0.051, 0.278, 0.631, 0
            
        Button:
            size_hint: 0.25, 0.05
            pos_hint: {'x': 0.375, 'y': 0.690}
            text: "Enter message"
            color: 1, 1, 1, 1
            background_color: 0.051, 0.278, 0.631, 0
          
           
<ScreenTwo>:
    canvas.before:
        Color:
            rgba: 0.204, 0.204, 0.212, 0.5
        Rectangle:
            size: self.size
            pos: self.pos

    RelativeLayout:
        orientation: 'vertical'
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.0, 'y': 0.875}
            text: "Encrypt"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_one'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.15, 'y': 0.875}
            text: "Decrypt"
            background_color: 0.292, 0.292, 0.295, 1
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 0.3 
                Line:
                    width: 2
                    rounded_rectangle: self.x, self.y, self.width, self.height, 10
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_two'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.3, 'y': 0.875} 
            text: "String to binary"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_three'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.45, 'y': 0.875}
            text: "Binary to string"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_four'
                
        Button:
            size_hint: 0.15, 0.09
            pos_hint: {'x': 0.75, 'y': 0.5}
            text: "Uncover"
            background_color: 0.051, 0.278, 0.631, 1
            on_press: root.extract_widget_info()
            
        Button:
            size_hint: 0.15, 0.09
            pos_hint: {'x': 0.1, 'y': 0.5}
            text: "Select Image"
            background_color: 0.051, 0.278, 0.631, 1
            on_press: root.open_filechooser()
            
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.25, 0.18
            pos_hint: {'x': 0.75, 'y': 0.827}
            background_normal: "Assisting_Files//image.png"
            background_down: "Assisting_Files//image.png" 
            on_press:
                app.stop()
                
        Button:
            size_hint: 0.868, 0.0000001
            pos_hint: {'x': 0.0, 'y': 0.8569}
            background_color: 233, 234, 232, 1
            
        Button:
            size_hint: 1.1, 0.005
            pos_hint: {'x': 0.0, 'y': 0.8350}
            background_color: 0.292, 0.292, 0.295, 1
            
        TextInput: 
            id: passinput
            multiline: False
            size_hint: 0.25, 0.05
            pos_hint: {'x': 0.375, 'y': 0.5}
            background_color: 1, 1, 1, 0.1
            
        Button:
            size_hint: 0.25, 0.05
            pos_hint: {'x': 0.375, 'y': 0.55}
            text: "Password"
            color: 1, 1, 1, 1
            background_color: 0.051, 0.278, 0.631, 0

        
<ScreenThree>:
    canvas.before:
        Color:
            rgba: 0.204, 0.204, 0.212, 0.5
        Rectangle:
            size: self.size
            pos: self.pos
            
    RelativeLayout:
        orientation: 'vertical'
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.0, 'y': 0.875}
            text: "Encrypt"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_one'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.15, 'y': 0.875}
            text: "Decrypt"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_two'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.3, 'y': 0.875} 
            text: "String to binary"
            background_color: 0.292, 0.292, 0.295, 1
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 0.3 
                Line:
                    width: 2
                    rounded_rectangle: self.x, self.y, self.width, self.height, 10
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_three'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.45, 'y': 0.875}
            text: "Binary to string"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_four'
                
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.25, 0.18
            pos_hint: {'x': 0.75, 'y': 0.827}
            background_normal: "Assisting_Files//image.png"
            background_down: "Assisting_Files//image.png" 
            on_press:
                app.stop()
                
        Button:
            size_hint: 0.868, 0.0000001
            pos_hint: {'x': 0.0, 'y': 0.8569}
            background_color: 233, 234, 232, 1
            
        Button:
            size_hint: 1.1, 0.005
            pos_hint: {'x': 0.0, 'y': 0.8350}
            background_color: 0.292, 0.292, 0.295, 1
            
        Button:
            size_hint: 0.15, 0.09
            pos_hint: {'x': 0.75, 'y': 0.5}
            text: "Binary"
            background_color: 0.051, 0.278, 0.631, 1
            on_press: root.extract_widget_info()
            
            
        Button:
            size_hint: 0.15, 0.09
            pos_hint: {'x': 0.1, 'y': 0.5}
            text: "Select File"
            background_color: 0.051, 0.278, 0.631, 1
            on_press: root.open_filechooser()
            
            
        TextInput:
            id: textinput1
            multiline: True
            size_hint: 0.40, 0.6
            pos_hint: {'x': 0.3, 'y': 0.125}
            background_color: 1, 1, 1, 0.1
            
        Switch: 
            id: switch2
            size_hint: 0.1, 0.1
            pos_hint: {'x': 0.17, 'y': 0.25}
            active: True            
            
        Button: 
            id: bestmodelbutton
            size_hint: 0.1, 0.1
            pos_hint: {'x': 0.03, 'y': 0.25}
            text: "Bestmodel"
            color: 1, 1, 1, 0
            background_color: 0.051, 0.278, 0.631, 0
            
            
        Button: 
            id: wordlistbutton
            size_hint: 0.1, 0.1
            pos_hint: {'x': 0.03, 'y': 0.25}
            text: "Include Wordlists"
            color: 1, 1, 1, 1
            background_color: 0.051, 0.278, 0.631, 0


<ScreenFour>:
    canvas.before:
        Color:
            rgba: 0.204, 0.204, 0.212, 0.5
        Rectangle:
            size: self.size
            pos: self.pos
    RelativeLayout:
        orientation: 'vertical'
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.0, 'y': 0.875}
            text: "Encrypt"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_one'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.15, 'y': 0.875}
            text: "Decrypt"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_two'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.3, 'y': 0.875} 
            text: "String to binary"
            background_color: 0.25, 0.25, 0.25, 1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_three'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.15, 0.125
            pos_hint: {'x': 0.45, 'y': 0.875}
            text: "Binary to string"
            background_color: 0.292, 0.292, 0.295, 1
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 0.3 
                Line:
                    width: 2
                    rounded_rectangle: self.x, self.y, self.width, self.height, 10
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_four'
                
        Button:
            padding: 10 
            spacing: 10 
            size_hint: 0.25, 0.18
            pos_hint: {'x': 0.75, 'y': 0.827}
            background_normal: "Assisting_Files//image.png"
            background_down: "Assisting_Files//image.png" 
            on_press:
                app.stop()
                
        Button:
            size_hint: 0.868, 0.0000001
            pos_hint: {'x': 0.0, 'y': 0.8569}
            background_color: 233, 234, 232, 1
            
        Button:
            size_hint: 1.1, 0.005
            pos_hint: {'x': 0.0, 'y': 0.8350}
            background_color: 0.292, 0.292, 0.295, 1
            
        Button:
            size_hint: 0.15, 0.09
            pos_hint: {'x': 0.75, 'y': 0.5}
            text: "Get str"
            background_color: 0.051, 0.278, 0.631, 1
            on_press: root.extract_widget_info()
            
        Button:
            size_hint: 0.15, 0.09
            pos_hint: {'x': 0.1, 'y': 0.5}
            text: "Select TextFile"
            background_color: 0.051, 0.278, 0.631, 1
            on_press: root.open_filechooser()
            
        TextInput:
            id: textinput1
            multiline: True
            size_hint: 0.40, 0.25
            pos_hint: {'x': 0.3, 'y': 0.425}
            background_color: 1, 1, 1, 0.1


""")


class ScreenOne(Screen):
    def open_filechooser(self):
        path = filechooser.open_file(title="Pick a PNG file..", path=str(BASE_DIR / 'Input_Directory'), filters=['*.png'], multiple=False)
        if path:
            self.filepath = path
    @report_errors
    def extract_widget_info(self):
        if not getattr(self, "filepath", []):
            raise ValueError("Choose a PNG image first.")
        print("Started steganography")
        widget_info = {}

        widget_info['textinput'] = str(self.ids.textinput.text)
        widget_info['passinput'] = str(self.ids.passinput.text)

        temp = Obfuscate(image_path=self.filepath[0], message=widget_info['textinput'], password=widget_info['passinput'])

        print(f"Saved image: {temp.output_path}")


class ScreenTwo(Screen):
    def open_filechooser(self):
        path = filechooser.open_file(title="Pick a PNG file..", path=str(BASE_DIR / 'Input_Directory'), filters=['*.png'], multiple=False)
        if path:
            self.filepath = path

    @report_errors
    def extract_widget_info(self):
        if not getattr(self, "filepath", []):
            raise ValueError("Choose a PNG image first.")
        print("Start desteganography")
        widget_info = {}
        widget_info['passinput'] = str(self.ids.passinput.text)
        widget_info['filepath'] = self.filepath[0]
        temp = Deobfuscate(image_path=widget_info['filepath'], password=widget_info['passinput'])
        temp.givebackfile()
        print("Ended desteganography")



class ScreenThree(Screen):

    @report_errors
    def open_filechooser(self):
        path = filechooser.open_file(title="Pick a text file..", path=str(BASE_DIR / 'Input_Directory'), filters=['*.txt', '*.tabs'], multiple=False)
        if path:
            self.filepath = path
            self.ids.textinput1.text = (BASE_DIR / path[0]).read_text(encoding="utf-8").rstrip("\n")

    def givebackfile(self, bin=None):
        with open(OUTPUT_DIR / "tabs_binair_output.txt", "w", encoding="utf-8") as file:
            file.write(bin)


    @report_errors
    def extract_widget_info(self):
        widget_info = {}
        widget_info['textinput1'] = str(self.ids.textinput1.text)
        widget_info['wordlistbutton'] = self.ids.switch2.active

        self.givebackfile(bin=EN_TABS(message=widget_info['textinput1'], optimized=widget_info['wordlistbutton']))
        print("Check 'Output_Directory\\tabs_binair_output.txt'")


class ScreenFour(Screen):
    def open_filechooser(self):
        path = filechooser.open_file(title="Pick a .txt file..", path=str(BASE_DIR / 'Input_Directory'), filters=['*.txt', '*.tabs'], multiple=False)
        if path:
            self.filepath = path

    def givebackfile(self):
        with open(OUTPUT_DIR / "tabs_string_output.txt", "w", encoding="utf-8") as file:
            file.write(self.mssg)

    def getfiledata(self):
        if self.filepath:
            with open(self.filepath[0], "r", encoding="utf-8") as file:
                self.binmessage = file.read()

    @report_errors
    def extract_widget_info(self):
        print("Started getting string")
        widget_info = {}
        if self.ids.textinput1.text:
            widget_info['textinput1'] = str(self.ids.textinput1.text)
        else:
            if not getattr(self, "filepath", []):
                raise ValueError("Enter TABS bits or choose a text file first.")
            self.getfiledata()
            widget_info['textinput1'] = self.binmessage

        self.mssg = DE_TABS(binary=widget_info['textinput1'])
        print(f"Done with getting string: '{self.mssg}'\nAlso check out: 'Output_Directory\\tabs_string_output.txt'")
        self.givebackfile()

screen_manager = ScreenManager(transition = FadeTransition())

screen_manager.add_widget(ScreenOne(name="screen_one"))
screen_manager.add_widget(ScreenTwo(name="screen_two"))
screen_manager.add_widget(ScreenThree(name="screen_three"))
screen_manager.add_widget(ScreenFour(name="screen_four"))

class ScreenApp(App):
    def build(self):
        return screen_manager


if __name__ == "__main__":
    sample_app = ScreenApp()
    sample_app.run()
