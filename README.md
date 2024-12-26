# Secure Python Loader

A secure loader application with KeyAuth authentication and custom animated GUI.

## Setup Instructions

### For Users with Source Code

1. Install Python 3.x (tested with Python 3.8+)
2. Install required packages:
   ```bash
   pip install keyauth.py customtkinter pillow pyinstaller
   ```

### KeyAuth Setup

1. Go to [KeyAuth.win](https://keyauth.win) and create an account
2. Create a new application
3. Copy your application details:
   - Application Name
   - Owner ID
   - Application Secret
4. Replace these values in `config.py`

### Building the Executable

1. Open command prompt in the project directory
2. Run:
   ```bash
   pyinstaller --onefile --noconsole --icon=assets/icon.ico main.py
   ```
3. Find your executable in the `dist` folder

### Customizing the Loader

To change what the loader executes after successful authentication:
1. Open `main.py`
2. Locate the `on_login_success()` function
3. Modify the code inside this function to execute your desired actions

## Features
- Secure KeyAuth Authentication
- Custom animated dark theme GUI
- Modern design with customtkinter
- Secure error handling 