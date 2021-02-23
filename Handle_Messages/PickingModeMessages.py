import pickle


class PickingModeMessages:

    def BootupPickingMode(self,Picking_Reference_List, Picking_Status_List, Authorisation_List, Start_Date):

        No_Refs_Today_Msg = [[1], [2]]
        No_Refs_Today_Msg = pickle.dumps(No_Refs_Today_Msg, protocol=2)

        if Picking_Reference_List == []:
            print("No Refs Yet")
            return No_Refs_Today_Msg
        Date_To_Search = Start_Date.strftime("%d-%m-%Y")
        Ready_to_send_refs = [[Date_To_Search]]
        Ready_to_send_refs.append(Picking_Reference_List)
        Ready_to_send_refs.append(Picking_Status_List)
        Ready_to_send_refs.append(Authorisation_List)
        Ready_to_send_refs.append([1])
        Ready_to_send_refs.append([1])
        msg = pickle.dumps(Ready_to_send_refs, protocol=2)
        print("Received Picking Mode Bootup Message, Responding With Refs.")
        return msg