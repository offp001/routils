# Contributing to RoUtils (Windows)

Thank you for your interest in contributing to **RoUtils**!

- If you liked RoUtils, Please star the the Repository


---

## Requirements

- **Python 3.12**: Python 3.12 or Higher

> During installation, make sure to check the box that says **"Add Python to PATH"** so that pip and python commands works.

---

## Compilation (Windows)

### Easy Method

You can let the scripts handle everything for you:

1. Double-click on `install_requirements.bat` to automatically install all requirements for RoUtils

2. Once that finishes, double-click on `compile.bat`.
3. When the compilation is complete, navigate to the newly created `dist` folder.
4. Open **`RoUtils.exe`** and you're good to go!

---

### Normal Method

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


# Compilation (Linux)

## Requirements

- Python 3.10 or newer
- Tkinter and Python virtual environment support

## Install Requirements;

### Debian and Ubuntu

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk python3-pip
```

### Fedora

```bash
sudo dnf install python3 python3-tkinter python3-pip
```

### Arch Linux

```bash
sudo pacman -S python tk python-pip
```

## Start Compiling

## Easy Method

Extract the complete project directory, open a terminal in that directory, then run:

```bash
chmod +x install.sh run.sh compile.sh
./install.sh
./compile.sh
```

After Compiling done, Run this.

```bash
chmod +x dist/routils
./dist/routils

```



## Normal Method

Create and activate the virtual environment:

```bash
python3 -m venv venv

```

Activate the created virtual environment:

```bash
source venv/bin/activate

```

Upgrade pip to the latest version (again):

```bash
python -m pip install --upgrade pip

```

Install all required Python packages and Pyinstaller:

```bash
python -m pip install numpy DracoPy Pillow lz4 zstandard sv-ttk ttkbootstrap pypresence psutil pynput cryptography 'mitmproxy>=11,<13' pyinstaller

```

Run a Python syntax check across the files:

```bash
python -m compileall -q main.pyw sober_support.py ai cache client console emote_manager fflag history home plugins release_notes server_viewer settings subplace themes viewer sober_proxy

```

Build the executable:

```bash
python -m PyInstaller --clean --noconfirm --onefile --windowed --name routils --paths "$PWD" --add-data "$PWD/routils.ico:." --add-data "$PWD/routils_rpc.png:." --collect-all sv_ttk --collect-all ttkbootstrap --hidden-import pynput.keyboard._xorg --hidden-import pynput.mouse._xorg main.pyw

```

Grant execution permission:

```bash
chmod +x dist/routils

```

Run it:

```bash
./dist/routils

```

*RoUtils by offp001*
