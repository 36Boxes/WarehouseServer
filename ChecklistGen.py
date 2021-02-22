
import pandas as pd

class ChecklistFunctions:

    def create_entire_check_list(Picked_DFS, reference_list_data):
        DF_Created = True
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

                Checking_Groupby_Dates = Picked_DFS.groupby("documentDate")
                listOfCheckingRefs = dict(Checking_Groupby_Refs.apply(list))
                updatedCheckList = reference_list_data["Checking_Reference_List"]
                for ref in listOfCheckingRefs:

                    if ref in updatedCheckList:
                        # We pass as this ref is already handled as its in our list
                        pass
                    else:
                        updatedCheckList.append(ref)

                reference_list_data["Checking_Reference_List"] = updatedCheckList

                if len(reference_list_data["Checking_Status_List"]) == len(
                        reference_list_data["Checking_Reference_List"]):
                    pass
                else:
                    difference = len(reference_list_data["Checking_Reference_List"]) - len(
                        reference_list_data["Checking_Status_List"])
                    additionToStatus = ['Not Checked'] * difference
                    updatedCheckStatusList = reference_list_data["Checking_Status_List"]
                    updatedCheckStatusList += additionToStatus
        else:
            DF_Created = False

        if DF_Created is True:
            if len(reference_list_data["Individual_Checking_Status"]) == len(
                    reference_list_data["Checking_Reference_List"]):
                pass
            else:
                end = len(reference_list_data["Checking_Reference_List"])
                start = len(reference_list_data["Individual_Checking_Status"])
                updatedICheckUser = reference_list_data["Individual_Checking_Users"]
                updatedICheckError = reference_list_data["Individual_Checking_Errors"]
                updatedICheckStatus = reference_list_data["Individual_Checking_Status"]
                for num in range(start, end):
                    checkList = reference_list_data["Checking_Reference_List"]
                    ref_in_question = checkList[num]
                    checking_ref_group = Checking_Groupby_Refs.get_group(ref_in_question)
                    amount_of_items = len(checking_ref_group)
                    AdditionTo_Individual_Checking_Users = [''] * amount_of_items
                    AdditionTo_Individual_Checking_Status = ['No'] * amount_of_items
                    AdditionTo_Individual_Checking_Errors = [None] * amount_of_items
                    updatedICheckUser.append(AdditionTo_Individual_Checking_Users)
                    updatedICheckError.append(AdditionTo_Individual_Checking_Errors)
                    updatedICheckStatus.append(AdditionTo_Individual_Checking_Status)

                reference_list_data["Individual_Checking_Status"] = updatedICheckStatus
                reference_list_data["Individual_Checking_Errors"] = updatedICheckError
                reference_list_data["Individual_Checking_Users"] = updatedICheckUser