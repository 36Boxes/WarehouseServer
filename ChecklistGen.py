import pandas as pd


class ChecklistFunctions:

    def create_entire_check_list(Picked_DFS, database):
        DF_Created = True
        if isinstance(Picked_DFS, pd.DataFrame):

            Checking_Groupby_Refs = Picked_DFS.groupby('reference')

            for count, ref in enumerate(database["Picking_Reference_List"]):
                try:
                    reference_group = Checking_Groupby_Refs.get_group(ref)
                    if 'Yes E' in reference_group.picked.values:
                        picking_statusList = database["Picking_Status_List"]
                        picking_statusList[count] = "Complete Error"
                    else:
                        picking_statusList = database["Picking_Status_List"]
                        picking_statusList[count] = "Complete"
                except KeyError as e:
                    pass

                Checking_Groupby_Dates = Picked_DFS.groupby("documentDate")
                listOfCheckingRefs = dict(Checking_Groupby_Refs.apply(list))
                updatedCheckList = database["Checking_Reference_List"]
                for ref in listOfCheckingRefs:

                    if ref in updatedCheckList:
                        # We pass as this ref is already handled as its in our list
                        pass
                    else:
                        updatedCheckList.append(ref)

                database["Checking_Reference_List"] = updatedCheckList

                if len(database["Checking_Status_List"]) == len(
                        database["Checking_Reference_List"]):
                    pass
                else:
                    difference = len(database["Checking_Reference_List"]) - len(
                        database["Checking_Status_List"])
                    additionToStatus = ['Not Checked'] * difference
                    updatedCheckStatusList = database["Checking_Status_List"]
                    updatedCheckStatusList += additionToStatus
        else:
            DF_Created = False

        if DF_Created is True:
            if len(database["Individual_Checking_Status"]) == len(
                    database["Checking_Reference_List"]):
                pass
            else:
                end = len(database["Checking_Reference_List"])
                start = len(database["Individual_Checking_Status"])
                updatedICheckUser = database["Individual_Checking_Users"]
                updatedICheckError = database["Individual_Checking_Errors"]
                updatedICheckStatus = database["Individual_Checking_Status"]
                for num in range(start, end):
                    checkList = database["Checking_Reference_List"]
                    ref_in_question = checkList[num]
                    checking_ref_group = Checking_Groupby_Refs.get_group(ref_in_question)
                    amount_of_items = len(checking_ref_group)
                    AdditionTo_Individual_Checking_Users = [''] * amount_of_items
                    AdditionTo_Individual_Checking_Status = ['No'] * amount_of_items
                    AdditionTo_Individual_Checking_Errors = [None] * amount_of_items
                    updatedICheckUser.append(AdditionTo_Individual_Checking_Users)
                    updatedICheckError.append(AdditionTo_Individual_Checking_Errors)
                    updatedICheckStatus.append(AdditionTo_Individual_Checking_Status)

                database["Individual_Checking_Status"] = updatedICheckStatus
                database["Individual_Checking_Errors"] = updatedICheckError
                database["Individual_Checking_Users"] = updatedICheckUser