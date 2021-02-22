

class Picklist_Functions:


    def GenPicks(self, Todays_List, reference_list_data, Picking_Groupby_Refs):
        list_Of_References = dict(Todays_List.groupby(['reference']).apply(list))

        temporary_Reflist = []
        temporary_statusList = reference_list_data["Picking_Status_List"]

        for reference in list_Of_References:
            temporary_Reflist.append(reference)

        # Since the ref list is longer than what we already have saved we know a new ref has appeared

        if len(temporary_Reflist) > len(reference_list_data["Picking_Reference_List"]):

            # Churn out a list of picking statuses that is the same length as the reference list

            for num in range(len(reference_list_data["Picking_Reference_List"]) - 1, len(temporary_Reflist) - 1):
                temporary_statusList.append('Not Picked')

            # Set the picking reference list in the dictionary

            reference_list_data["Picking_Reference_List"] = temporary_Reflist

        # Since our ref list is longer than the status list we need to add to our status list to make it equal

        if len(temporary_statusList) < len(reference_list_data["Picking_Reference_List"]):
            new_status_list = reference_list_data["Picking_Status_List"]

            # Add not picked for each ref that was missed

            for num in range(len(temporary_statusList), len(reference_list_data["Picking_Reference_List"])):
                new_status_list.append('Not Picked')

            reference_list_data["Picking_Status_List"] = new_status_list

        if len(temporary_statusList) == len(reference_list_data["Picking_Reference_List"]):
            reference_list_data["Picking_Status_List"] = temporary_statusList

        # Now we need to create the individual logs for each item within the reference

        Individual_Picking_Status, Individual_Picking_Users, Individual_Picking_Errors = self.create_Individual_Picking_Lists(
            Picking_Groupby_Refs=Picking_Groupby_Refs, reference_list_data=reference_list_data)

        reference_list_data["Individual_Picking_Status"] = Individual_Picking_Status
        reference_list_data["Individual_Picking_Errors"] = Individual_Picking_Errors
        reference_list_data["Individual_Picking_Users"] = Individual_Picking_Users

    def create_Individual_Picking_Lists(self,Picking_Groupby_Refs, reference_list_data):
        for count, ref in enumerate(reference_list_data["Picking_Reference_List"]):
            reference_chunk = Picking_Groupby_Refs.get_group(ref)
            amount_of_items = len(reference_chunk)
            updated_pickStatus = reference_list_data["Individual_Picking_Status"]
            updated_pickUser = reference_list_data["Individual_Picking_Users"]
            updated_pickErrors = reference_list_data["Individual_Picking_Errors"]
            try:
                potential_status_line = updated_pickStatus[count]
                if amount_of_items > len(potential_status_line):
                    difference = amount_of_items - len(potential_status_line)
                    Addition_to_status = difference * ['No']
                    Addition_to_user = difference * ['']
                    Addition_to_errors = difference * [None]
                    updated_pickStatus[count] += Addition_to_status
                    updated_pickUser[count] += Addition_to_user
                    updated_pickErrors[count] += Addition_to_errors

                continue
            except IndexError:
                pass
            Individual_Status_Line = amount_of_items * ['No']
            Individual_User_Line = amount_of_items * ['']
            Individual_Error_Line = amount_of_items * [None]
            updated_pickStatus.append(Individual_Status_Line)
            updated_pickUser.append(Individual_User_Line)
            updated_pickErrors.append(Individual_Error_Line)

        return updated_pickStatus, updated_pickUser, updated_pickErrors
