"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import functools
import math
import tkinter as tk
from tkinter import *


class CardMachineOverviewPage(tk.Frame):
    """
        This TkInter object holds all information for all CardMachine objects,
        it's also able to display specific information and perform actions on that object.
    """

    def __init__(self, parent, controller):
        """ Object constructor """
        tk.Frame.__init__(self, parent)

        # Initialise variables
        self.controller = controller
        self.searchString = []
        self.tempLabel = None
        self.informationLabels = ["Card Machine Station: ", "Longitude: ", "Latitude: ", "In service: ", "Name: ",
                                  "Direct Distance: ", ""]
        self.informationHeaders = ["General Card Machine Information", "Closest Mechanic"]

        # Declaration Background Frame
        self.backgroundContainer = Frame(self)
        self.backgroundContainer.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.backgroundContainer.configure(background="#fcc63f", height=480, width=1000)

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
        self.searchEntry.insert(0, "Search name, status")
        self.searchEntry.bind('<FocusIn>', self.on_entry_click)
        self.searchEntry.bind("<Key>", self.search_station)

        # Declaration of left Listbox to list all CardMachine objects
        self.stationListBox = Listbox(self.backgroundContainer)
        self.stationListBox.place(relx=0.020, rely=0.15, relwidth=0.45, relheight=0.80)
        self.stationListBox.bind("<Double-Button-1>", self.get_machine_specifics)
        self.stationListBox.configure(
            background="#ebedeb",
            foreground=self.controller.buttonBackgroundColor,
            relief=self.controller.buttonRelief,
            highlightbackground="#fcc63f",
            highlightcolor="#fcc63f",
            width=500, height=100
        )

        # Declaration of scrollbar and assign it to the Listbox
        self.scrollbar = Scrollbar(self.stationListBox)
        self.stationListBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.stationListBox.yview)

        self.informationContainer = Frame(self.backgroundContainer)
        self.search_station(None)

    def search_station(self, key):
        """
            Function takes searchEntry input and searches corresponding stations with it.
            Can be based on name and status.
        """
        self.controller.log("CardMachineOverviewPage.search_station(key={})".format(key))
        if self.searchEntry.get() == "" or not key:
            for station in self.controller.cardMachineList:
                self.stationListBox.insert(END, station.station_name)
        else:
            self.stationListBox.delete(0, END)
            for station in self.controller.cardMachineList:
                # Match to station_name
                if self.searchEntry.get().lower().strip() in station.station_name.lower():
                    self.stationListBox.insert(END, station.station_name)
                # Match to defect
                elif self.searchEntry.get().lower().strip() in station.defect.lower():
                    self.stationListBox.insert(END, station.station_name)

    def on_entry_click(self, x):
        """ If searchEntry is clicked and has default text in it, it is removed. """
        self.controller.log("CardMachineOverviewPage.on_entry_click()")
        if self.searchEntry.get() == 'Search name, status':
            self.searchEntry.delete(0, END)
            self.searchEntry.insert(0, '')
            self.searchEntry.config(fg='black')

    def calculate_distance_time_popup(self, card_machine, mechanic_info):
        """ Creates popup for the Google API data between coordinates of Mechanic and CardMachine. """
        self.controller.log(
            "CardMachineOverviewPage.calculate_distance_time_popup(card_machine={}), mechanic_info={}".format(
                card_machine, mechanic_info))

        # Get the travel advice
        travel_advice = self.controller.get_distance_travel_time(
            latitude1=card_machine.latitude, longitude1=card_machine.longitude,
            latitude2=mechanic_info[1].latitude, longitude2=mechanic_info[1].longitude
        )

        # Create the new popup
        self.controller.new_popup(
            title="Travel information",
            message="Traveling to {} by car will be {} kilometer over {} minutes.".format(
                card_machine.station_name, travel_advice[0], travel_advice[1]
            ),
            popup_width=450, popup_height=100, background_color="#fcc63f",
            buttons=[{"text": "  Done  ", "command": "self.popup.destroy"}], fields=None
        )

    def update_machine_specifics_labels(self, card_machine_info, card_machine, mechanic_info):
        """ This function takes the object input and updates the TkInter objects with its information. """
        self.controller.log(
            "CardMachineOverviewPage.update_machine_specifics_labels("
            "card_machine_info={}, card_machine={}, mechanic_info={})".format(
                card_machine_info, card_machine, mechanic_info)
        )

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
            if label == 4:
                rely += 0.22

            if card_machine_info[label] != "":
                self.tempLabel = Label(self.informationContainer)
                self.tempLabel.place(relx=0.05, rely=rely, relwidth=0.425)
                self.tempLabel.configure(anchor='w', background="#ebedeb", text=self.informationLabels[label])

                self.tempLabel = Label(self.informationContainer)
                self.tempLabel.place(relx=0.5, rely=rely, relwidth=0.455)
                self.tempLabel.configure(anchor='w', background="#ebedeb", text=card_machine_info[label])

            else:
                # Place the buttons and link it to the Mechanic object
                self.tempLabel = Button(self.informationContainer)
                self.tempLabel.place(relx=0.05, rely=rely, relwidth=0.425)
                self.tempLabel.configure(
                    command=functools.partial(self.controller.dispatch_mechanic, card_machine, mechanic_info[1]),
                    background=self.controller.buttonBackgroundColor,
                    foreground=self.controller.buttonForegroundColor,
                    relief=self.controller.buttonRelief,
                    text=" Dispatch Mechanic ",
                    anchor='w'
                )

                self.tempLabel = Button(self.informationContainer)
                self.tempLabel.place(relx=0.5, rely=rely, relwidth=0.425)
                self.tempLabel.configure(
                    command=functools.partial(self.calculate_distance_time_popup, card_machine, mechanic_info),
                    background=self.controller.buttonBackgroundColor,
                    foreground=self.controller.buttonForegroundColor,
                    relief=self.controller.buttonRelief,
                    text=" Calculate Travel Time ",
                    anchor='w'
                )
            rely += 0.05

    def get_machine_specifics(self, x):
        """ Takes element from listBox and formats the data to be parsed to the function that will display it. """
        self.controller.log("CardMachineOverviewPage.get_machine_specifics(x={})".format(x))

        # Get the card machine from the listBOx
        station_input = x.widget.get(x.widget.curselection()[0])
        card_machine = None
        card_machine_info = []

        for machine in self.controller.cardMachineList:
            if machine.station_name.lower() == station_input.lower():
                card_machine = machine

        # Get the closest Mechanic to this CardMachine
        mechanic_info = self.controller.get_closest_mechanic(card_machine, None)

        # Format the CardMachine data in line with the data headers
        card_machine_info.append(card_machine.station_name)
        card_machine_info.append(card_machine.longitude)
        card_machine_info.append(card_machine.latitude)
        card_machine_info.append(card_machine.defect)
        card_machine_info.append(mechanic_info[1].name)
        card_machine_info.append("{} km".format(math.floor(mechanic_info[0])))
        card_machine_info.append("")

        # Update the container object
        self.informationContainer.place(relx=0.520, rely=0.15, relwidth=0.45, relheight=0.80)
        self.informationContainer.configure(background="#ebedeb")
        self.update_machine_specifics_labels(card_machine_info, card_machine, mechanic_info)
