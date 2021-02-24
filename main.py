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
from Handle_Messages.OtherMessages import OtherMiscMessages
from Handle_Messages.PickingModeMessages import PickingModeMessages
from Handle_Messages.CheckingModeMessages import CheckingModeMessages
from Handle_Messages.ShipmentModeMessages import ShipmentModeMessages
from Handle_Messages.PutAwayModeMessages import PutAwayModeMessages


path_To_Database = "/Users/joshmanik/PycharmProjects/Panda Server/TWOPAKTESTFILE.xlsx"

Start_Date = datetime.date.today() - timedelta(740)

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

global Pallet_Tag_Number
Pallet_Tag_Number = 0

PutAway_DFS = None
Receipted_DFS = None
Picked_DFS = None

# Here we have our actual server side code,
# how it works is it identifies the length of the message and uses that length
# to specify which message it then should return


class Echo(Protocol):

    def dataReceived(self, data):
        """
            As soon as any data is received, handle the message and write it back.
            """
        response = self.handle_message(data)
        self.transport.write(response)

    def handle_message(self, msg):

        global Picked_Checked_DFS


        try:
            msg = msg.decode('utf-8')
        except UnicodeDecodeError as e:
            msg = pickle.loads(msg)
        try:

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
            try:
                Checking_Groupby_Refs = Picked_DFS.groupby('reference')
                PutAway_Groupby_Refs = PutAwayListFunctions.PutAway_Groupby_Refs
            except AttributeError:
                pass


            # We decipher which message we want to send by checking
            # the length of the message received

            if len(msg) == 1:
                return OtherMiscMessages().Updater_Message(
                    msg=msg,
                    Picking_Reference_List=Picking_Reference_List,
                    Picking_Status_List=Picking_Status_List,
                    Checking_Reference_List=Checking_Reference_List,
                    Checking_Status_List=Checking_Status_List,
                    Shipment_Reference_List=Shipment_Reference_List,
                    Shipment_Status_List=Shipment_Status_List,
                    Shipment_Arrival_List=Shipment_Arrival_List,
                    PutAway_Reference_List=PutAway_Reference_List,
                    PutAway_Status_List=PutAway_Status_List,
                    Todays_Date=Start_Date
                )

            if len(msg) == 2:
                return PickingModeMessages().BootupPickingMode(
                    Picking_Reference_List=Picking_Reference_List,
                    Picking_Status_List=Picking_Status_List,
                    Authorisation_List=Authorisation_List,
                    Start_Date=Start_Date
                )

            if len(msg) == 3:
                return CheckingModeMessages().BootupCheckingMode(
                    Picked_DFS=Picked_DFS,
                    Checking_Reference_List=Checking_Reference_List,
                    Checking_Status_List=Checking_Status_List
                )

            if len(msg) == 4:
                return ShipmentModeMessages().Bootup_Shipment_Mode(
                    Shipment_Reference_List=Shipment_Reference_List,
                    Shipment_Arrival_List=Shipment_Arrival_List,
                    Shipment_Status_List=Shipment_Status_List
                )

            if len(msg) == 5:
                return PutAwayModeMessages().BootUp_PutAwayMode(
                    PutAway_Reference_List=PutAway_Reference_List,
                    PutAway_Status_List=PutAway_Status_List
                )

            if len(msg) == 6:
                return PickingModeMessages().PickingModeRefresh(
                    Authorisation_List=Authorisation_List,
                    Picking_Status_List=Picking_Status_List,
                    Picking_Reference_List=Picking_Reference_List
                )

            if len(msg) == 7:
                return PickingModeMessages().PickingModeViewDetailedReference(
                    msg=msg,
                    Picking_Groupby_Refs=Picking_Groupby_Refs,
                    Picking_Reference_List=Picking_Reference_List,
                    Individual_Picking_Status=Individual_Picking_Status
                )

            if len(msg) == 8:
                return PickingModeMessages().See_Individual_Picks(
                    msg=msg,
                    Todays_Date=Start_Date,
                    Picking_Reference_List=Picking_Reference_List,
                    Picking_Groupby_Dates=Picking_Groupby_Dates,
                    Individual_Picking_Status=Individual_Picking_Status
                )

            if len(msg) == 9:
                return PickingModeMessages().Quick_MarkAs_Picked(
                    msg=msg,
                    Picked_DFS=Picked_DFS,
                    Picking_Reference_List=Picking_Reference_List,
                    Picking_Status_List=Picking_Status_List,
                    Individual_Picking_Status=Individual_Picking_Status,
                    Individual_Picking_Users=Individual_Picking_Users
                )

            if len(msg) == 10:
                return PickingModeMessages().MarkItemAsPicked(
                    msg=msg,
                    Picked_DFS=Picked_DFS,
                    Picking_Reference_List=Picking_Reference_List,
                    Picking_Status_List=Picking_Status_List,
                    Individual_Picking_Status=Individual_Picking_Status,
                    Individual_Picking_Errors=Individual_Picking_Errors,
                    Individual_Picking_Users=Individual_Picking_Users
                )

            if len(msg) == 11:
                return PickingModeMessages().MarkListAsPicked(
                    msg=msg,
                    Picked_DFS=Picked_DFS,
                    Picking_Status_List=Picking_Status_List,
                    Picking_Groupby_Refs=Picking_Groupby_Refs,
                    Checking_Groupby_Refs=Checking_Groupby_Refs,
                    Individual_Picking_Users=Individual_Picking_Users,
                    Individual_Picking_Errors=Individual_Picking_Errors,
                    Individual_Picking_Status=Individual_Picking_Status
                )

            if len(msg) == 12:
                return CheckingModeMessages().CheckingModeViewDetailedReference(
                    msg=msg,
                    Picked_DFS=Picked_DFS,
                    Picking_Reference_List=Picking_Reference_List,
                    Checking_Reference_List=Checking_Reference_List,
                    Individual_Picking_Users=Individual_Picking_Users,
                    Individual_Checking_Status=Individual_Checking_Status,
                )

            if len(msg) == 13:
                return CheckingModeMessages().SendEmailToOffice(
                    Picked_Checked_DFS=Picked_Checked_DFS
                )

            if len(msg) == 14:
                return CheckingModeMessages().CheckingModeViewIndividualItem(
                    msg=msg,
                    Checking_Groupby_Refs=Checking_Groupby_Refs,
                    Checking_Reference_List=Checking_Reference_List,
                    Picking_Reference_List=Picking_Reference_List,
                    Individual_Picking_Errors=Individual_Picking_Errors,
                    Individual_Picking_Users=Individual_Picking_Users
                )

            if len(msg) == 15:
                return CheckingModeMessages().QuickMarkAsChecked(
                    msg=msg,
                    Checking_Status_List=Checking_Status_List,
                    Individual_Checking_Status=Individual_Checking_Status,
                    Individual_Checking_Users=Individual_Checking_Users
                )

            if len(msg) == 16:
                return CheckingModeMessages().Mark_Item_As_Checked(
                    msg=msg,
                    Checking_Groupby_Refs=Checking_Groupby_Refs,
                    Checking_Reference_List=Checking_Reference_List,
                    Checking_Status_List=Checking_Status_List,
                    Individual_Checking_Errors=Individual_Checking_Errors,
                    Individual_Checking_Users=Individual_Checking_Users,
                    Individual_Checking_Status=Individual_Checking_Status
                )

            if len(msg) == 17:
                return CheckingModeMessages().LogError(
                    msg=msg,
                    Checking_Reference_List=Checking_Reference_List,
                    Checking_Groupby_Refs=Checking_Groupby_Refs,
                    Individual_Checking_Errors=Individual_Checking_Errors,
                    Individual_Checking_Users=Individual_Checking_Users,
                    Individual_Checking_Status=Individual_Checking_Status,
                    Checking_Status_List=Checking_Status_List
                )

            if len(msg) == 18:
                return ShipmentModeMessages().QuickMarkAsArrived(
                    msg=msg,
                    Shipment_Status_List=Shipment_Status_List
                )

            if len(msg) == 19:
                return ShipmentModeMessages().QuickMarkAsNotArrived(
                    msg=msg,
                    Shipment_Status_List=Shipment_Status_List
                )

            if len(msg) == 20:
                ShipmentModeMessages().ViewDetailedShipmentList(
                    msg=msg,
                    Shipment_Reference_List=Shipment_Reference_List,
                    Individual_Shipment_Status=Individual_Shipment_Status,
                    Shipment_Groupby_Refs=Shipment_Groupby_Refs,
                    Individual_Shipment_Carton_Placed=Individual_Shipment_Carton_Placed
                )

            if len(msg) == 21:
                ShipmentModeMessages().QuickMarkAsReceipted(
                    msg=msg,
                    Shipment_Status_List=PutAway_Groupby_Refs,
                    Individual_Shipment_Status=Individual_Shipment_Status,
                    PutAway_Groupby_Refs=PutAway_Groupby_Refs,
                )

            if len(msg) == 22:
                ShipmentModeMessages().QuickUnMarkAsReceipted(
                    msg=msg,
                    Shipment_Status_List=Shipment_Status_List,
                    Shipment_Reference_List=Shipment_Reference_List,
                    Individual_Shipment_Status=Individual_Shipment_Status,
                    PutAway_Groupby_Refs=PutAway_Groupby_Refs
                )

            if len(msg) == 23:
                ShipmentModeMessages().ViewIndividualShipmentItem(
                    msg=msg,
                    Shipment_Reference_List=Shipment_Reference_List,
                    Individual_Shipment_Carton_Placed=Individual_Shipment_Carton_Placed,
                    Individual_Shipment_Status=Individual_Shipment_Status,
                    Shipment_Groupby_Refs=Shipment_Groupby_Refs,
                    Individual_Shipment_Pallet_Amount=Individual_Shipment_Pallet_Amount
                )

            if len(msg) == 24:
                ShipmentModeMessages().AddBoxesToVirtualPallet(
                    msg=msg,
                    Individual_Shipment_Carton_Placed=Individual_Shipment_Carton_Placed,
                    Shipment_Status_List=Shipment_Status_List,
                    Individual_Shipment_Status=Individual_Shipment_Status
                )

            if len(msg) == 25:
                ShipmentModeMessages().RemoveBoxesFromVirtualPallet(
                    msg=msg,
                    Individual_Shipment_Carton_Placed=Individual_Shipment_Carton_Placed,
                    Shipment_Status_List=Shipment_Status_List,
                    Individual_Shipment_Status=Individual_Shipment_Status
                )

            if len(msg) == 26:
                ShipmentModeMessages().MarkItemGroupAsReceipted(
                    msg=msg,
                    Individual_Shipment_Status=Individual_Shipment_Status,
                    Shipment_Status_List=Shipment_Status_List,
                    PutAway_Groupby_Refs=PutAway_Groupby_Refs,
                    Individual_Shipment_Carton_Placed=Individual_Shipment_Carton_Placed,
                    Individual_Shipment_Users=Individual_Shipment_Users,
                    Shipment_Reference_List=Shipment_Reference_List
                )

            if len(msg) == 27:
                ShipmentModeMessages().SendItemListGroupToPutAwayDataFrame(
                    msg=msg,
                    Receipted_DFS=Receipted_DFS,
                    Individual_Shipment_Carton_Placed=Individual_Shipment_Carton_Placed,
                    PutAway_Groupby_Refs=PutAway_Groupby_Refs,
                    Individual_Shipment_Users=Individual_Shipment_Users,
                    Shipment_Arrival_List=Shipment_Arrival_List,
                    Individual_Shipment_Errors=Individual_Shipment_Errors,
                    Individual_Shipment_Status=Individual_Shipment_Status,
                    Shipment_Status_List=Shipment_Status_List,
                    Shipment_Groupby_Refs=Shipment_Groupby_Refs,
                    Shipment_Reference_List=Shipment_Reference_List
                )

            if len(msg) == 28:
                ShipmentModeMessages().PalletTagGenerator(
                    Pallet_Tag_Number=Pallet_Tag_Number
                )

            if len(msg) == 29:
                ShipmentModeMessages().LogVirtualPallet(
                    msg=msg,
                    PutAway_Pallet_Counter=PutAway_Pallet_Counter,
                    Individual_Shipment_Carton_Placed=Individual_Shipment_Carton_Placed,
                    Individual_Shipment_Pallet_Amount=Individual_Shipment_Pallet_Amount
                )

            if len(msg) == 30:
                ShipmentModeMessages().SendErrorMessageToOffice(
                    msg=msg,
                    Shipment_Groupby_Refs=Shipment_Groupby_Refs,
                    Shipment_Reference_List=Shipment_Reference_List
                )

            if len(msg) == 31:
                PutAwayModeMessages().ViewDetailedPutAwayList(
                    msg=msg,
                    Individual_Shipment_Pallet_Amount=Individual_Shipment_Pallet_Amount,
                    Individual_PutAway_Status=Individual_PutAway_Status,
                    PutAway_Groupby_Refs=PutAway_Groupby_Refs,
                    PutAway_Pallet_Counter=PutAway_Pallet_Counter,
                    PutAway_Reference_List=PutAway_Reference_List,
                    Shipment_Reference_List=Shipment_Reference_List
                )

            if len(msg) == 32:
                PutAwayModeMessages().ViewDetailedIndividualItem(
                    msg=msg,
                    PutAway_Reference_List=PutAway_Reference_List,
                    Shipment_Reference_List=Shipment_Reference_List,
                    Individual_Shipment_Pallet_Amount=Individual_Shipment_Pallet_Amount,
                    PutAway_Groupby_Refs=PutAway_Groupby_Refs,
                    Individual_PutAway_Status=Individual_PutAway_Status,
                    Individual_PutAway_Users=Individual_PutAway_Users,
                    Individual_PutAway_Errors=Individual_PutAway_Errors,
                    Individual_PutAway_Location=Individual_PutAway_Location
                )

            if len(msg) == 33:
                PutAwayModeMessages().MarkLocationPlaced(
                    msg=msg,
                    Individual_PutAway_Status=Individual_PutAway_Status,
                    Individual_Shipment_Pallet_Amount=Individual_Shipment_Pallet_Amount,
                    PutAway_Pallet_Counter=PutAway_Pallet_Counter,
                    PutAway_Reference_List=PutAway_Reference_List,
                    PutAway_Status_List=PutAway_Status_List,
                    Shipment_Reference_List=Shipment_Reference_List
                )

            if len(msg) == 34:
                PutAwayModeMessages().MarkPutAwayGroupAsPutAway(
                    msg=msg,
                    Individual_PutAway_Status=Individual_PutAway_Status,
                    Individual_Shipment_Pallet_Amount=Individual_Shipment_Pallet_Amount,
                    PutAway_Reference_List=PutAway_Reference_List,
                    PutAway_Status_List=PutAway_Status_List,
                    Shipment_Reference_List=Shipment_Reference_List
                )

            if len(msg) == 35:
                PutAwayModeMessages().SendPutAwayToOffice(
                    msg=msg,
                    Individual_PutAway_Status=Individual_PutAway_Status,
                    Individual_Shipment_Pallet_Amount=Individual_Shipment_Pallet_Amount,
                    PutAway_DFS=PutAway_DFS,
                    PutAway_Groupby_Refs=PutAway_Groupby_Refs,
                    PutAway_Pallet_Counter=PutAway_Pallet_Counter,
                    PutAway_Reference_List=PutAway_Reference_List,
                    Shipment_Reference_List=Shipment_Reference_List,
                    Shipment_Arrival_List=Shipment_Arrival_List,
                    Shipment_Status_List=Shipment_Status_List
                )

            print("responded: {}\n".format(msg))
            return msg.encode('utf-8')
        except ValueError as e:
            print(e)
            print(msg)
            print('Im Outside The Try Function, message must not be accounted for!')


