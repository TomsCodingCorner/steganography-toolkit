"""Regression checks for the retained demo, using synthetic data only."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "Final_Minimal_Product"
sys.path.insert(0, str(APP_DIR))

from PIL import Image
import STEGANOGRAPHY as steg
from TABS import EN_TABS, DE_TABS
from Assisting_Files.DecimalProcessing import endecimalprocessing, dedecimalprocessing
from Assisting_Files.Hash import RandomNumberGenerator


class DemoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.output = self.directory / "output"
        self.patch = patch.object(steg, "OUTPUT_DIR", self.output)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.image = APP_DIR / "Input_Directory" / "demo.png"

    def test_original_models_and_bit_modes_roundtrip(self):
        messages = ["", "This is a safe demo message.", "Line 1\nLine 2! T3?f0",
                    "".join(chr(i) for i in range(32, 127)), "A" * 300]
        for model in sorted((APP_DIR / "Model").glob("*.json")):
            for optimized in (False, True):
                for message in messages:
                    with self.subTest(model=model.name, optimized=optimized, message=message[:20]):
                        self.assertEqual(DE_TABS(EN_TABS(message, optimized, model)), message)

    def test_decimal_chunk_width_changes_roundtrip(self):
        values = [0] * 35 + list(range(256)) + [1] * 40 + [255] * 20
        for optimized in (False, True):
            binary = endecimalprocessing(values, optimization=optimized).santa()
            self.assertEqual(dedecimalprocessing(binary).santa(), values)

    def test_invalid_binary_is_rejected(self):
        for binary in ("", "abc", "00000", "11110000", "111101110"):
            with self.subTest(binary=binary), self.assertRaises(ValueError):
                DE_TABS(binary)

    def test_unsupported_characters_are_rejected(self):
        with self.assertRaises(ValueError):
            EN_TABS("Unsupported: \U0001f642")

    def test_coordinate_order_is_unique_and_password_dependent(self):
        def coordinates(password, count):
            return RandomNumberGenerator(64, 64, password, count).getcoordinates()
        short = coordinates("demo-password", 16)
        long = coordinates("demo-password", 100)
        self.assertEqual(short, long[:16])
        self.assertEqual(len(set(long)), 100)
        self.assertNotEqual(short, coordinates("other-password", 16))

    def test_png_roundtrip_and_small_pixel_changes(self):
        message = "Two lines!\nT3?f0 remains part of the message."
        hidden = steg.Obfuscate(self.image, message, "demo-password")
        recovered = steg.Deobfuscate(hidden.output_path, "demo-password")
        self.assertEqual(recovered.return_message(), message)
        self.assertEqual(recovered.givebackfile().read_text(encoding="utf-8"), message)
        with Image.open(self.image) as source, Image.open(hidden.output_path) as result:
            source = source.convert("RGBA")
            self.assertEqual(result.size, source.size)
            for original, modified in zip(source.getdata(), result.getdata()):
                self.assertTrue(all(abs(a - b) <= 1 for a, b in zip(original, modified)))

    def test_unused_channels_in_last_pixel_are_preserved(self):
        hidden = steg.Obfuscate(self.image, "A", "demo-password")
        used = hidden.len_bin_mssg % 4
        self.assertNotEqual(used, 0)
        coordinate = hidden.indexorder[-1]
        with Image.open(self.image) as source:
            original = source.convert("RGBA").getpixel(coordinate)
        self.assertEqual(hidden.img.getpixel(coordinate)[used:], original[used:])

    def test_wrong_password_and_unencoded_image_are_rejected(self):
        hidden = steg.Obfuscate(self.image, "Safe message", "demo-password")
        for image, password in [(hidden.output_path, "wrong"), (self.image, "demo-password")]:
            with self.subTest(image=image.name), self.assertRaises(ValueError):
                steg.Deobfuscate(image, password)

    def test_capacity_and_empty_input_are_rejected(self):
        tiny = self.directory / "tiny.png"
        Image.new("RGB", (2, 2)).save(tiny)
        with self.assertRaises(ValueError):
            steg.Obfuscate(tiny, "Too large", "demo-password")
        with self.assertRaises(ValueError):
            steg.Deobfuscate(tiny, "demo-password")
        with self.assertRaises(ValueError):
            steg.Obfuscate(self.image, "", "demo-password")

    def test_separate_processes_and_unrelated_working_directory(self):
        encoded = self.directory / "encoded.png"
        message = "Cross-process demo.\nExact text!"
        setup = "import sys; sys.path.insert(0, sys.argv[1]); import STEGANOGRAPHY as s; from pathlib import Path; "
        subprocess.run([sys.executable, "-c", setup +
                        "s.OUTPUT_DIR = Path(sys.argv[2]); h = s.Obfuscate(sys.argv[3], sys.argv[4], 'demo-password'); h.img.save(sys.argv[5])",
                        str(APP_DIR), str(self.output), str(self.image), message, str(encoded)],
                       cwd=self.directory, check=True, capture_output=True, text=True)
        result = subprocess.run([sys.executable, "-c", setup +
                                 "print(s.Deobfuscate(sys.argv[2], 'demo-password').return_message())",
                                 str(APP_DIR), str(encoded)],
                                cwd=self.directory, check=True, capture_output=True, text=True)
        self.assertEqual(result.stdout.rstrip("\n"), message)


if __name__ == "__main__":
    unittest.main()
