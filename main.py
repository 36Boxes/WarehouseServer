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

path_To_Database = "/Users/joshmanik/PycharmProjects/Panda Server/TWOPAKTESTFILE.xlsx"

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

class Twisted_Echo_Server(Protocol):


    def data_received(self, data):
        # As soon as data is received handle the message
        # to gain the response and send it right back
        response = self.handle_Message(data)
        self.transport.write(response)

    def handle_message(self, msg):
        msg = self.decode_message(msg=msg)

        # We define our lists here to save us typing them out hundreds of times

        Picking_Reference_List = database["Picking_Reference_List"]
        Picking_Status_List = database["Picking_Status_List"]
        Individual_Picking_Errors = database["Individual_Picking_Errors"]
        Individual_Picking_Status = database["Individual_Picking_Status"]
        Individual_Picking_Users = database["Individual_Picking_Users"]


        if len(msg) == 1:






    def decode_message(self, msg):
        try:
            msg = msg.decode('utf-8')
        except UnicodeDecodeError as e:
            msg = pickle.loads(msg)

        return msg

    def Handle_message_length_One(self, database, msg):
        msg = ", ".join(msg)
        if msg == 'Update':
            if database["Picking_Reference_List"] == []:
                Tickback = [[1]]
                Tickback = pickle.dumps(Tickback, protocol=2)
                return Tickback
            Date_To_Search = DATE_MON.strftime("%d-%m-%Y")
            Tickback = [
                Date_To_Search, , Picking_Status_List, Authorisation_List,
                Checking_Status_List, Checking_Reference_List, Shipment_Status_List, Shipment_Reference_List,
                Shipment_Arrival_List, PutAway_Reference_List, PutAway_Status_List

            ]
            Tickback = pickle.dumps(Tickback, protocol=2)
            return Tickback

        Tickback = [[1]]
        Tickback = pickle.dumps(Tickback, protocol=2)
        return Tickback




def main():
    f = Factory()
    f.protocol = Twisted_Echo_Server
    reactor.listenTCP(8000, f)
    reactor.run()





def job():
    global DATE_MON
    date_to_check = datetime.date.today()
    stringed_date_mon = str(DATE_MON)
    stringed_checkdate = str(date_to_check)
    if stringed_date_mon == stringed_checkdate:
        pass

    else:
        DATE_MON = date_to_check


def refresh_files():
    while True:
        global Todays_Date
        Todays_Date = datetime.date.today() - timedelta(738)
        # 2019-02-15
        xlsx = pd.ExcelFile(path_To_Database)
        df = pd.read_excel(xlsx, sheet_name='Sheet1')

        # We group the data by two factors the date and the reference number

        Picking_Groupby_Dates = df.groupby('documentDate')
        Picking_Groupby_Refs = df.groupby('reference')
        try:
            Todays_List = Picking_Groupby_Dates.get_group(Todays_Date)
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


if __name__ == '__main__':
    refreshit = Thread(target=refresh_files())
    refreshit.start()
    main()
    refreshit.join()
