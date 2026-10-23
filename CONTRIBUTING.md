# Contributing to RoUtils

Thank you for your interest in contributing to **RoUtils**!

---

## Prerequisites

Before compiling or working on RoUtils, make sure you have the following installed on your system:

* **Python 3.12**: If you don't have it installed, you can download it directly from the [Official Python 3.12 Download Page](https://www.python.org/downloads/release/python-3120/).
> *Important:* During installation, make sure to check the box that says **"Add Python to PATH"** so that pip and python commands work seamlessly in your terminal.


* **PIP**: Usually comes bundled with Python 3.12. You can verify it by running `pip --version` in your terminal.

---

## Compilation Methods

You can compile RoUtils from source using either the **Easy Method** (recommended for quick builds) or the **Manual Method**.

### Method 1: The Easy Way

You can let the scripts handle everything for you:

1. Double-click on `install_requirements.bat` to automatically install all requirements for RoUtils
2. Once that finishes, double-click on `compile.bat`.
3. When the compilation is complete, navigate to the newly created `dist` folder.
4. Open **`RoUtils.exe`** and you're good to go!

---

### Method 2: The Manual Way (Terminal)

If you prefer full control over the process step-by-step:

1. Open your terminal (CMD, etc) inside the project folder.
2. Verify that Python 3.12 and pip are ready by checking your environment.
3. Install the required dependencies by running:
```bash
pip install -r requirements.txt

```


4. Build the executable using PyInstaller with the clean configuration:
```bash
py -3.12 -m PyInstaller --noconfirm --clean --onefile --windowed --icon=routils.ico --add-data "routils.ico;." --name=RoUtils main.pyw

```


5. Wait for the compilation process to finish.
6. Navigate into the output directory:
```bash
cd dist

```


7. Open the compiled RoUtils directly from the terminal:
```bash
.\RoUtils.exe

```


8. Alternatively, you can open the source folder, go into the `dist` folder, and simply double-click **`RoUtils.exe`** to run it without needing a terminal.

---

*RoUtils by offp001*
