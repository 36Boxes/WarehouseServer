import pickle


class PutAwayModeMessages:

    def BootUp_PutAwayMode(self, PutAway_Reference_List, PutAway_Status_List):
        print("Received Put-Away Mode Bootup Message, Responding With Put-Away Lists.")
        Message_i_wanna_send = ['pizza', 'tablets', 'grapes', PutAway_Reference_List, PutAway_Status_List]
        Message_i_wanna_send = pickle.dumps(Message_i_wanna_send, protocol=2)
        return Message_i_wanna_send