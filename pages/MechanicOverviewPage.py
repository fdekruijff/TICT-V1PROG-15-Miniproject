"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import functools
import tkinter as tk
from tkinter import *


class MechanicOverviewPage(tk.Frame):
    """
        This TkInter object holds all information for all Mechanic objects,
        it's also able to display specific information and perform actions on that object.
    """

    def __init__(self, parent, controller):
        """ Object constructor """
        tk.Frame.__init__(self, parent)

        # Initialise variables
        self.controller = controller
        self.searchString = []
        self.tempLabel = None
        self.selectedMechanic = None
        self.informationLabels = ["Name: ", "Region: ", "Age: ", "Phone: ", "Availability: ", "Shift: "]
        self.informationHeaders = ["General Information", "Actions"]
        self.actionButtons = [
            {"text": "Change availability", "command": "self.change_availability"},
            {"text": "Change shift", "command": "self.change_shift"},
            {"text": "Modify personal information", "command": "self.update_mechanic_information"},
            {"text": "Remove Mechanic", "command": "self.remove_mechanic"},
        ]

        # Declaration of Background Frame
        self.backgroundContainer = Frame(self)
        self.backgroundContainer.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.backgroundContainer.configure(background="#fcc63f", width=1000, height=480)

        # Declaration of 'Back' Button
        self.notificationButton = Button(self.backgroundContainer)
        self.notificationButton.place(relx=0, rely=0, relheight=0.10, relwidth=0.25)
        self.notificationButton.configure(
            text='Back',
            command=functools.partial(self.controller.show_frame, "StartPage"),
            background=self.controller.buttonBackgroundColor,
            foreground=self.controller.buttonForegroundColor,
            relief=self.controller.buttonRelief
        )

        # Declaration of entry field
        self.searchEntry = Entry(self.backgroundContainer)
        self.searchEntry.place(relx=0.25, rely=0.0, relheight=0.10, relwidth=0.75)
        self.searchEntry.configure(background="white", foreground="grey", insertbackground="black", justify="center")
        self.searchEntry.insert(0, "Search for name, region or availability")
        self.searchEntry.bind('<FocusIn>', self.on_entry_click)
        self.searchEntry.bind("<Key>", self.search_mechanic)

        # Declaration of left Listbox to list all Mechanic objects
        self.mechanicListBox = Listbox(self.backgroundContainer)
        self.mechanicListBox.place(relx=0.020, rely=0.15, relwidth=0.45, relheight=0.80)
        self.mechanicListBox.bind("<Double-Button-1>", self.get_mechanic_specifics)
        self.mechanicListBox.configure(
            background="#ebedeb",
            foreground=self.controller.buttonBackgroundColor,
            relief=self.controller.buttonRelief,
            highlightbackground="#fcc63f",
            highlightcolor="#fcc63f",
            width=500, height=100,
        )

        # Declaration of scrollbar and assign it to the Listbox
        self.scrollbar = Scrollbar(self.mechanicListBox)
        self.mechanicListBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.mechanicListBox.yview)

        self.informationContainer = Frame(self.backgroundContainer)
        self.search_mechanic(None)

    def update_mechanic_list(self):
        """ Updates the listBox with all elements from controller.mechanicList. """
        self.controller.log("MechanicOverviewPage.update_mechanic_list()")
        self.mechanicListBox.delete(0, END)
        for mechanic in self.controller.mechanicList:
            self.mechanicListBox.insert(END, mechanic.name)

    def update_mechanic_information(self):
        """ Button that creates a popup to update the Mechanic object attributes. """
        self.controller.log("MechanicOverviewPage.update_mechanic_information()")
        self.controller.update_fields_information.append(self.selectedMechanic)

        # Create the new popup
        self.controller.new_popup(
            title="Update information",
            message="Please enter the field you which to update and the value it needs to have\n"
                    "Fields can be: \n" + str(self.selectedMechanic)[:-2],
            popup_width=450, popup_height=250, background_color="#fcc63f",
            buttons=[
                {"text": "Update", "command": "self.update_fields"},
                {"text": "Cancel", "command": "self.popup.destroy"}
            ],
            fields=[
                {"text": "Field"},
                {"text": "Value"}
            ]
        )
        try:
            self.get_mechanic_specifics(None, self.selectedMechanic)
            self.update_mechanic_list()
        except tk.TclError:
            # It sometimes spawns an error, catch it and continue running
            return

    def remove_mechanic(self):
        """ Button that removes Mechanic object from the list and database entirely. """
        self.controller.log("MechanicOverviewPage.remove_mechanic()")
        if self.selectedMechanic:
            try:
                # Create a notification about it
                self.controller.new_notification(
                    mechanic=self.selectedMechanic,
                    message="{} was removed".format(
                        self.selectedMechanic.name
                    ), sms=False
                )
                # Run some update functions to update the GUI with this change
                self.selectedMechanic.remove(self.controller.mechanicFile)
                self.controller.mechanicList.remove(self.selectedMechanic)
                self.get_mechanic_specifics(None, None, 0)
                self.update_mechanic_list()
            except ValueError:
                return

    def change_availability(self):
        """ Button that swaps the availability of the Mechanic object, whatever it may be. """
        self.controller.log("MechanicOverviewPage.change_availability()")
        if self.selectedMechanic:
            # From Available to Occupied
            if self.selectedMechanic.availability == "Available":
                self.selectedMechanic.set_attribute("availability", "Occupied", self.controller.mechanicFile)
            # From Occupied to Available
            elif self.selectedMechanic.availability == "Occupied":
                self.selectedMechanic.set_attribute("availability", "Available", self.controller.mechanicFile)

            # Update the informationContainer and create a notification about it
            self.get_mechanic_specifics(None, self.selectedMechanic)
            self.controller.new_notification(
                mechanic=self.selectedMechanic,
                message="Availability for {} changed to {}".format(
                    self.selectedMechanic.name,
                    self.selectedMechanic.availability
                ), sms=False
            )

    def change_shift(self):
        """ Button that swaps the availability of the Mechanic object, whatever it may be. """
        self.controller.log("MechanicOverviewPage.change_shift()")
        if self.selectedMechanic:
            # From day to night
            if self.selectedMechanic.shift == "day":
                self.selectedMechanic.set_attribute("shift", "night", self.controller.mechanicFile)
            # From night to day
            elif self.selectedMechanic.shift == "night":
                self.selectedMechanic.set_attribute("shift", "day", self.controller.mechanicFile)

            # Update the informationContainer and create a notification about it
            self.get_mechanic_specifics(None, self.selectedMechanic)
            self.controller.new_notification(
                mechanic=self.selectedMechanic,
                message="shift for {} changed to {}".format(
                    self.selectedMechanic.name,
                    self.selectedMechanic.shift
                ), sms=False
            )

    def search_mechanic(self, key):
        """
            Function takes searchEntry input and searches corresponding Mechanics with it.
            Can be based on name, region and availability.
        """
        self.controller.log("MechanicOverviewPage.search_mechanic(key={})".format(key))
        if self.searchEntry.get() == "" or not key:
            for mechanic in self.controller.mechanicList:
                self.mechanicListBox.insert(END, mechanic.name)
        else:
            self.mechanicListBox.delete(0, END)
            for mechanic in self.controller.mechanicList:
                # Match to name
                if self.searchEntry.get().lower().strip() in mechanic.name.lower():
                    self.mechanicListBox.insert(END, mechanic.name)
                # Match to region
                elif self.searchEntry.get().lower().strip() in mechanic.region.lower():
                    self.mechanicListBox.insert(END, mechanic.name)
                # Match to availability
                elif self.searchEntry.get().lower().strip() in mechanic.availability.lower():
                    self.mechanicListBox.insert(END, mechanic.name)

    def on_entry_click(self, x):
        """ If searchEntry is clicked and has default text in it, it is removed. """
        self.controller.log("MechanicOverviewPage.on_entry_click()")
        if self.searchEntry.get() == "Search for name, region or availability":
            self.searchEntry.delete(0, END)
            self.searchEntry.insert(0, '')
            self.searchEntry.config(fg='black')

    def get_mechanic_specifics(self, x, passed_mechanic=None, index=None):
        """
            Finds the Mechanic object associated with x and displays it to the informationContainer.
            If a mechanic or index is passed this will be shown instead.
        """
        self.controller.log(
            "MechanicOverviewPage.get_mechanic_specifics(x={}, passed_mechanic={}, index={})"
            "".format(x, passed_mechanic, index)
        )

        # Find the Mechanic object
        mechanic_info = []
        mechanic = None
        if x and index is None and passed_mechanic is None:
            mechanic_input = x.widget.get(x.widget.curselection()[0])
            for found_mechanic in self.controller.mechanicList:
                if found_mechanic.name.lower() == mechanic_input.lower():
                    mechanic = found_mechanic
        elif passed_mechanic is not None:
            mechanic = passed_mechanic
        elif index is not None:
            mechanic = self.controller.mechanicList[index]

        # Align Mechanic data with header information to display later in the loop
        try:
            mechanic_info.append(mechanic.name)
            mechanic_info.append(mechanic.region.title())
            mechanic_info.append(mechanic.age)
            mechanic_info.append(mechanic.phone_number)
            mechanic_info.append(mechanic.availability)
            mechanic_info.append(mechanic.shift)
        except AttributeError:
            self.get_mechanic_specifics(x, passed_mechanic, index)

        self.selectedMechanic = mechanic
        self.informationContainer.place(relx=0.520, rely=0.15, relwidth=0.45, relheight=0.80)
        self.informationContainer.configure(background="#ebedeb")

        # Place the information Headers
        rely = 0
        for label in self.informationHeaders:
            self.tempLabel = Label(self.informationContainer)
            self.tempLabel.place(relx=0, rely=rely, relwidth=1, relheight=0.15)
            self.tempLabel.configure(font="Helvetica 12 bold", text=label, background="#ebedeb")
            rely += 0.5

        # Place the information titles and the information data
        rely = 0.2
        for label in range(len(self.informationLabels)):
            self.tempLabel = Label(self.informationContainer)
            self.tempLabel.place(relx=0.05, rely=rely, relwidth=0.425)
            self.tempLabel.configure(anchor='w', background="#ebedeb", text=self.informationLabels[label])

            self.tempLabel = Label(self.informationContainer)
            self.tempLabel.place(relx=0.5, rely=rely, relwidth=0.455)
            self.tempLabel.configure(anchor='w', background="#ebedeb", text=mechanic_info[label])
            rely += 0.05

        # Place the buttons
        rely = 0.65
        for label in self.actionButtons:
            self.tempLabel = Button(self.informationContainer)
            self.tempLabel.place(relx=0.05, rely=rely, relwidth=0.9)
            self.tempLabel.configure(
                background=self.controller.buttonBackgroundColor,
                foreground=self.controller.buttonForegroundColor,
                relief=self.controller.buttonRelief,
                text=label['text'],
                command=eval(label['command'])
            )
            rely += 0.07
