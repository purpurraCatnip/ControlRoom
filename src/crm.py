import sys
import json
import csv
import os

from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtWidgets import(
    QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QGridLayout, QLineEdit, QHBoxLayout, QScrollArea, QSizePolicy, QFrame, QSpacerItem, QFileDialog
)

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Control Room Manager")
        self.setWindowIcon(QIcon('./assets/icon.png'))
        self.setContentsMargins(0, 0, 20, 20)
        self.setProperty("class", "Main")

        layout = QGridLayout()
        self.setLayout(layout)

        #Contact List is RIIIIIGHT here !! c: 
        contactWin = QWidget()
        contactWin.setProperty("class", "contacts")
        contactWin.setMinimumSize(800, 450)
        contactWin.setMaximumSize(10000, 500)
        layout.addWidget(contactWin, 0, 0)

        contacts = QVBoxLayout()
        contactWin.setLayout(contacts)

        #Highlighted Contact Holder!! :D
        focusContact = QWidget()
        focusContact.setProperty("class", "contacts")
        focusContact.setMinimumSize(800, 400)
        focusContact.setMaximumSize(10000, 450)
        focusLayout = QHBoxLayout()
        focusContact.setLayout(focusLayout)
        layout.addWidget(focusContact, 1, 0)

        #Contact List Title
        title = QLabel(
            '<b>contacts</b>',
            alignment=Qt.AlignmentFlag.AlignLeft,
        )
        title.setProperty("class", "title")

        subheader = QLabel(
            'View All of Your Contacts!',
            alignment=Qt.AlignmentFlag.AlignLeft,
        )

        #Scroll Window!! :D
        scrollWindow = QWidget()
        scrollWindow.setProperty("class", "scrollWindow")
        scrollLayout = QVBoxLayout()
        scrollWindow.setLayout(scrollLayout)
        scroll = QScrollArea()
        scroll.setStyleSheet("QScrollArea{background-color: rgba(0, 0, 0, 0);}")
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(360)
        scroll.setWidget(scrollWindow)


        #This is to help select the contacts!!
        selectedHelper = -1

        contactArr = []
        saveDat = []

        class PFP(QLabel):
            def __init__(self):
                super().__init__()

                # Create a QLabel for the profile picture
                self.setFixedSize(200, 200)
                self.setScaledContents(True)
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Connect the clicked signal of the profile picture label to open the file picker
                self.mousePressEvent = self.openFilePicker

            def openFilePicker(self, event):
                # Open the file picker dialog to select a new profile picture
                file_name, _ = QFileDialog.getOpenFileName(
                    self, "Select Profile Picture", "", "Image Files (*.png *.jpg *.jpeg)"
                )
                
                if file_name:
                    # Update the profile picture if a file is selected
                    self.setPixmap(QPixmap(file_name))
                    saveDat[selectedHelper]["PFP"] = file_name

        #This is for backend stuff, allows for saving and what not
        def createDict(name = '', add = '', phone = '', email = '', pfpURL = './assets/patchy.png', notes=''):
            newContact = {
                "Name": name,
                "Phone Number": phone,
                "Address": add,
                "E-Mail Address": email,
                "PFP": pfpURL,
                "Notes": notes,
            }

            saveDat.append(newContact)
        
        def saveContacts(arr):
            with open('./assets/saveData/contacts.json', 'w') as file:
                json.dump(arr, file, indent=4)
        
        #Creates the Focused Widget, non-functional YET, it gains functionality in the next function~
        selectedCont = QWidget()
        selectedCont.setVisible(False)
        selectedCont.setProperty("class", "focusedContact")
        grid = QGridLayout()
        selectedCont.setLayout(grid)

        selectedCont.PfpURL = './assets/patchy.png'
        selectedCont.PfpMap = QPixmap(selectedCont.PfpURL).scaled(200, 200)
        selectedCont.Pfp = PFP()
        selectedCont.Pfp.setPixmap(selectedCont.PfpMap)

        selectedCont.Name = QLineEdit("Name")
        selectedCont.Name.setProperty("class", "focusName")
        selectedCont.Name.setMaximumSize(10000, 60)

        selectedCont.AddLabel = QTextEdit("Address")
        selectedCont.AddLabel.setProperty("class", "focusLabels")
        selectedCont.AddLabel.setMinimumSize(300, 0)

        selectedCont.PhoneLabel = QTextEdit("Number")
        selectedCont.PhoneLabel.setProperty("class", "focusLabels")
        selectedCont.PhoneLabel.setMinimumSize(300, 0)


        selectedCont.EmailLabel = QTextEdit("Email")
        selectedCont.EmailLabel.setProperty("class", "focusLabels")
        selectedCont.EmailLabel.setMinimumSize(300, 0)


        selectedCont.NoteLabel = QLabel("Notes")
        selectedCont.NoteLabel.setStyleSheet("color: #000; margin-left: 10px;")

        selectedCont.NoteField = QTextEdit()
        selectedCont.NoteField.setPlaceholderText("Add Text")
        selectedCont.NoteField.setProperty("class", "focusNotes")
        selectedCont.NoteField.setMinimumSize(250, 50)
        selectedCont.NoteField.setMaximumSize(10000, 100)

        saveButton = QPushButton("Save Changes")
        saveButton.setProperty("class", "focusSave")
        saveButton.setMaximumSize(150, 40)

        deleteButton = QPushButton("Delete Contact")
        deleteButton.setProperty("class", "focusDelete")
        deleteButton.setMaximumSize(150, 40)

        spacer = QWidget()
        spacer.setMinimumSize(0, 50)

        noteHolder = QWidget()
        noteLayout = QVBoxLayout()
        noteHolder.setLayout(noteLayout)
        noteHolder.setMaximumSize(10000, 100)
        noteLayout.addWidget(selectedCont.NoteLabel)
        noteLayout.addWidget(selectedCont.NoteField)
        
        grid.addWidget(selectedCont.Pfp, 0, 0, 3, 1)
        grid.addWidget(selectedCont.Name, 0, 1, 1, 3)
        grid.addWidget(selectedCont.AddLabel, 1, 1)
        grid.addWidget(selectedCont.EmailLabel, 1, 2)
        grid.addWidget(selectedCont.PhoneLabel, 1, 3)
        grid.addWidget(noteHolder, 2, 1, 1, 3)
        grid.addWidget(deleteButton, 3, 0)
        grid.addWidget(saveButton, 3, 1)
        grid.addWidget(spacer, 3, 2)

        focusLayout.addWidget(selectedCont)

        #This changes the selected contact stuff to match with the selected contact! Its called when the widget gets clicked on <|:)
        def selectedContact(id):
            tempPixmap = QPixmap(saveDat[id].get("PFP", './assets/patchy.png')).scaled(200, 200)
            selectedCont.PfpMap = tempPixmap
            print(saveDat[id].get("PFP"))
            selectedCont.Pfp.setPixmap(selectedCont.PfpMap)

            if(saveDat[id].get("Name") == ' N/A'):
                selectedCont.Name.setText('N/A')
            else:
                selectedCont.Name.setText(saveDat[id].get("Name", 'No name!'))

            selectedCont.AddLabel.setText(saveDat[id].get("Address", 'N/A'))
            selectedCont.EmailLabel.setText(saveDat[id].get("E-Mail Address", 'N/A'))
            selectedCont.PhoneLabel.setText(saveDat[id].get("Phone Number", 'N/A'))
            selectedCont.NoteField.setText(saveDat[id].get("Notes", ''))

            selectedCont.setVisible(True)

        #This is so I can actually make the holder for the contacts clickable.
        class contactHolder(QFrame):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.show()
            
            def mousePressEvent(self, e):
                nonlocal selectedHelper
                nonlocal focusLayout
                if selectedHelper != self.ID:
                    #These make the non-selected widgets back to their default state!
                    contactArr[selectedHelper].setProperty("class", "contact")
                    contactArr[selectedHelper].style().unpolish(contactArr[selectedHelper])
                    contactArr[selectedHelper].style().polish(contactArr[selectedHelper])
                    selectedHelper = self.ID

                    #This sets the new QSS Class for a selected widget!
                    self.setProperty("class", "contactSel")
                    self.style().unpolish(self)
                    self.style().polish(self)
                    
                    #This loads the focus widget, allowing you to change things!
                    selectedContact(self.ID)

                    #Allows me to see which one is selected <|:)
                    print("Hi! Click!")
                    print(self.ID)

                else:
                    print("Mismatched ID? " + str(selectedHelper))
                    print("Hey! I'm already clicked!")

        #This function actually creates the contact in the list!
        def createContact(first="first", last="last", pfpURL='./assets/patchy.png', add='address', email='email', phone='phone number', notes=''):
            hold = contactHolder()
            hold.setProperty("class", "contact")

            gridLayout = QGridLayout()
            hold.setLayout(gridLayout)

            hold.firstLabel = QLabel(first, alignment=Qt.AlignmentFlag.AlignCenter)
            hold.firstLabel.setProperty("class", "firstName")
            hold.firstLabel.setMaximumSize(70, 50)

            hold.lastLabel = QLabel(last, alignment=Qt.AlignmentFlag.AlignCenter)
            hold.lastLabel.setProperty("class", "lastName")
            hold.lastLabel.setMaximumSize(70, 50)

            pfpMap = QPixmap(pfpURL).scaled(40, 40)
            hold.pfp = QLabel()
            hold.pfp.setPixmap(pfpMap)
            hold.pfp.setMinimumSize(40, 40)
            hold.pfp.setMaximumSize(40, 40)

            hold.addLabel = QLabel(add)
            hold.addLabel.setProperty("class", "contLabels")

            hold.emailLabel = QLabel(email)
            hold.emailLabel.setProperty("class", "contLabels")

            hold.phoneLabel = QLabel(phone)
            hold.phoneLabel.setProperty("class", "contLabels")

            stretcher = QWidget()
            stretcher.setMaximumSize(30, 0)

            gridLayout.addWidget(hold.firstLabel, 0, 0)
            gridLayout.addWidget(hold.lastLabel, 0, 1)
            gridLayout.addWidget(hold.pfp, 0, 2)
            gridLayout.addWidget(stretcher, 0, 3)
            gridLayout.addWidget(hold.addLabel, 0, 4)
            gridLayout.addWidget(hold.emailLabel, 0, 5)
            gridLayout.addWidget(hold.phoneLabel, 0, 6)

            hold.setMinimumSize(60, 60)
            hold.setMaximumSize(10000, 60)

            #This appends the contact to the array, as well as setting its ID value, and save data!
            contactArr.append(hold)
            createDict(first + ' ' + last, add, phone, email, pfpURL, notes)
            hold.ID = len(contactArr) - 1
            
            #These are for me to see if its all good <|;)
            print(hold.ID)
            print(contactArr)

            #Returns the holder so i can add it!
            saveContacts(saveDat)
            return hold
        
            #End of Contact Function

        #These are the button functions!

        def deleteContact(id):
            contactArr[id].deleteLater()
            del contactArr[id]
            del saveDat[id]

            i = 0
            for element in contactArr:
                if element.ID != i:
                    print("!!! Mismatch ID!!! Oh no!")
                    element.ID = i
                i += 1

            selectedCont.setVisible(False)
            nonlocal selectedHelper
            selectedHelper = -1

            saveContacts(saveDat)
        
        def saveChanges(id):
            name = selectedCont.Name.text()
            add = selectedCont.AddLabel.toPlainText()
            email = selectedCont.EmailLabel.toPlainText()
            phone = selectedCont.PhoneLabel.toPlainText()
            pfpURL = saveDat[id].get("PFP")
            if(pfpURL == ''):
                pfpURL = './assets/patchy.png'
            pfp = QPixmap(pfpURL).scaled(40, 40)

            saveDat[id]["Name"] = name
            saveDat[id]["Address"] = add
            saveDat[id]["Phone Number"] = phone
            saveDat[id]["E-Mail Address"] = email
            saveDat[id]["Notes"] = selectedCont.NoteField.toPlainText()

            print(saveDat[id]["Notes"])

            selectedContact(id)
            if ' ' in name:
                print("found a space")
                lastName = name[name.find(' '):]
                firstName = name[:name.find(' ')]
            else:
                firstName = name
                lastName = 'N/A'

            contactArr[id].firstLabel.setText(firstName)
            contactArr[id].lastLabel.setText(lastName)
            contactArr[id].addLabel.setText(add)
            contactArr[id].emailLabel.setText(email)
            contactArr[id].phoneLabel.setText(phone)
            contactArr[id].pfp.setPixmap(pfp)
            saveContacts(saveDat)

        saveButton.clicked.connect(lambda: saveChanges(selectedHelper))
        deleteButton.clicked.connect(lambda: deleteContact(selectedHelper))

        def loadContacts():
            with open('./assets/saveData/contacts.json', 'r') as file:
                saveDat = json.load(file)

                for entry in saveDat:
                    name = entry["Name"]
                    names = name.split(' ')
                    firstName = names[0]
                    lastName = ' '.join(names[1:]) if len(names) > 1 else 'N/A'

                    scrollLayout.addWidget(createContact(firstName, lastName, entry["PFP"], entry["Address"], entry["E-Mail Address"], entry["Phone Number"], entry["Notes"]), alignment=Qt.AlignmentFlag.AlignTop)
        if os.path.exists('./assets/saveData/contacts.json'):
            loadContacts()
        
        #This function creates a contact when the add contact button is pressed. It has to be waaaay up here because of python's weird bullshit
        def testFunc(name, phone, add, email):
            lastName = 'N/A'
            firstName = name
            if ' ' in name:
                lastName = name[name.find(' '):]
                firstName = name[:name.find(' ')]
            if phone == '':
                phone = 'N/A'
            if add == '':
                add = 'N/A'
            if email == '':
                email = 'N/A'
            scrollLayout.addWidget(createContact(firstName, lastName, './assets/patchy.png', add, email, phone), alignment=Qt.AlignmentFlag.AlignTop)

        #All of this is for creating the stuff that goes in the contact list. It also has to be down here because of python
        subheader.setProperty("class", "sub")

        contacts.addWidget(title)
        contacts.addWidget(subheader)
        #scrollLayout.addWidget(createContact("Terezi", "Pyrope", './assets/tezi.png', '1401 Alternia Blvd', 'gallowsCallibrator@skaia.net', '(555) 123-4567'), alignment=Qt.AlignmentFlag.AlignTop)

        contacts.addWidget(scroll)

        #NEW CONTACT FORM IS HERE !!! <|:3
        newContactWin = QWidget()
        layout.addWidget(newContactWin, 0, 1, 2, 1, Qt.AlignmentFlag.AlignRight) #Important: This makes it span 2 rows
        newContacts = QVBoxLayout()
        newContacts.setSpacing(10)
        newContactWin.setLayout(newContacts)

        #Functions for the labels and text fields
        def contLabel(string, layout):
            label = QLabel(string)
            label.setProperty("class", "newContactLabels")
            layout.addWidget(label)
        
        def helpLabel(string, layout):
            label = QLabel(string)
            label.setProperty("class", "helpText")
            layout.addWidget(label)

        def contField(field, layout):
            field.setPlaceholderText("Add Text")
            field.setProperty("class", "newContactText")
            field.setMinimumSize(250, 50)
            field.setMaximumSize(300, 75)
            layout.addWidget(field)
        
        def export_to_csv(data):
            fieldnames = data[0].keys()
            
            with open('./assets/saveData/contacts.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
    
        #This actually adds in all of the stuff for the new contact form!
        newContactLabel = QLabel('<b>add new contact </b>')
        newContactLabel.setStyleSheet("color: #000000;" "font-size: 20px;" "padding: 5px;")
        newContacts.addWidget(newContactLabel)
        
        contLabel('Name', newContacts)
        nameField = QLineEdit()
        contField(nameField, newContacts)
        helpLabel("Type your Contact's Name here (Required)", newContacts)

        contLabel('Phone Number', newContacts)
        phoneField = QLineEdit()
        contField(phoneField, newContacts)
        helpLabel("Type your Contact's Phone Number here (Optional)", newContacts)

        contLabel('Address', newContacts)
        addField = QTextEdit()
        contField(addField, newContacts)
        helpLabel("Type your Contact's Address here (Optional)", newContacts)

        contLabel('Email', newContacts)
        emailField = QLineEdit()
        emailField.setPlaceholderText("jade@harley.com")
        emailField.setProperty("class", "emailField")
        emailField.setMaximumSize(300, 50)
        newContacts.addWidget(emailField)
        helpLabel("Type your Contact's Email Address here (Required)", newContacts)

        submit = QPushButton("Add Contact ==>")
        submit.setFixedWidth(250)
        submit.setProperty("class", "addButton")
        submit.clicked.connect(lambda: testFunc(nameField.text(), phoneField.text(), addField.toPlainText(), emailField.text()))
        newContacts.addWidget(submit, Qt.AlignmentFlag.AlignHCenter)

        newContacts.addStretch()
        contacts.addStretch()

        csvButton = QPushButton("Export to CSV ==>")
        csvButton.setFixedWidth(150)
        csvButton.setProperty("class", "focusSave")
        csvButton.clicked.connect(lambda: export_to_csv(saveDat))
        newContacts.addWidget(csvButton, Qt.AlignmentFlag.AlignHCenter)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.setStyleSheet(Path('./styles/sheet.qss').read_text())
    sys.exit(app.exec())