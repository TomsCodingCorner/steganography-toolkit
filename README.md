# TABS Steganography Toolkit

A Python steganography project I built in **2024**. It started as a school assignment, but I enjoyed experimenting with it and continued developing it in my own time.

The project hides text in PNG images and retrieves it using a password-derived pixel order. It combines my TABS text encoding with image manipulation and a Kivy interface for trying it out. I enjoyed exploring how text could be represented as bits and stored through small changes to an image.

In 2026, I revisited the project to make it easier to run and share. I fixed issues affecting the demo, added tests, and documented the setup while keeping the original approach and much of the code.

**Originally developed in 2024 · Cleaned up for sharing in October 2026**

## What it does

- Encodes text into bits using the project's TABS dictionaries.
- Hides those bits in the least significant bits of PNG pixel channels.
- Uses a password and SHA-256 to determine the pixel order.
- Extracts the hidden text using the same password.
- Provides a desktop interface and a small command-line demo.

The password controls where the data is hidden. **It does not encrypt the message.** This is an educational project for exploring encoding and steganography, rather than a tool for protecting sensitive information.

## Getting started

The documented setup uses **Python 3.13 on Windows**.

Open PowerShell in the repository's root directory and run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The dependencies are Pillow, Kivy, and plyer. No separate build step is required.

The desktop interface needs a graphical environment with a working OpenGL driver. Once the dependencies are installed, the included demo runs locally without a network connection.

## Run the demo

The quickest way to try the project is to hide a sample message and read it back:

```powershell
.\.venv\Scripts\python.exe Final_Minimal_Product\STEGANOGRAPHY.py
```

The demo uses:

- The synthetic image at `Final_Minimal_Product/Input_Directory/demo.png`.
- The message in `demo_message.txt`: `This is a safe demo message.`
- The public example password: `demo-password`.

Expected output:

```text
Teruggelezen bericht: This is a safe demo message.
Demo geslaagd: het teruggelezen bericht is exact gelijk aan de invoer.
Uitvoer: <project path>/Final_Minimal_Product/Output_Directory
```

The console messages are still in Dutch. They confirm that the recovered message exactly matches the original.

The demo creates `Final_Minimal_Product/Output_Directory` automatically and saves:

| File | Contents |
| --- | --- |
| `tabs_innocentimage.png` | The image containing the hidden message. |
| `tabs_desteg_output.txt` | The recovered text: `This is a safe demo message.` |

Running the demo again overwrites these output files.

## Try the desktop interface

Start the original Kivy interface:

```powershell
.\.venv\Scripts\python.exe Final_Minimal_Product\GUI.py
```

To reproduce the same example:

1. Open **Encrypt**, click **Select Image**, and choose the included `demo.png`.
2. Enter `This is a safe demo message.` and the password `demo-password`, then click **Hide**.
3. Open **Decrypt**, select the generated `tabs_innocentimage.png`, enter the same password, and click **Uncover**.
4. Open `Final_Minimal_Product/Output_Directory/tabs_desteg_output.txt` and check the recovered message.

The original interface uses the labels **Encrypt** and **Decrypt**, although these operations hide and extract data rather than perform cryptographic encryption.

The other two screens let you experiment with TABS text-to-bits encoding and decoding separately. Generated files are saved in `Final_Minimal_Product/Output_Directory`.

## How it works

The encoder converts the message into a bit sequence using the included TABS dictionaries. A small header containing a signature and the payload length is added so the decoder can recognise the format and determine where the message ends.

A password-derived sequence selects unique pixel coordinates. The message bits are written into the least significant bits of the image's RGBA channels, changing each affected channel value by at most one.

To recover the message, the decoder recreates the coordinate sequence from the password, reads the header and payload, and converts the bits back into text.

SHA-256 is used to derive the coordinate sequence; it is not used to encrypt the message. The coordinate-generation helper was adapted from externally supplied code in the original project, as noted in its source.

## Project structure

Most of the original layout is retained under `Final_Minimal_Product`.

| File or directory | Purpose |
| --- | --- |
| `Final_Minimal_Product/GUI.py` | The original four-screen Kivy interface. |
| `Final_Minimal_Product/STEGANOGRAPHY.py` | Hiding and extracting messages in PNG images, including the automatic demo. |
| `Final_Minimal_Product/TABS.py` | Entry points for text encoding and decoding. |
| `Final_Minimal_Product/Assisting_Files/` | Encoding helpers, bit processing, coordinate generation, and Pillow image access. |
| `Final_Minimal_Product/Model/` | The two original encoding dictionaries. |
| `Final_Minimal_Product/Input_Directory/` | The sample image and message. |
| `tests/` | Regression tests and GUI smoke tests. |

The encoder selects a suitable dictionary automatically. The dictionaries were retained during cleanup, with support for a missing backtick character added.

## Limitations

- The included dictionaries support printable ASCII characters and line breaks, rather than general Unicode text.
- Unsupported characters, empty messages, insufficient image capacity, and a wrong password are rejected.
- The password-based pixel order does not provide cryptographic confidentiality or authenticated integrity.
- The current format requires the signature and length header. Images produced by the older demo without this header are not supported.
- Keep the output as PNG and preserve its pixel values. Resizing, image editing, conversion to JPEG, or services that alter images can destroy the hidden message.
- The documented installation and GUI verification target Windows. Cross-platform GUI behaviour has not been fully verified.

## Tests and verification

Run the checks from the repository root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests\gui_smoke.py
.\.venv\Scripts\python.exe -m compileall -q Final_Minimal_Product tests
.\.venv\Scripts\python.exe -m pip check
```

During the October 2026 cleanup, the project was checked on **Windows with Python 3.13.7**, including:

- Dependency installation in a fresh virtual environment.
- The complete PNG demo from a clean source copy without an existing output directory.
- Ten regression tests.
- Three GUI tests using a hidden Kivy window.

The regression tests cover both dictionaries, both bit modes, punctuation, line breaks, capacity checks, invalid input, password handling, and decoding in a separate process launched from another working directory.

The GUI tests exercise the actual button callbacks with a mocked file picker. They do not replace a manual visual check or a test of the native file dialog. No packaged executable or full Linux/macOS validation was produced during that cleanup.

## About this version

This repository is a cleaned publication of my 2024 project, rather than a record of continuous development since then.

The October 2026 update focused on getting one complete demo working reliably. It included fixes to PNG storage and decoding, safer example data, installation instructions, and automated tests. Older experiments, duplicate model directories, unused helpers, and an unfinished model-generation screen were removed.

The original encoding approach, desktop interface, and much of the implementation remain. IDE settings, virtual environments, caches, and generated output are excluded through `.gitignore`.

## License

See [LICENSE](LICENSE) for the project's license.
