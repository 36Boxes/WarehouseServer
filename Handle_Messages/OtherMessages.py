import pickle


class OtherMiscMessages:

    def Updater_Message(self, msg, Picking_Reference_List,Picking_Status_List, Checking_Status_List,
                    Checking_Reference_List, Shipment_Status_List, Shipment_Reference_List, Shipment_Arrival_List,
                    PutAway_Reference_List, PutAway_Status_List, Todays_Date):
        msg = ", ".join(msg)
        if msg == 'Update':
            if Picking_Reference_List == []:
                Tickback = [[1]]
                Tickback = pickle.dumps(Tickback, protocol=2)
                return Tickback
            Date_To_Search = Todays_Date.strftime("%d-%m-%Y")
            Tickback = [
                Date_To_Search, Picking_Reference_List, Picking_Status_List, [''],
                Checking_Status_List, Checking_Reference_List, Shipment_Status_List, Shipment_Reference_List,
                Shipment_Arrival_List, PutAway_Reference_List, PutAway_Status_List

            ]
            Tickback = pickle.dumps(Tickback, protocol=2)
            return Tickback

        Tickback = [[1]]
        Tickback = pickle.dumps(Tickback, protocol=2)
        return Tickback