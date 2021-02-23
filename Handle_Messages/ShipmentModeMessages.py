import pickle


class ShipmentModeMessages:

    def Bootup_Shipment_Mode(self, Shipment_Reference_List, Shipment_Status_List, Shipment_Arrival_List):
        print("Received Shipment Mode Bootup Message, Responding With Shipment Lists.")
        Preset_Message = [[1], [2], [3], [4], [5], [6], [7]]
        Addition_to_Message = [[Shipment_Reference_List], [Shipment_Status_List], [Shipment_Arrival_List]]
        Preset_Message.append(Addition_to_Message)
        Total_Message = pickle.dumps(Preset_Message, protocol=2)
        return Total_Message