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

            xlsx = pd.ExcelFile(path_To_Database)
            df = pd.read_excel(xlsx, sheet_name='Sheet2')
            Shipment_Groupby_Dates = df.groupby('arrivalDate')
            Shipment_Groupby_Refs = df.groupby('reference')
            list_of_shipment_refs = dict(df.groupby(['reference']).apply(list))


            temporary_ship_list = []
            for ref in list_of_shipment_refs:
                temporary_ship_list.append(ref)


            if len(temporary_ship_list) == len(reference_list_data["Shipment_Reference_List"]):
                pass
            else:
                if len(temporary_ship_list) > len(reference_list_data["Shipment_Reference_List"]):
                    current_status_list = reference_list_data["Shipment_Status_List"]
                    for num in range(len(reference_list_data["Shipment_Reference_List"]), len(temporary_ship_list) - 1):
                        current_status_list.append('Not Arrived')

                    reference_list_data["Shipment_Reference_List"] = temporary_ship_list

            currentShipList = reference_list_data["Shipment_Reference_List"]
            currentshipArrrival = reference_list_data["Shipment_Arrival_List"]
            currentShip_status = reference_list_data["Shipment_Status_List"]
            currentship_I_Status = reference_list_data["Individual_Shipment_Status"]
            currentship_I_errors = reference_list_data["Individual_Shipment_Errors"]
            currentship_I_users = reference_list_data["Individual_Shipment_Users"]
            currentship_I_cartons_placed = reference_list_data["Individual_Shipment_Carton_Placed"]
            for count, ref in enumerate(temporary_ship_list):
                if ref == currentShipList[count]:
                    pass
                else:
                    del currentShipList[count]
                    del currentShip_status[count]
                    del currentshipArrrival[count]
                    del currentship_I_Status[count]
                    del currentship_I_errors[count]
                    del currentship_I_users[count]
                    del currentship_I_cartons_placed[count]


            reference_list_data["Shipment_Reference_List"] = currentShipList
            reference_list_data["Shipment_Arrival_List"] = currentshipArrrival
            reference_list_data["Individual_Shipment_Status"] = currentship_I_Status
            reference_list_data["Individual_Shipment_Errors"] = currentship_I_errors
            reference_list_data["Individual_Shipment_Users"] = currentship_I_users
            reference_list_data["Individual_Shipment_Carton_Placed"] = currentship_I_cartons_placed
            reference_list_data["Shipment_Status_List"] = currentShip_status

            if len(currentShipList) > len(currentShip_status):
                for num in range(len(currentShip_status), len(currentShipList)):
                    currentShip_status.append('Not Arrived')

                reference_list_data["Shipment_Status_List"] = currentShip_status


            for count , ref in enumerate(reference_list_data["Shipment_Reference_List"]):
                Individual_Shipment_Status = reference_list_data["Individual_Shipment_Status"]
                Individual_Shipment_Users = reference_list_data["Individual_Shipment_Users"]
                try:
                    Potential_Status_Line = Individual_Shipment_Status[count]
                    Potential_User_Line = Individual_Shipment_Users[count]
                    continue
                except IndexError:
                    pass

                Shipment_Chunk = Shipment_Groupby_Refs.get_group(ref)
                length_of_chunk = len(Shipment_Chunk)
                for number in range(0, 1):
                    Row = Shipment_Chunk.iloc[[number]]
                    data_needed = Row['arrivalDate'].values
                    data_needed = str(data_needed)

                    # This is to format the date so it looks nice when we send to the UI of the client

                    Trunacted_date = data_needed.index('T')
                    a, b = data_needed[:Trunacted_date], data_needed[Trunacted_date + 3:]
                    date_of_shipment_arrival = a[2:]


                Individual_Status_Line = length_of_chunk * ['No']
                Individual_User_Line = length_of_chunk * ['']
                Individual_Error_Line = length_of_chunk * [None]
                Individual_Shipment_Carton_Place = length_of_chunk * [0.00]
                Individual_Shipment_Pallet_Amounts = length_of_chunk * [[1, 0.00, 0000, None, '', '']]
                PutAway_Pallet_Counters = length_of_chunk * [0]

                SAL = reference_list_data["Shipment_Arrival_List"]
                ISSL = reference_list_data["Individual_Shipment_Status"]
                ISUL = reference_list_data["Individual_Shipment_Users"]
                ISEL = reference_list_data["Individual_Shipment_Errors"]
                ISCPL = reference_list_data["Individual_Shipment_Carton_Placed"]
                ISPAL = reference_list_data["Individual_Shipment_Pallet_Amount"]
                PAPCL = reference_list_data["PutAway_Pallet_Counter"]

                SAL.append(date_of_shipment_arrival)
                ISSL.append(Individual_Status_Line)
                ISUL.append(Individual_User_Line)
                ISEL.append(Individual_Error_Line)
                ISCPL.append(Individual_Shipment_Carton_Place)
                ISPAL.append(Individual_Shipment_Pallet_Amounts)
                PAPCL.append(PutAway_Pallet_Counters)

                reference_list_data["Individual_Shipment_Status"] = ISSL
                reference_list_data["Individual_Shipment_Users"] = ISUL
                reference_list_data["Individual_Shipment_Errors"] = ISEL
                reference_list_data["Individual_Shipment_Carton_Placed"] = ISCPL
                reference_list_data["Individual_Shipment_Pallet_Amount"] = ISPAL
                reference_list_data["PutAway_Pallet_Counter"] = PAPCL
                reference_list_data["Shipment_Arrival_List"] = SAL

                for count, box in enumerate(ISCPL):
                    FIRST_COUNT = count
                    for count, Cartons_on_pallet in enumerate(box):
                        if Cartons_on_pallet > 0:
                            Carry_It_Home = 0
                            Individual_Shipment_Status = reference_list_data["Individual_Shipment_Status"]
                            Statuses = Individual_Shipment_Status[FIRST_COUNT]
                            if Statuses[count] == 'Receipted':
                                Carry_It_Home = 1

                            if Carry_It_Home == 0:
                                Statuses[count] = 'In Progress'
                                Shipment_Status_List = reference_list_data["Shipment_Status_List"]
                                Shipment_Status_List[FIRST_COUNT] = 'In Progress'

                reference_list_data["Individual_Shipment_Status"] = Individual_Shipment_Status
        print(reference_list_data)
        print(reference_list_data["Shipment_Reference_List"])
        print(reference_list_data["Shipment_Status_List"])
        print(reference_list_data["Shipment_Arrival_List"])
        print(reference_list_data["Individual_Shipment_Status"])
        print(reference_list_data["Individual_Shipment_Errors"])
        print(reference_list_data["Individual_Shipment_Users"])
        print(reference_list_data["Individual_Shipment_Carton_Placed"])
        print(reference_list_data["Individual_Shipment_Pallet_Amount"])


if __name__ == '__main__':
    refreshit = Thread(target=refresh_files())
    refreshit.start()
    main()
    refreshit.join()