def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(8000, f)
    reactor.run()


def RefreshFiles():
    while True:
        global Start_Date
        global Picking_Groupby_Refs
        global Picking_Groupby_Dates
        global Shipment_Groupby_Refs
        # 2019-02-15
        # Start_Date = Check_to_see_if_day_has_changed(Start_Date)

        xlsx = pd.ExcelFile(path_To_Database)
        df = pd.read_excel(xlsx, sheet_name='Sheet1')

        # We group the data by two factors the date and the reference number

        Picking_Groupby_Dates = df.groupby('documentDate')
        Picking_Groupby_Refs = df.groupby('reference')

        xlsx = pd.ExcelFile(path_To_Database)
        df = pd.read_excel(xlsx, sheet_name='Sheet2')

        # Do the same for the shipment sheet

        Shipment_Groupby_Dates = df.groupby('arrivalDate')
        Shipment_Groupby_Refs = df.groupby('reference')

        try:
            Pallet_Tag_Number = ShipmentModeMessages.Pallet_Tag_Number
        except AttributeError:
            pass

        try:
            Todays_List = Picking_Groupby_Dates.get_group(Start_Date)
            References_Available = True
        except KeyError:

            # We know if a key error is called no references are in the database for today's date

            References_Available = False
            print("No References Available at the moment!")

        if References_Available is True:

            # We wanna create the data for todays Picking References so we call that function

            Picklist_Functions().GenPicks(Todays_List=Todays_List,
                                          database=database,
                                          Picking_Groupby_Refs=Picking_Groupby_Refs)

            # We wanna check to see if we can create the data for the checking today also

            ChecklistFunctions().GenChecklist(Picked_DFS=Picked_DFS,
                                              database=database)

            # We wanna create the data for the Shipment lists too

            ShipmentListFunctions().Gen_ShipLists(database=database,
                                                  path_To_Database=path_To_Database)

            # We want to lastly now check to see if we can create the put away data

            PutAwayListFunctions().Gen_PutAways(Receipted_DFS=Receipted_DFS,
                                                database=database)


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
    refreshit = Thread(target=RefreshFiles)
    refreshit.start()
    main()
    refreshit.join()
