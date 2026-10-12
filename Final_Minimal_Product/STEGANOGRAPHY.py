"""Hide TABS bits in PNG pixels using a password-derived coordinate order."""

from pathlib import Path

from Assisting_Files import Image, Hash
from TABS import EN_TABS, DE_TABS

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Output_Directory"
# A signature and bit length stop decoding before the unused pixels.
SIGNATURE = "".join(f"{byte:08b}" for byte in b"TABS")
HEADER_BITS = 64


class Obfuscate:
    def __init__(self, image_path, message, password=None):
        if not message or not image_path or not password:
            raise ValueError("Choose an image and enter a message and password.")
        self.password = password
        self.message = message
        self.image_path = image_path
        self.img = Image.ImgC(image_path)
        self.imagebits, self.imagewidth, self.imageheight = self.img.byteammount()
        self.whatineed()
        if self.len_bin_mssg > self.imagebits:
            raise ValueError("The message is too large for this image.")
        self.rndmpxl_hash()
        self.luobfuscatatione()
        self.return_image()

    def return_image(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.output_path = OUTPUT_DIR / "tabs_innocentimage.png"
        self.img.save(self.output_path)
        return self.output_path

    def whatineed(self):
        payload = EN_TABS(message=self.message, optimized=False)
        self.binary_message = SIGNATURE + f"{len(payload):032b}" + payload
        self.len_bin_mssg = len(self.binary_message)

    def rndmpxl_hash(self):
        rng = Hash.RandomNumberGenerator(
            image_width=self.imagewidth, image_height=self.imageheight,
            password=str(self.password), num_coordinates=(self.len_bin_mssg + 3) // 4)
        self.indexorder = rng.getcoordinates()

    def luobfuscatatione(self):
        offset = 0
        for coordinate in self.indexorder:
            pixel = list(self.img.getpixel(x=coordinate))
            for channel in range(4):
                if offset == self.len_bin_mssg:
                    break
                pixel[channel] = (pixel[channel] & ~1) | int(self.binary_message[offset])
                offset += 1
            # Preserve the remaining channels in the last pixel.
            self.img.setpixel(x=coordinate, value=tuple(pixel))


class Deobfuscate:
    def __init__(self, image_path, password=None):
        if not image_path or not password:
            raise ValueError("Choose an image and enter a password.")
        self.password = password
        self.image_path = image_path
        self.img = Image.ImgC(image_path)
        self.imagebits, self.imagewidth, self.imageheight = self.img.byteammount()
        if self.imagebits < HEADER_BITS:
            raise ValueError("This image is too small to contain a TABS message.")
        header = self.ludeobfuscatatione(HEADER_BITS)
        if header[:32] != SIGNATURE:
            raise ValueError("Incorrect password or no TABS message in this image.")
        length = int(header[32:], 2)
        if not 8 <= length <= self.imagebits - HEADER_BITS:
            raise ValueError("Invalid message length; the image may be damaged.")
        self.binary_message = self.ludeobfuscatatione(HEADER_BITS + length)[HEADER_BITS:]
        self.whatidontneed()

    def whatidontneed(self):
        self.message = DE_TABS(binary=self.binary_message)

    def return_message(self):
        return self.message

    def givebackfile(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUTPUT_DIR / "tabs_desteg_output.txt"
        path.write_text(self.message, encoding="utf-8")
        return path

    def ludeobfuscatatione(self, bit_count):
        rng = Hash.RandomNumberGenerator(
            image_width=self.imagewidth, image_height=self.imageheight,
            password=str(self.password), num_coordinates=(bit_count + 3) // 4)
        bits = [str(channel & 1) for coordinate in rng.getcoordinates()
                for channel in self.img.getpixel(x=coordinate)]
        return "".join(bits)[:bit_count]


if __name__ == "__main__":
    message = (BASE_DIR / "Input_Directory" / "demo_message.txt").read_text(encoding="utf-8").rstrip("\n")
    hidden = Obfuscate(BASE_DIR / "Input_Directory" / "demo.png", message, "demo-password")
    decoded = Deobfuscate(hidden.output_path, "demo-password")
    decoded.givebackfile()
    if decoded.return_message() != message:
        raise RuntimeError("The decoded message does not match the input.")
    print(f"Teruggelezen bericht: {decoded.return_message()}")
    print("Demo geslaagd: het teruggelezen bericht is exact gelijk aan de invoer.")
    print(f"Uitvoer: {OUTPUT_DIR}")
