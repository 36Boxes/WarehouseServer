import pandas as pd

class PutAwayListFunctions:
    
    
    def Gen_PutAways(Receipted_DFS, database):
        if isinstance(Receipted_DFS, pd.DataFrame) is False:
            pass
        else:
            PutAway_Groupby_Refs = Receipted_DFS.groupby('reference')
            Shipment_Status_List = database["Shipment_Status_List"]
            for count, ref in enumerate(database["Shipment_Reference_List"]):
                try:
                    reference_chunk = PutAway_Groupby_Refs.get_group(ref)
                    if 'Yes E' in reference_chunk.status.values:
                        Shipment_Status_List[count] = 'Receipted W Error'
                    else:
                        Shipment_Status_List[count] = 'Receipted'
                except KeyError:
                    pass
            Put_away_ref_list = dict(PutAway_Groupby_Refs.apply(list))
            current_PARL = database["PutAway_Reference_List"]
            for ref in Put_away_ref_list:
                if ref in database["PutAway_Reference_List"]:
                    pass
                else:
                    current_PARL.append(ref)

            database["PutAway_Reference_List"] = current_PARL

            if len(database["PutAway_Status_List"]) == len(database["PutAway_Reference_List"]):
                pass
            else:
                difference = len(database["PutAway_Reference_List"]) - len(
                    database["PutAway_Status_List"])
                Current_PASL = database["PutAway_Status_List"]
                Addtition_to_Status = ['Not Put Away'] * difference
                Current_PASL += Addtition_to_Status
                database["PutAway_Status_List"] = Current_PASL
            if len(database["Individual_PutAway_Status"]) == len(
                    database["PutAway_Reference_List"]):
                pass
            else:
                active_list = database["PutAway_Reference_List"]
                end = len(active_list)
                start = len(database["Individual_PutAway_Status"])
                for num in range(start, end):
                    ref = active_list[num]
                    ref_group = PutAway_Groupby_Refs.get_group(ref)
                    amount_of_items = len(ref_group)
                    addition_to_Errors = [None] * amount_of_items
                    addition_to_Users = [''] * amount_of_items
                    addition_to_Status = ['No'] * amount_of_items
                    addition_to_Location = ['Not Placed'] * amount_of_items

                for count, statuses in enumerate(database["Individual_PutAway_Status"]):
                    checker = 0
                    for num, status in enumerate(statuses):
                        if status == 'Put-Away':
                            checker += 1
                            if checker == len(status):
                                PASL = database["PutAway_Status_List"]
                                PASL[count] = 'Put-Away'
                                database["PutAway_Status_List"] = PASL