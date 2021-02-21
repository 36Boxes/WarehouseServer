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
        Todays_Date = datetime.date.today() - timedelta(737)
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

            create_entire_picking_list(Todays_List=Todays_List, Picking_Groupby_Refs=Picking_Groupby_Refs)

            # We wanna create the data for the checking today also

            if isinstance(Picked_DFS, pd.DataFrame):

                Checking_Groupby_Refs = Picked_DFS.groupby('reference')

                for count, ref in enumerate(reference_list_data["Picking_Reference_List"]):
                    try:
                        reference_group = Checking_Groupby_Refs.get_group(ref)
                        if 'Yes E' in reference_group.picked.values:
                            picking_statusList = reference_list_data["Picking_Status_List"]
                            picking_statusList[count] = "Complete Error"
                        else:
                            picking_statusList = reference_list_data["Picking_Status_List"]
                            picking_statusList[count] = "Complete"
                    except KeyError as e:
                        pass

                    Checking_Groupby_Dates = Picked_DFS.groupby()


def create_entire_picking_list(Todays_List, Picking_Groupby_Refs):
    list_Of_References = dict(Todays_List.groupby(['reference']).apply(list))

    temporary_Reflist = []
    temporary_statusList = reference_list_data["Picking_Status_List"]

    for reference in list_Of_References:
        temporary_Reflist.append(reference)

    # Since the ref list is longer than what we already have saved we know a new ref has appeared

    if len(temporary_Reflist) > len(reference_list_data["Picking_Reference_List"]):

        # Churn out a list of picking statuses that is the same length as the reference list

        for num in range(len(reference_list_data["Picking_Reference_List"]) - 1, len(temporary_Reflist) - 1):
            temporary_statusList.append('Not Picked')

        # Set the picking reference list in the dictionary

        reference_list_data["Picking_Reference_List"] = temporary_Reflist

    # Since our ref list is longer than the status list we need to add to our status list to make it equal

    if len(temporary_statusList) < len(reference_list_data["Picking_Reference_List"]):
        new_status_list = reference_list_data["Picking_Status_List"]

        # Add not picked for each ref that was missed

        for num in range(len(temporary_statusList), len(reference_list_data["Picking_Reference_List"])):
            new_status_list.append('Not Picked')

        reference_list_data["Picking_Status_List"] = new_status_list

    if len(temporary_statusList) == len(reference_list_data["Picking_Reference_List"]):
        reference_list_data["Picking_Status_List"] = temporary_statusList

    # Now we need to create the individual logs for each item within the reference

    Individual_Picking_Status, Individual_Picking_Users, Individual_Picking_Errors = create_Individual_Picking_Lists(
        Picking_Groupby_Refs)

    reference_list_data["Individual_Picking_Status"] = Individual_Picking_Status
    reference_list_data["Individual_Picking_Errors"] = Individual_Picking_Errors
    reference_list_data["Individual_Picking_Users"] = Individual_Picking_Users



def create_Individual_Picking_Lists(Picking_Groupby_Refs):
    for count, ref in enumerate(reference_list_data["Picking_Reference_List"]):
        reference_chunk = Picking_Groupby_Refs.get_group(ref)
        amount_of_items = len(reference_chunk)
        updated_pickStatus = reference_list_data["Individual_Picking_Status"]
        updated_pickUser = reference_list_data["Individual_Picking_Users"]
        updated_pickErrors = reference_list_data["Individual_Picking_Errors"]
        try:
            potential_status_line = updated_pickStatus[count]
            if amount_of_items > len(potential_status_line):
                difference = amount_of_items - len(potential_status_line)
                Addition_to_status = difference * ['No']
                Addition_to_user = difference * ['']
                Addition_to_errors = difference * [None]
                updated_pickStatus[count] += Addition_to_status
                updated_pickUser[count] += Addition_to_user
                updated_pickErrors[count] += Addition_to_errors

            continue
        except IndexError:
            pass
        Individual_Status_Line = amount_of_items * ['No']
        Individual_User_Line = amount_of_items * ['']
        Individual_Error_Line = amount_of_items * [None]
        updated_pickStatus.append(Individual_Status_Line)
        updated_pickUser.append(Individual_User_Line)
        updated_pickErrors.append(Individual_Error_Line)

    return updated_pickStatus, updated_pickUser, updated_pickErrors



if __name__ == '__main__':
    refreshit = Thread(target=refresh_files())
    refreshit.start()
    main()
    refreshit.join()