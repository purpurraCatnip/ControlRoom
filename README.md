Control Room Manager
============

A simple contact book application that allows users to manage their contacts, add new contacts, delete existing contacts, and export contacts to CSV format!!! <|:D

Installation
------------

1. Clone the repository:

   git clone https://github.com/purpurraCatnip/ControlRoom.git

2. Navigate to the project directory:

   cd ControlRoom

3. Set up a virtual environment (optional):

   python3 -m venv venv
   source venv/bin/activate

4. Install the required dependencies:

   pip install -r requirements.txt

Usage
-----

1. Run the program:

   python3 crm.py

2. Use the following commands to interact with the contact book:
   
   Use the GUI To add, remove, and edit Contacts! The book saves your contacts to assets/saveData/contacts.json
   every time you do an action, so you don't need to worry about losing your stuff! Click on the profile picture
   in the bottom most box to swap it out with a desired image! You can also Export to a CSV file, also located in
   assets/saveData! Enjoy <|:D 

File Structure
--------------

The file structure of the project is organized as follows:

ControlRoom/
  .venv/
  assets/
    saveData/
      contacts.json
    other asset files...
  src/
    crm.py
  styles/
    sheet.qss
  README.md
  requirements.txt

- `.venv/`: Virtual environment directory (created if you set up a virtual environment).
- `assets/`: Folder containing asset files, including the `saveData/` directory where the `contacts.json` file is stored, and the `contacts.csv` files get exported to.
- `crm.py`: The main Python file containing the contact book program.
- `sheet.qss`: The style sheet file for customizing the program's appearance.
- `README.md`: The documentation file you're currently reading.

License
-------

This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
------------

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

Contact
-------

If you have any questions or feedback, feel free to contact me at purpurraCatnip@gmail.com, or reach out at hightekhextress on Discord / Twitter!
