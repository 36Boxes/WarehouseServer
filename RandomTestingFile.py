from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import pandas as pd
import datetime
from datetime import timedelta
import pickle
from threading import Thread
from Refresh_Files.PicklistGen import Picklist_Functions
from Refresh_Files.ChecklistGen import ChecklistFunctions
from Refresh_Files.ShipmentGen import ShipmentListFunctions
from Refresh_Files.PutAwayListGen import PutAwayListFunctions
from Handle_Messages.OtherMessages import HandleMessage1
from Handle_Messages.PickingModeMessages import HandleMessage2
from Handle_Messages.CheckingModeMessages import HandleMessage3
from Handle_Messages.ShipmentModeMessages import HandleMessage4

path_To_Database = "/Users/joshmanik/PycharmProjects/Panda Server/TWOPAKTESTFILE.xlsx"

Start_Date = datetime.date.today() -  timedelta(739)

# Dictionary that holds all our ordered lists

database = {


    "Picking_Reference_List" : [],
    "Picking_Status_List" : [],
    "Individual_Picking_Errors": [],
    "Individual_Picking_Status" : [],
    "Individual_Picking_Users" : [],


    "Checking_Reference_List" : [],
    "Checking_Status_List" : [],
    "Individual_Checking_Errors" : [],
    "Individual_Checking_Status" : [],
    "Individual_Checking_Users" : [],


    "Shipment_Reference_List" : [],
    "Shipment_Status_List" : [],
    "Shipment_Arrival_List" : [],
    "Individual_Shipment_Errors" : [],
    "Individual_Shipment_Status" : [],
    "Individual_Shipment_Users" : [],
    "Individual_Shipment_Carton_Placed" : [],
    "Individual_Shipment_Pallet_Amount" : [],


    "PutAway_Reference_List" : [],
    "PutAway_Status_List" : [],
    "Individual_PutAway_Errors" : [],
    "Individual_PutAway_Status" : [],
    "Individual_PutAway_Users" : [],
    "Individual_PutAway_Location" : [],
    "PutAway_Pallet_Counter" : [],

}



PutAway_DFS = None
Receipted_DFS = None
Picked_DFS = None

# Here we have our actual server side code,
# how it works is it identifies the length of the message and uses that length
# to specify which message it then should return

class Echo(Protocol):


    def data_received(self, data):
        """
            As soon as any data is received, handle the message and write it back.
            """
        print("got")
        response = self.handle_Message(data)
        self.transport.write(response)

    def handle_message(self, msg):
        try:
            msg = msg.decode('utf-8')
        except UnicodeDecodeError as e:
            msg = pickle.loads(msg)

        # We define our lists here to save us typing them out hundreds of times

        Picking_Reference_List = database["Picking_Reference_List"]
        Picking_Status_List = database["Picking_Status_List"]

        # This was a feature that was never implemented so ive just taken out the data
        # However the app still needs to send an authorisation list so it still has to be an object
        Authorisation_List = ['']


        Individual_Picking_Errors = database["Individual_Picking_Errors"]
        Individual_Picking_Status = database["Individual_Picking_Status"]
        Individual_Picking_Users = database["Individual_Picking_Users"]
        Checking_Reference_List = database["Checking_Reference_List"]
        Checking_Status_List = database["Checking_Status_List"]
        Individual_Checking_Errors = database["Individual_Checking_Errors"]
        Individual_Checking_Status = database["Individual_Checking_Status"]
        Individual_Checking_Users = database["Individual_Checking_Users"]
        Shipment_Reference_List = database["Shipment_Reference_List"]
        Shipment_Status_List = database["Shipment_Status_List"]
        Shipment_Arrival_List = database["Shipment_Arrival_List"]
        Individual_Shipment_Errors = database["Individual_Shipment_Errors"]
        Individual_Shipment_Status = database["Individual_Shipment_Status"]
        Individual_Shipment_Users = database["Individual_Shipment_Users"]
        Individual_Shipment_Carton_Placed = database["Individual_Shipment_Carton_Placed"]
        Individual_Shipment_Pallet_Amount = database["Individual_Shipment_Pallet_Amount"]
        PutAway_Reference_List = database["PutAway_Reference_List"]
        PutAway_Status_List = database["PutAway_Status_List"]
        Individual_PutAway_Errors = database["Individual_PutAway_Errors"]
        Individual_PutAway_Status = database["Individual_PutAway_Status"]
        Individual_PutAway_Users = database["Individual_PutAway_Users"]
        Individual_PutAway_Location = database["Individual_PutAway_Location"]
        PutAway_Pallet_Counter = database["PutAway_Pallet_Counter"]


        if len(msg) == 1:
            return HandleMessage1.Message_One(
                msg=msg,
                Picking_Reference_List= Picking_Reference_List,
                Picking_Status_List= Picking_Status_List,
                Checking_Reference_List = Checking_Reference_List,
                Checking_Status_List= Checking_Status_List,
                Shipment_Reference_List= Shipment_Reference_List,
                Shipment_Status_List= Shipment_Status_List,
                Shipment_Arrival_List= Shipment_Arrival_List,
                PutAway_Reference_List= PutAway_Reference_List,
                PutAway_Status_List= PutAway_Status_List,
                Todays_Date=Start_Date
            )

        if len(msg) == 2:
            return HandleMessage2.BootupPickingMode(
                Picking_Reference_List= Picking_Reference_List,
                Picking_Status_List= Picking_Status_List,
                Authorisation_List= Authorisation_List,
                Start_Date= Start_Date
            )

        if len(msg) == 3:
            return HandleMessage3.BootupCheckingMode(
                Picked_DFS = Picked_DFS,
                Checking_Reference_List = Checking_Reference_List,
                Checking_Status_List = Checking_Status_List
            )



def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(8000, f)
    reactor.run()


def refresh_files():
    while True:
        global Start_Date
        # 2019-02-15
        # Start_Date = Check_to_see_if_day_has_changed(Start_Date)

        xlsx = pd.ExcelFile(path_To_Database)
        df = pd.read_excel(xlsx, sheet_name='Sheet1')

        # We group the data by two factors the date and the reference number

        Picking_Groupby_Dates = df.groupby('documentDate')
        Picking_Groupby_Refs = df.groupby('reference')
        try:
            Todays_List = Picking_Groupby_Dates.get_group(Start_Date)
            References_Available = True
        except KeyError:

            # We know if a key error is called no references are in the database for today's date

            References_Available = False
            print("No References Available at the moment!")

        if References_Available is True:

            # We wanna create the data for todays Picking References so we call that function

            Picklist_Functions.GenPicks(Todays_List=Todays_List, database=database, Picking_Groupby_Refs=Picking_Groupby_Refs)

            # We wanna check to see if we can create the data for the checking today also

            ChecklistFunctions.create_entire_check_list(Picked_DFS=Picked_DFS, database=database)

            # We wanna create the data for the Shipment lists too

            ShipmentListFunctions.Gen_ShipLists(database=database, path_To_Database=path_To_Database)

            # We want to lastly now check to see if we can create the put away data

            PutAwayListFunctions.Gen_PutAways(Receipted_DFS=Receipted_DFS, database=database)


def Check_to_see_if_day_has_changed(Start_Date):
    date_to_check = datetime.date.today()
    strStartDate = str(Start_Date)
    strCheckDate = str(date_to_check)
    if strStartDate == strCheckDate:
        pass

    else:
        Start_Date = date_to_check

    return Start_Date

if __name__ == '__main__':
    refreshit = Thread(target=refresh_files())
    refreshit.start()
    main()
    refreshit.join()
