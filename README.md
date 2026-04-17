Setup Guide: Prisma SASE Policy Tool (Windows & macOS)
------------------------------------------------------

This document provides step-by-step instructions to configure your environment, install the required dependencies, and execute the Python script to export Palo Alto SASE policies. The tool enables retrieval of all Security Policies from Prisma Access and Strata Cloud Manager in a streamlined and efficient manner.

-------------------------------------------------------
1. Install Python
Python is the engine that runs our script. You need Python 3.8 or higher.

For Windows:
Download: Go to python.org and download the "Windows installer (64-bit)".

Install: Run the .exe file.

CRITICAL: Check the box that says "Add Python to PATH" at the bottom of the installer window.

Click "Install Now".

Verify: Open Command Prompt and type:
python --version

For Mac:
Check: Mac usually comes with Python, but it might be an old version. Open Terminal and type:
python3 --version

Install/Update: If it's missing or old, download the macOS installer from python.org or use Homebrew:
brew install python

2. Required Python Packages
The script relies on four specific "libraries" to handle the UI, the API, and the Excel formatting:

Streamlit: Creates the web interface.
Requests: Handles the communication with Palo Alto APIs.
Pandas: Organizes the data into rows and columns.
Openpyxl: Allows Python to write .xlsx files.

3. Detailed Installation & Execution Steps
Step 1: Create a Project Folder
Create a new folder on your Desktop named sase_tool. Move your app.py file into this folder.

Step 2: Open Terminal / Command Prompt
Windows: Press Win + R, type cmd, and hit Enter.

Mac: Press Cmd + Space, type Terminal, and hit Enter.

Step 3: Navigate to the Folder
Type cd followed by the path to your folder:

Bash
# Example for Windows
cd %USERPROFILE%\Desktop\sase_tool

# Example for Mac
cd ~/Desktop/sase_tool

Step 4: Install Dependencies
Copy and paste this command to install all required packages at once:

Bash
# Windows
pip install streamlit requests pandas openpyxl

# Mac
pip3 install streamlit requests pandas openpyxl

Step 5: Run the Script
Launch the tool by running:

Bash
# Windows
streamlit run app.py

# Mac
python3 -m streamlit run app.py


4. How to Use the Tool

Once you run the command, a browser tab will open at http://localhost:8501.
Credentials: Enter your Client ID, Client Secret, and TSG ID.
Select Action: * List Security Rules: Use this for your bulk export of all 900+ rules.
Get Security Rule: Use this to look up a specific rule ID.
Folder/Position: Ensure these match where your rules live (e.g., Folder: Mobile Users, Position: pre).
Export: Click the button and wait for the "Download Excel" button to appear.
