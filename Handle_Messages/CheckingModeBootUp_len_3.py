import pickle
import pandas as pd

class HandleMessage3:

    def BootupCheckingMode(Picked_DFS, Checking_Reference_List, Checking_Status_List):

        No_Refs_Today_Msg = [[1], [2]]
        No_Refs_Today_Msg = pickle.dumps(No_Refs_Today_Msg, protocol=2)

        if isinstance(Picked_DFS, pd.DataFrame) is False:
            print('No Checks Yet')
            return No_Refs_Today_Msg
        else:
            print("Received Checking Mode Bootup Message, Responding With Checks.")
            Ready_to_send_Check_refs = [['First'], ['I did this']]
            Ready_to_send_Check_refs.append(Checking_Reference_List)
            Ready_to_send_Check_refs.append(Checking_Status_List)
            msg = pickle.dumps(Ready_to_send_Check_refs, protocol=2)
            return msg