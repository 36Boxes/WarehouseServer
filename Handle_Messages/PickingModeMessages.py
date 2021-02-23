import pickle
import pandas as pd
import datetime

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

    def PickingModeRefresh(self, Authorisation_List, Picking_Reference_List, Picking_Status_List):
        print("Received Picking Mode Refresh Message, Responding With Picking Lists.")
        readied_message = [['Big']]
        readied_message.append(Authorisation_List)
        readied_message.append(Picking_Reference_List)
        readied_message.append(Picking_Status_List)
        msg = pickle.dumps(readied_message, protocol=2)
        return msg

    def PickingModeViewDetailedReference(self, msg, Picking_Reference_List, Picking_Groupby_Refs, Individual_Picking_Status):

        No_Refs_Today_Msg = [[1],[2]]
        No_Refs_Today_Msg = pickle.dumps(No_Refs_Today_Msg, protocol=2)

        print("Received Picking Mode more detailed message, Responding With Filtered Lists.")
        ref_Index_number = msg[6]
        ref_Index_number = ref_Index_number[0]

        if int(ref_Index_number) > len(Picking_Reference_List):
            print('Ref index Is Higher Than The Ref Count')
            return No_Refs_Today_Msg
        if int(ref_Index_number) == len(Picking_Reference_List):
            print('Ref index Is Higher Than The Ref Count')
            return No_Refs_Today_Msg


        ref = Picking_Reference_List[int(ref_Index_number)]

        Chopped_DF = Picking_Groupby_Refs.get_group(ref)
        sorted_df = Chopped_DF.sort_values('name2')

        end = len(Chopped_DF)
        locations = []
        product_codes = []

        # This is a function that sorts the locations by levels to allow the first levels to be shown first

        Preset_Message = [['6'], ['RINGS'], ['AND'], ['COUNTING']]

        for num in range(0, end):
            ROW = sorted_df.iloc[[num]]
            code = ROW['code'].values
            location = ROW['name2'].values
            productCode = (",".join(code))
            location = (",".join(location))
            product_codes.append(productCode)
            locations.append(location)


        new_codes = []
        new_locations = []
        for count, location in enumerate(locations):
            try:
                numba = int(location[-1:])
            except ValueError as e:
                print('I just Caught Your Problem')
                print('this list has locations without numbers on the end')
                numba = 0
            if numba == 1:
                code_in_question = product_codes[count]
                new_codes.append(code_in_question)
                new_locations.append(location)

        filtered_codes = []
        filtered_locs = []
        for i in new_locations:
            filtered_locs.append(i)
        for n in new_codes:
            filtered_codes.append(n)
        for count, lo in enumerate(locations):
            if lo in new_locations:
                pass
            else:
                filtered_locs.append(lo)
                filtered_codes.append(product_codes[count])

        pick_status = Individual_Picking_Status[int(ref_Index_number)]
        Preset_Message.append(filtered_locs)
        Preset_Message.append(filtered_codes)
        Preset_Message.append(pick_status)
        Total_Message = pickle.dumps(Preset_Message, protocol=2)
        return Total_Message

    def See_Individual_Picks(self, msg, Individual_Picking_Status, Picking_Reference_List, Picking_Groupby_Dates, Todays_Date):
        print("Received Picking Mode See Individual Picks Message, Responding With Filtered Lists.")
        chops = msg[6]
        chops = chops[0]
        chips = msg[7]
        chips = chips[0]
        ref = Picking_Reference_List[int(chops)]
        chopped = Picking_Groupby_Dates.get_group(Todays_Date)
        chopped = chopped.groupby('reference')
        chopped = chopped.get_group(ref)
        sorted_df = chopped.sort_values('name2')
        end = len(sorted_df)
        codes = []
        locs = []
        desc = []
        qoc = []
        qop = []
        name = []
        quans = []
        name3 = []
        Readied_database = []
        for row in range(0, end):
            RR = sorted_df.iloc[[row]]
            code = RR['code'].values
            code = (",".join(code))
            locat = RR['name2'].values
            locat = (",".join(locat))
            des = RR['description'].values
            des = (",".join(des))
            carton = RR['name3'].values
            cartons = (",".join(carton))
            inbox = RR['name'].values
            box_amount = (",".join(inbox))
            quantity = RR['quantity'].values
            ASCII = ord(cartons[0])
            ASCIII = ord(box_amount[0])
            if ASCII == 82:
                cartons = str(cartons)
                carton = cartons[1:]
            elif ASCII == 67:
                cartons = str(cartons)
                carton = cartons[2:]
            elif ASCII == 80:
                cartons = str(cartons)
                carton = cartons[1:]
            elif ASCII == 69:
                carton = cartons
                carton = 1
            if ASCIII == 82:
                box_amount = str(box_amount)
                inbox = box_amount[1:]
            elif ASCIII == 67:
                box_amount = str(box_amount)
                inbox = box_amount[2:]
            elif ASCIII == 80:
                box_amount = str(box_amount)
                inbox = box_amount[1:]
            elif ASCIII == 69:
                inbox = box_amount
                inbox = 1
            inbox = float(quantity) * int(inbox)
            carton = int(inbox) / int(carton)
            quantity = 1 * float(quantity)
            codes.append(code)
            locs.append(locat)
            desc.append(des)
            qoc.append(carton)
            qop.append(inbox)
            name.append(box_amount)
            name3.append(cartons)
            quans.append(quantity)
        new_codes = []
        new_locs = []
        new_desc = []
        new_qoc = []
        new_qop = []
        for count, loc in enumerate(locs):
            try:
                numba = int(loc[-1:])
            except ValueError as e:
                print('No Locs end in numbers')
                numba = 0
            if numba == 1:
                code_in_question = codes[count]
                desc_in_question = desc[count]
                qoc_in_question = qoc[count]
                qop_in_question = qop[count]
                new_codes.append(code_in_question)
                new_locs.append(loc)
                new_desc.append(desc_in_question)
                new_qoc.append(qoc_in_question)
                new_qop.append(qop_in_question)
            if numba == 0:
                pick_stats = Individual_Picking_Status[int(chops)]
                Readied_database.append(locs)
                Readied_database.append(desc)
                Readied_database.append(codes)
                Readied_database.append(qop)
                Readied_database.append(qoc)
                Readied_database.append(pick_stats)
                ready = pickle.dumps(Readied_database, protocol=2)
                return ready
        filtered_codes = []
        filtered_locs = []
        filtered_desc = []
        filtered_qoc = []
        filtered_qop = []
        for i in new_locs:
            filtered_locs.append(i)
        for n in new_codes:
            filtered_codes.append(n)
        for a in new_desc:
            filtered_desc.append(a)
        for t in new_qoc:
            filtered_qoc.append(t)
        for y in new_qop:
            filtered_qop.append(y)
        for count, lo in enumerate(locs):
            if lo in new_locs:
                pass
            else:
                filtered_qop.append(qop[count])
                filtered_qoc.append(qoc[count])
                filtered_locs.append(lo)
                filtered_codes.append(codes[count])
                filtered_desc.append(desc[count])
        pick_stats = Individual_Picking_Status[int(chops)]
        Readied_database.append(filtered_locs)
        Readied_database.append(filtered_desc)
        Readied_database.append(filtered_codes)
        Readied_database.append(filtered_qop)
        Readied_database.append(filtered_qoc)
        Readied_database.append(pick_stats)
        ready = pickle.dumps(Readied_database, protocol=2)
        return ready

    def Quick_MarkAs_Picked(self, msg, Individual_Picking_Status, Individual_Picking_Users, Picking_Status_List, Picking_Reference_List, Picked_DFS):
        User_right_now = msg[5]
        no_cap = 0
        chopso = msg[7]
        chopso = chopso[0]
        chips = msg[6]
        chips = chips[0]
        payload = msg[8]
        payload = payload[0]
        print("Received Picking Mode Quick Mark As Picked Message, Marking as " + payload + ".")
        picko = Individual_Picking_Status[int(chopso)]
        uso = Individual_Picking_Users[int(chopso)]
        picko[int(chips)] = payload
        uso[int(chips)] = User_right_now
        dap = ['Yes', 'Yes E']
        for i in picko:
            if i in dap:
                if i == 'Yes E':
                    no_cap = 1
                    continue
                continue
            else:
                print("Logged Pick In Server!")
                print('Picklist not done yet')
                Picking_Status_List[int(chopso)] = 'Incomplete'
                one_two = [Picking_Status_List, Individual_Picking_Status[int(chopso)]]
                one_two = pickle.dumps(one_two, protocol=2)
                return one_two
        ref_we_are_on = Picking_Reference_List[int(chopso)]
        conditioner = 0
        try:
            pickgrop = Picked_DFS.groupby('reference')
            tes = pickgrop.get_group(ref_we_are_on)
            print(tes)
            conditioner = 1
        except AttributeError as e:
            print('Pick List Not Sent')
        except KeyError as e:
            print('Pick List Not Sent')
            conditioner = 0
        if conditioner == 0:
            print('Logging into status list')
            Picking_Status_List[int(chopso)] = 'Not Sent!'
            print(Picking_Status_List)
        if conditioner == 1:
            print('Logging into status list')
            Picking_Status_List[int(chopso)] = 'Complete'
            print(Picking_Status_List)
            if no_cap == 1:
                Picking_Status_List[int(chopso)] = 'Complete Error'
        one_two = [Picking_Status_List, Individual_Picking_Status[int(chopso)]]
        one_two = pickle.dumps(one_two, protocol=2)
        return one_two

    def MarkItemAsPicked(self, msg, Picking_Reference_List, Individual_Picking_Status, Picking_Status_List, Picked_DFS, Individual_Picking_Users, Individual_Picking_Errors):
        print("Received Picking Mode Mark As Picked Message, Marking Item As Picked.")
        User_right_now = msg[2]
        User_right_now = User_right_now[0]
        error_message = msg[3]
        error_message = error_message[0]
        cargo = 0
        no_cap = 0
        chops = msg[0]
        chops = chops[0]
        chips = msg[1]
        chips = chips[0]
        picko = Individual_Picking_Status[int(chops)]
        uso = Individual_Picking_Users[int(chops)]
        error_line = Individual_Picking_Errors[int(chops)]
        error_line[int(chips)] = error_message
        if error_message == None:
            picko[int(chips)] = 'Yes'
        else:
            picko[int(chips)] = 'Yes E'
        uso[int(chips)] = User_right_now
        dap = ['Yes', 'Yes E']
        for i in picko:
            if i in dap:
                if i == 'Yes E':
                    no_cap = 1
                    continue
                continue
            else:
                Picking_Status_List[int(chops)] = 'Incomplete'
                sendback = [Individual_Picking_Status[chops], Picking_Status_List, 3, 4, 5, 6, 7, 8, 9]
                sendbac = pickle.dumps(sendback, protocol=2)
                return sendbac

        ref_we_are_on = Picking_Reference_List[int(chops)]
        conditioner = 0

        try:
            pickgrop = Picked_DFS.groupby('reference')
            tes = pickgrop.get_group(ref_we_are_on)
            conditioner = 1
        except AttributeError as e:
            pass
        except KeyError as e:
            pass
            conditioner = 0
        if conditioner == 0:
            Picking_Status_List[int(chops)] = 'Not Sent!'
            sop = [Individual_Picking_Status[chops], Picking_Status_List]
            sop = pickle.dumps(sop, protocol=2)
            return sop
        if conditioner == 1:
            print('Logging into status list')
            Picking_Status_List[int(chops)] = 'Complete'
            sendback = [Individual_Picking_Status[chops], Picking_Status_List, 3, 4, 5, 6, 7, 8, 9, 0]
            sendback = pickle.dumps(sendback, protocol=2)
            return sendback
        if no_cap == 1:
            Picking_Status_List[int(chops)] = 'Complete Error'
            sendback = [Individual_Picking_Status[chops], Picking_Status_List, 3, 4, 5, 6, 7, 8, 9, 0]
            sendback = pickle.dumps(sendback, protocol=2)
            return sendback

    def MarkListAsPicked(self, msg, Picking_Groupby_Refs, Checking_Groupby_Refs, Individual_Picking_Status, Individual_Picking_Users, Individual_Picking_Errors, Picking_Status_List, Picked_DFS):
        print("Received Picking Mode Mark Picklist As Picked Message, Marking as Complete.")
        Confirmation_Email_9 = [[1],[2],[3],[4],[5],[6],[7],[8],[9]]
        Confirmation_Email_9 = pickle.dumps(Confirmation_Email_9, protocol=2)
        qoc = msg[1]
        qop = msg[2]
        qoc = qoc[0]
        qop = qop[0]
        referenc = msg[3]
        padd = ['Yes', 'Yes E']
        ref_check = referenc[0]  # ERROR
        ref_check_df = Picking_Groupby_Refs.get_group(ref_check)
        refsa = referenc * len(qoc)
        try:
            Dont_Be_Slick = Checking_Groupby_Refs.get_group(ref_check)
            print("You're Being Slick")
            msg = [['22'], ['west'], ['rest'], ['pack'], ['repos'], ['pasta'], ['poptarts']]
            msg = pickle.dumps(msg, protocol=2)
            return msg
        except KeyError:
            pass

        except NameError:
            pass
        endoz = len(ref_check_df)
        codes = []
        locs = []
        desc = []

        for zam in range(0, endoz):
            RR = ref_check_df.iloc[[zam]]
            code = RR['code'].values
            code = (",".join(code))
            locat = RR['name2'].values
            locat = (",".join(locat))
            des = RR['description'].values
            des = (",".join(des))
            codes.append(code)
            locs.append(locat)
            desc.append(des)

        chops = msg[4]
        chips = msg[6]
        chaps = chops[0]
        chaips = chips[0]
        picko_mode = Individual_Picking_Status[int(chaps)]
        uso_mode = Individual_Picking_Users[int(chaps)]
        ero_mode = Individual_Picking_Errors[int(chaps)]

        for count, i in enumerate(picko_mode):
            if i in padd:
                continue
            else:
                return Confirmation_Email_9
        dates = [datetime.date.today()] * len(refsa)
        reference = pd.DataFrame({'reference': refsa})
        documentDate = pd.DataFrame({'documentDate': dates})
        code = pd.DataFrame({'code': codes})
        description = pd.DataFrame({'description': desc})
        nam = pd.DataFrame({'QuantityofCartons': qoc})
        name2 = pd.DataFrame({'name2': locs})
        name3 = pd.DataFrame({'QuantityofPieces': qop})
        pickeder = pd.DataFrame({'picked': picko_mode})
        errors = pd.DataFrame({'errors': ero_mode})
        users = pd.DataFrame({'user': uso_mode})
        Picked_DF = (
            pd.concat([reference, documentDate, code, description, nam, name2, name3, pickeder, errors, users], axis=1))
        if len(Picked_DF) == len(ref_check_df):
            pass
        else:
            sendback = [Individual_Picking_Status[chaps], Picking_Status_List, 3, 4, 5, 6, 7, 8, 9, 0]
            sendbac = pickle.dumps(sendback, protocol=2)
            return sendbac
        if isinstance(Picked_DFS, pd.DataFrame) is False:
            Picked_DFS = Picked_DF
            sendback = [Individual_Picking_Status[chaps], Picking_Status_List, 3, 4, 5, 6, 7, 8, 9, 0]
            sendback = pickle.dumps(sendback, protocol=2)
            return sendback
        else:
            condit = 1
            poppies = Picked_DF
            pass
        if condit == 1:
            pass
        else:
            pop_tart = Picked_DFS.groupby('reference')
            poppies = pop_tart.get_group(ref_check)
        if len(poppies) == len(ref_check_df):
            capper = 0
            print(Picked_DFS)
            for i in picko_mode:
                if i == 'Yes':
                    pass
                else:
                    capper += 1
            if capper == 1:
                Picking_Status_List[chaps] = 'Complete Error'
            if capper == 0:
                Picking_Status_List[chaps] = 'Complete'
            Picked_DFS = pd.concat([Picked_DFS, Picked_DF])
            sendback = [Individual_Picking_Status[chaps], Picking_Status_List, 3, 4, 5, 6, 7, 8, 9, 0]
            sendback = pickle.dumps(sendback, protocol=2)
            return sendback
        if len(poppies) > len(ref_check_df):
            diff = len(poppies) - len(ref_check_df)
            poppies = poppies.reset_index(drop=True)
            endo = (len(ref_check_df) + diff)
            endomii = int(endo) - int(1)
            poppies.drop([len(ref_check_df), endomii])
            Picked_DFS = pd.concat([Picked_DFS, poppies])
        print(Picked_DFS)
        capper = 0
        for i in picko_mode:
            if i == 'Yes':
                pass
            else:
                capper += 1
        if capper == 1:
            Picking_Status_List[chaps] = 'Complete Error'
        if capper == 0:
            Picking_Status_List[chaps] = 'Complete'
        sendback = [Individual_Picking_Status[chaps], Picking_Status_List, 3, 4, 5, 6, 7, 8, 9, 0]
        sendback = pickle.dumps(sendback, protocol=2)
        return sendback