from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import pandas as pd
import datetime
from datetime import timedelta
import pickle
from threading import Thread
import sentry_sdk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from PicklistGen import Picklist_Functions
from ChecklistGen import ChecklistFunctions
from ShipmentGen import ShipmentListFunctions

path_To_Database = "/Users/joshmanik/PycharmProjects/Panda Server/TWOPAKTESTFILE.xlsx"

# Dictonary that holds all our ordered lists

reference_list_data = {


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


global Receipted_DFS
global PutAway_DFS
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




    def decode_message(self, msg):

        try:
            msg = msg.decode('utf-8')
        except UnicodeDecodeError as e:
            msg = pickle.loads(msg)

        return msg




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

        if References_Available == True:

            # We wanna create the data for todays Picking References so we call that function

            Picklist_Functions.GenPicks(Todays_List=Todays_List, reference_list_data=reference_list_data, Picking_Groupby_Refs=Picking_Groupby_Refs)

            # We wanna create the data for the checking today also

            ChecklistFunctions.create_entire_check_list(Picked_DFS=Picked_DFS, reference_list_data=reference_list_data)

            # We wanna create the data for the Shipment lists too

            ShipmentListFunctions.Gen_ShipLists(reference_list_data=reference_list_data, path_To_Database=path_To_Database)

            print(reference_list_data)


if __name__ == '__main__':
    refreshit = Thread(target=refresh_files())
    refreshit.start()
    main()
    refreshit.join()