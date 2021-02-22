import pandas as pd



class ShipmentListFunctions:

    def Gen_ShipLists(database, path_To_Database):

        xlsx = pd.ExcelFile(path_To_Database)
        df = pd.read_excel(xlsx, sheet_name='Sheet2')
        Shipment_Groupby_Dates = df.groupby('arrivalDate')
        Shipment_Groupby_Refs = df.groupby('reference')
        list_of_shipment_refs = dict(df.groupby(['reference']).apply(list))

        temporary_ship_list = []
        for ref in list_of_shipment_refs:
            temporary_ship_list.append(ref)

        if len(temporary_ship_list) == len(database["Shipment_Reference_List"]):
            pass
        else:
            if len(temporary_ship_list) > len(database["Shipment_Reference_List"]):
                current_status_list = database["Shipment_Status_List"]
                for num in range(len(database["Shipment_Reference_List"]), len(temporary_ship_list) - 1):
                    current_status_list.append('Not Arrived')

                database["Shipment_Reference_List"] = temporary_ship_list

        currentShipList = database["Shipment_Reference_List"]
        currentshipArrrival = database["Shipment_Arrival_List"]
        currentShip_status = database["Shipment_Status_List"]
        currentship_I_Status = database["Individual_Shipment_Status"]
        currentship_I_errors = database["Individual_Shipment_Errors"]
        currentship_I_users = database["Individual_Shipment_Users"]
        currentship_I_cartons_placed = database["Individual_Shipment_Carton_Placed"]
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

        database["Shipment_Reference_List"] = currentShipList
        database["Shipment_Arrival_List"] = currentshipArrrival
        database["Individual_Shipment_Status"] = currentship_I_Status
        database["Individual_Shipment_Errors"] = currentship_I_errors
        database["Individual_Shipment_Users"] = currentship_I_users
        database["Individual_Shipment_Carton_Placed"] = currentship_I_cartons_placed
        database["Shipment_Status_List"] = currentShip_status

        if len(currentShipList) > len(currentShip_status):
            for num in range(len(currentShip_status), len(currentShipList)):
                currentShip_status.append('Not Arrived')

            database["Shipment_Status_List"] = currentShip_status

        for count, ref in enumerate(database["Shipment_Reference_List"]):
            Individual_Shipment_Status = database["Individual_Shipment_Status"]
            Individual_Shipment_Users = database["Individual_Shipment_Users"]
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

            SAL = database["Shipment_Arrival_List"]
            ISSL = database["Individual_Shipment_Status"]
            ISUL = database["Individual_Shipment_Users"]
            ISEL = database["Individual_Shipment_Errors"]
            ISCPL = database["Individual_Shipment_Carton_Placed"]
            ISPAL = database["Individual_Shipment_Pallet_Amount"]
            PAPCL = database["PutAway_Pallet_Counter"]

            SAL.append(date_of_shipment_arrival)
            ISSL.append(Individual_Status_Line)
            ISUL.append(Individual_User_Line)
            ISEL.append(Individual_Error_Line)
            ISCPL.append(Individual_Shipment_Carton_Place)
            ISPAL.append(Individual_Shipment_Pallet_Amounts)
            PAPCL.append(PutAway_Pallet_Counters)

            database["Individual_Shipment_Status"] = ISSL
            database["Individual_Shipment_Users"] = ISUL
            database["Individual_Shipment_Errors"] = ISEL
            database["Individual_Shipment_Carton_Placed"] = ISCPL
            database["Individual_Shipment_Pallet_Amount"] = ISPAL
            database["PutAway_Pallet_Counter"] = PAPCL
            database["Shipment_Arrival_List"] = SAL

            for count, box in enumerate(ISCPL):
                FIRST_COUNT = count
                for count, Cartons_on_pallet in enumerate(box):
                    if Cartons_on_pallet > 0:
                        Carry_It_Home = 0
                        Individual_Shipment_Status = database["Individual_Shipment_Status"]
                        Statuses = Individual_Shipment_Status[FIRST_COUNT]
                        if Statuses[count] == 'Receipted':
                            Carry_It_Home = 1

                        if Carry_It_Home == 0:
                            Statuses[count] = 'In Progress'
                            Shipment_Status_List = database["Shipment_Status_List"]
                            Shipment_Status_List[FIRST_COUNT] = 'In Progress'

            database["Individual_Shipment_Status"] = Individual_Shipment_Status

