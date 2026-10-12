"""Exercise the original Kivy screen bindings with a hidden test window."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "Final_Minimal_Product"
sys.path.insert(0, str(APP_DIR))
os.environ["KIVY_HOME"] = str(ROOT / ".tmp" / "kivy")
os.environ["KIVY_NO_ARGS"] = "1"
# A hidden SDL window may report zero DPI; use deterministic test metrics.
os.environ["KIVY_DPI"] = "96"
os.environ["KIVY_METRICS_DENSITY"] = "1"
os.environ["KIVY_METRICS_FONTSCALE"] = "1"

from kivy.config import Config
Config.set("graphics", "window_state", "hidden")
import GUI
import STEGANOGRAPHY as steg
from kivy.core.window import Window
from TABS import DE_TABS


def press(screen, label):
    button = next(widget for widget in screen.walk() if getattr(widget, "text", None) == label)
    button.dispatch("on_press")


class GuiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "output"
        self.output.mkdir()
        for module in (GUI, steg):
            patcher = patch.object(module, "OUTPUT_DIR", self.output)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.manager = GUI.ScreenApp().build()

    def test_hide_and_uncover_buttons(self):
        screen = self.manager.get_screen("screen_one")
        image = APP_DIR / "Input_Directory" / "demo.png"
        with patch.object(GUI.filechooser, "open_file", return_value=[str(image)]):
            press(screen, "Select Image")
        screen.ids.textinput.text = "This is a safe demo message."
        screen.ids.passinput.text = "demo-password"
        press(screen, "Hide")
        encoded = self.output / "tabs_innocentimage.png"
        self.assertTrue(encoded.is_file())
        screen = self.manager.get_screen("screen_two")
        with patch.object(GUI.filechooser, "open_file", return_value=[str(encoded)]):
            press(screen, "Select Image")
        screen.ids.passinput.text = "demo-password"
        press(screen, "Uncover")
        self.assertEqual((self.output / "tabs_desteg_output.txt").read_text(),
                         "This is a safe demo message.")

    def test_text_and_binary_buttons(self):
        screen = self.manager.get_screen("screen_three")
        sample = APP_DIR / "Input_Directory" / "demo_message.txt"
        with patch.object(GUI.filechooser, "open_file", return_value=[str(sample)]):
            press(screen, "Select File")
        press(screen, "Binary")
        binary_file = self.output / "tabs_binair_output.txt"
        self.assertEqual(DE_TABS(binary_file.read_text()), "This is a safe demo message.")
        screen = self.manager.get_screen("screen_four")
        screen.ids.textinput1.text = ""
        with patch.object(GUI.filechooser, "open_file", return_value=[str(binary_file)]):
            press(screen, "Select TextFile")
        press(screen, "Get str")
        self.assertEqual((self.output / "tabs_string_output.txt").read_text(),
                         "This is a safe demo message.")

    def test_navigation_and_incomplete_input(self):
        screen = self.manager.get_screen("screen_one")
        press(screen, "Binary to string")
        self.assertEqual(self.manager.current, "screen_four")
        if hasattr(screen, "filepath"):
            del screen.filepath
        with patch.object(GUI, "Popup") as popup:
            press(screen, "Hide")
            popup.return_value.open.assert_called_once()


if __name__ == "__main__":
    try:
        unittest.main()
    finally:
        Window.close()
