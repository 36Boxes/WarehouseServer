import pickle
import pandas as pd
import smtplib


class ShipmentModeMessages:
    global Pallet_Tag_Number


    def Bootup_Shipment_Mode(self, Shipment_Reference_List, Shipment_Status_List, Shipment_Arrival_List):
        print("Received Shipment Mode Bootup Message, Responding With Shipment Lists.")
        Preset_Message = [[1], [2], [3], [4], [5], [6], [7]]
        Addition_to_Message = [[Shipment_Reference_List], [Shipment_Status_List], [Shipment_Arrival_List]]
        Preset_Message.append(Addition_to_Message)
        Total_Message = pickle.dumps(Preset_Message, protocol=2)
        return Total_Message

    def QuickMarkAsArrived(self, msg, Shipment_Status_List):
        Confirmation_Email = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]
        Confirmation_Email = pickle.dumps(Confirmation_Email, protocol=2)
        Talib = msg[17]
        Talib = Talib[0]
        Shipment_Status_List[int(Talib)] = 'Arrived'
        return Confirmation_Email

    def QuickMarkAsNotArrived(self, msg, Shipment_Status_List):
        Confirmation_Email_9 = [[1],[2],[3],[4],[5],[6],[7],[8],[9]]
        Confirmation_Email_9 = pickle.dumps(Confirmation_Email_9, protocol=2)
        Talib = msg[47]
        Talib = Talib[0]
        Shipment_Status_List[int(Talib)] = 'Not Arrived'
        print(Shipment_Status_List)
        return Confirmation_Email_9

    def ViewDetailedShipmentList(self, msg, Shipment_Reference_List, Individual_Shipment_Status, Shipment_Groupby_Refs,
                                 Individual_Shipment_Carton_Placed):
        Confirmation_Email_11 = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11]]
        Confirmation_Email_11 = pickle.dumps(Confirmation_Email_11, protocol=2)
        Talib = msg[19]
        Talib = Talib[0]
        if int(Talib) >= len(Shipment_Reference_List):
            print('No Item Was Clicked')
            return Confirmation_Email_11
        Shipment_Ref = Shipment_Reference_List[int(Talib)]
        statuses = Individual_Shipment_Status[int(Talib)]
        Ref_in_Questions = Shipment_Groupby_Refs.get_group(Shipment_Ref)
        Accent = Individual_Shipment_Carton_Placed[int(Talib)]
        print(Ref_in_Questions)
        eZdoesIT = len(Ref_in_Questions)
        codes = []
        carts = []
        Metta = []
        world_peace = []
        for row in range(0, eZdoesIT):
            TT = Ref_in_Questions.iloc[[row]]
            Code = TT['code'].values
            Code = (",".join(Code))
            quantity = TT['quantity'].values
            box_amount = TT['name'].values
            cartons = TT['name2'].values
            metta = TT['description'].values
            metta = (','.join(metta))
            cartons = cartons[0]
            box_amount = box_amount[0]
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
            codes.append(Code)
            carts.append(carton)
            Metta.append(metta)
            world_peace.append(inbox)
        maga = [codes, carts, statuses, Accent]
        maga = pickle.dumps(maga, protocol=2)
        return maga


    def QuickMarkAsReceipted(self, msg, Individual_Shipment_Status, PutAway_Groupby_Refs, Shipment_Status_List):

        Confirmation_Email = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]
        Confirmation_Email = pickle.dumps(Confirmation_Email, protocol=2)

        No_Refs_Today_Msg = [[1],[2]]
        No_Refs_Today_Msg = pickle.dumps(No_Refs_Today_Msg, protocol=2)

        Confirmation_Email_9 = [[1],[2],[3],[4],[5],[6],[7],[8],[9]]
        Confirmation_Email_9 = pickle.dumps(Confirmation_Email_9, protocol=2)

        Talib = msg[18]
        Talib = Talib[0]
        mosdef = msg[19]
        mosdef = mosdef[0]
        User = msg[20]
        User = User[0]
        if mosdef >= len(Individual_Shipment_Status[int(Talib)]):
            return No_Refs_Today_Msg
        lineop = Individual_Shipment_Status[int(Talib)]
        lineop[int(mosdef)] = 'Receipted'
        for count, status in enumerate(Individual_Shipment_Status):
            J_M = 0
            Talib = count
            for Police, answer in enumerate(status):
                Toppler = len(status)
                print(status)
                if answer == 'Receipted':
                    J_M += 1
                    if J_M == Toppler:
                        try:
                            people = PutAway_Groupby_Refs.get_group(Shipment_Status_List[Talib])
                            print(people)
                            Shipment_Status_List[Talib] = 'Receipted'
                        except KeyError:
                            Shipment_Status_List[Talib] = 'Not Sent!'
                        except NameError:
                            Shipment_Status_List[Talib] = 'Not Sent!'
                    if J_M > 0:
                        if J_M == Toppler:
                            return Confirmation_Email
                        Shipment_Status_List[Talib] = 'In Progress'
                    if J_M == 0:
                        Shipment_Status_List[Talib] = 'Arrived'
        return Confirmation_Email_9

    def QuickUnMarkAsReceipted(self, msg, Individual_Shipment_Status, Shipment_Reference_List, PutAway_Groupby_Refs, Shipment_Status_List):


        Confirmation_Email = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]
        Confirmation_Email = pickle.dumps(Confirmation_Email, protocol=2)

        No_Refs_Today_Msg = [[1],[2]]
        No_Refs_Today_Msg = pickle.dumps(No_Refs_Today_Msg, protocol=2)

        Talib = msg[19]
        Talib = Talib[0]
        mosdef = msg[20]
        mosdef = mosdef[0]
        User = msg[21]
        User = User[0]
        print(User)
        print(mosdef)
        print(Talib)
        if mosdef >= len(Individual_Shipment_Status[int(Talib)]):
            return No_Refs_Today_Msg
        lineop = Individual_Shipment_Status[int(Talib)]
        lineop[int(mosdef)] = 'No'
        for count, status in enumerate(Individual_Shipment_Status):
            J_M = 0
            Talib = count
            for Police, answer in enumerate(status):
                Toppler = len(status)
                if answer == 'Receipted':
                    J_M += 1
                    if J_M == Toppler:
                        try:
                            people = PutAway_Groupby_Refs.get_group(Shipment_Reference_List[Talib])
                            Shipment_Status_List[Talib] = 'Receipted'
                        except KeyError:
                            Shipment_Status_List[Talib] = 'Not Sent!'
                        except NameError:
                            Shipment_Status_List[Talib] = 'Not Sent!'
                if J_M > 0:
                    if J_M == Toppler:
                        return Confirmation_Email
                    Shipment_Status_List[Talib] = 'In Progress'
                if J_M == 0:
                    Shipment_Status_List[Talib] = 'Arrived'
        return Confirmation_Email

    def ViewIndividualShipmentItem(self, msg, Shipment_Reference_List, Individual_Shipment_Carton_Placed, Individual_Shipment_Status,
                                   Shipment_Groupby_Refs, Individual_Shipment_Pallet_Amount):

        No_Refs_Today_Msg = [[1],[2]]
        No_Refs_Today_Msg = pickle.dumps(No_Refs_Today_Msg, protocol=2)

        mosdef = msg[22]
        mosdef = mosdef[0]
        Talib = msg[21]
        Talib = Talib[0]
        if int(Talib) >= len(Shipment_Reference_List):
            return No_Refs_Today_Msg
        if int(mosdef) >= len(Individual_Shipment_Carton_Placed[int(Talib)]):
            return No_Refs_Today_Msg
        Shipment_Ref = Shipment_Reference_List[int(Talib)]
        statuses = Individual_Shipment_Status[int(Talib)]
        Ref_in_Questions = Shipment_Groupby_Refs.get_group(Shipment_Ref)
        eZdoesIT = len(Ref_in_Questions)
        codes = []
        carts = []
        Metta = []
        world_peace = []
        Pallet_Amounts = Individual_Shipment_Pallet_Amount[int(Talib)]
        for row in range(0, eZdoesIT):
            TT = Ref_in_Questions.iloc[[row]]
            Code = TT['code'].values
            Code = (",".join(Code))
            quantity = TT['quantity'].values
            box_amount = TT['name'].values
            cartons = TT['name2'].values
            metta = TT['description'].values
            metta = (','.join(metta))
            cartons = cartons[0]
            box_amount = box_amount[0]
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
            codes.append(Code)
            carts.append(carton)
            Metta.append(metta)
            world_peace.append(inbox)
        maga = [codes, carts, statuses, Metta, world_peace, Pallet_Amounts]
        maga = pickle.dumps(maga, protocol=2)
        return maga


    def AddBoxesToVirtualPallet(self, msg, Individual_Shipment_Carton_Placed, Individual_Shipment_Status, Shipment_Status_List):

        No_Refs_Today_Msg = [[1],[2]]
        No_Refs_Today_Msg = pickle.dumps(No_Refs_Today_Msg, protocol=2)

        Talib = msg[21]
        Mos_Def = msg[22]
        Cartons_Placed = msg[23]
        Talib = Talib[0]
        Mos_Def = Mos_Def[0]
        Cartons_Placed = Cartons_Placed[0]
        Shipment_Line = Individual_Shipment_Carton_Placed[int(Talib)]
        Shipment_Line[int(Mos_Def)] += float(Cartons_Placed)
        Palooza = Individual_Shipment_Status[int(Talib)]
        Pop_For_Roc = 0
        if Palooza[int(Mos_Def)] == 'Receipted':
            Pop_For_Roc = 1
        if Pop_For_Roc == 0:
            Palooza[int(Mos_Def)] = 'In Progress'
            Shipment_Status_List[int(Talib)] = 'In Progress'
        return No_Refs_Today_Msg

    def RemoveBoxesFromVirtualPallet(self, msg, Individual_Shipment_Carton_Placed, Individual_Shipment_Status, Shipment_Status_List):

        No_Refs_Today_Msg_3 = [[1],[2],[3]]
        No_Refs_Today_Msg_3 = pickle.dumps(No_Refs_Today_Msg_3, protocol=2)

        Talib = msg[22]
        Mos_Def = msg[23]
        Cartons_Placed = msg[24]
        Talib = Talib[0]
        Mos_Def = Mos_Def[0]
        Cartons_Placed = Cartons_Placed[0]
        Shipment_Line = Individual_Shipment_Carton_Placed[int(Talib)]
        Shipment_Line[int(Mos_Def)] -= float(Cartons_Placed)
        Palooza = Individual_Shipment_Carton_Placed[int(Talib)]
        John_Paxon = 0
        Paloozaa = Individual_Shipment_Status[Talib]
        if Palooza[int(Mos_Def)] == 0:
            John_Paxon = 1
        if John_Paxon == 0:
            Paloozaa[int(Mos_Def)] = 'In Progress'
            Shipment_Status_List[int(Talib)] = 'In Progress'
        else:
            Paloozaa[int(Mos_Def)] = 'No'
            Shipment_Status_List[int(Talib)] = 'Arrived'
        return No_Refs_Today_Msg_3

    def MarkItemGroupAsReceipted(self, msg, Individual_Shipment_Status, Individual_Shipment_Users, Individual_Shipment_Carton_Placed,
                                 PutAway_Groupby_Refs, Shipment_Reference_List, Shipment_Status_List):


        Confirmation_Email = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]
        Confirmation_Email = pickle.dumps(Confirmation_Email, protocol=2)

        Talib = msg[23]
        Talib = Talib[0]
        Mos_Def = msg[24]
        Mos_Def = Mos_Def[0]
        User_That_Receipted = msg[25]
        User_That_Receipted = User_That_Receipted[0]
        Portable = Individual_Shipment_Status[int(Talib)]
        Portable[int(Mos_Def)] = 'Receipted'
        Pasta = Individual_Shipment_Users[int(Talib)]
        Pasta[int(Mos_Def)] = User_That_Receipted
        MJ = Individual_Shipment_Carton_Placed[int(Talib)]
        for count, status in enumerate(Individual_Shipment_Status):
            J_M = 0
            Talib = count
            for Police, answer in enumerate(status):
                Toppler = len(status)
                if answer == 'Receipted':
                    J_M += 1
                    if J_M == Toppler:
                        try:
                            people = PutAway_Groupby_Refs.get_group(Shipment_Reference_List[Talib])
                            Shipment_Status_List[Talib] = 'Receipted'
                        except KeyError:
                            Shipment_Status_List[Talib] = 'Not Sent!'
                        except NameError:
                            Shipment_Status_List[Talib] = 'Not Sent!'
                    if J_M > 0:
                        if J_M == Toppler:
                            return Confirmation_Email
                        Shipment_Status_List[Talib] = 'In Progress'
                    if J_M == 0:
                        Shipment_Status_List[Talib] = 'Arrived'
        return Confirmation_Email

    def SendItemListGroupToPutAwayDataFrame(self, msg, Shipment_Reference_List, Individual_Shipment_Carton_Placed,
                                            PutAway_Groupby_Refs, Receipted_DFS, Shipment_Status_List, Shipment_Arrival_List,
                                            Shipment_Groupby_Refs, Individual_Shipment_Errors, Individual_Shipment_Users, Individual_Shipment_Status):

        Confirmation_Email_12 = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12]]
        Confirmation_Email_12 = pickle.dumps(Confirmation_Email_12, protocol=2)

        Confirmation_Email = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]
        Confirmation_Email = pickle.dumps(Confirmation_Email, protocol=2)

        No_Refs_Today_Msg_5 = [[1],[2],[3],[4],[5]]
        No_Refs_Today_Msg_5 = pickle.dumps(No_Refs_Today_Msg_5, protocol=2)

        Talib = msg[25]
        Talib = Talib[0]
        Mos_Def = msg[26]
        Mos_Def = Mos_Def[0]
        Container_In_Question = Shipment_Reference_List[int(Talib)]
        placesplusfaces = Individual_Shipment_Carton_Placed[int(Talib)]
        try:
            Slick_Rick = PutAway_Groupby_Refs.get_group(Container_In_Question)
            return Confirmation_Email
        except NameError:
            pass
        except KeyError:
            pass
        Arrival_Date_Of_Container = Shipment_Arrival_List[int(Talib)]
        Shipment_df = Shipment_Groupby_Refs.get_group(Container_In_Question)
        endat_deya = len(Shipment_df)
        Product_Codes = []
        Descriptions = []
        Quantities = []
        Pieces_Variable = []
        Cartons_Variable = []
        for zam in range(0, endat_deya):
            RR = Shipment_df.iloc[[zam]]
            code = RR['code'].values
            code = (",".join(code))
            CT = RR['name2'].values
            CT = (",".join(CT))
            PT = RR['name'].values
            PT = (','.join(PT))
            des = RR['description'].values
            des = (",".join(des))
            Quan = RR['quantity'].values
            Product_Codes.append(code)
            Descriptions.append(des)
            Quantities.append(Quan)
            Pieces_Variable.append(PT)
            Cartons_Variable.append(CT)
        shippo_errors = (Individual_Shipment_Errors[int(Talib)])
        shippo_users = (Individual_Shipment_Users[int(Talib)])
        shippo_status = (Individual_Shipment_Status[int(Talib)])
        shap_up = 0
        meetings = len(shippo_errors)
        references = [Container_In_Question] * meetings
        arrivals = [Arrival_Date_Of_Container] * meetings
        for answer in shippo_status:
            if answer == 'Receipted':
                shap_up += 1

        if shap_up == meetings:
            reference = pd.DataFrame({'reference': references})
            arriba = pd.DataFrame({'arrivalDate': arrivals})
            coder = pd.DataFrame({'code': Product_Codes})
            desk = pd.DataFrame({'description': Descriptions})
            qaps = pd.DataFrame({'quantity': Quantities})
            nam = pd.DataFrame({'name': Pieces_Variable})
            name2 = pd.DataFrame({'name2': Cartons_Variable})
            recstat = pd.DataFrame({'status': shippo_status})
            shiperrors = pd.DataFrame({'errors': shippo_errors})
            shipuseme = pd.DataFrame({'user': shippo_users})
            cartons_rec = pd.DataFrame({'cartonsReceipted': placesplusfaces})
            Receipted_DF = (pd.concat(
                [reference, arriba, coder, desk, qaps, nam, name2, recstat, shiperrors, shipuseme, cartons_rec],
                axis=1))
            if isinstance(Receipted_DFS, pd.DataFrame) is False:
                Receipted_DFS = Receipted_DF
                print(Receipted_DFS)
                Shipment_Status_List[int(Talib)] = 'Receipted'
                return Confirmation_Email_12
            else:
                Receipted_DFS = pd.concat([Receipted_DFS, Receipted_DF])
                print(Receipted_DFS)
                Shipment_Status_List[int(Talib)] = 'Receipted'
                return Confirmation_Email_12
        return No_Refs_Today_Msg_5

    def PalletTagGenerator(self, Pallet_Tag_Number):
        print('I need to send the current pallet tag and then add one')
        msg = [[1], [2], [3]]
        msg.append([Pallet_Tag_Number])
        msg = pickle.dumps(msg, protocol=2)
        Pallet_Tag_Number += 1
        return msg

    def LogVirtualPallet(self, msg, Individual_Shipment_Carton_Placed, Individual_Shipment_Pallet_Amount, PutAway_Pallet_Counter):
        Conform_To_Society = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]
        User_that_palleted = msg[26]
        Talib = msg[27]
        Mos_Def = msg[28]
        User_that_palleted = User_that_palleted[0]
        Talib = Talib[0]
        Mos_Def = Mos_Def[0]
        Placed_Line = Individual_Shipment_Carton_Placed[int(Talib)]
        Amount_Placed = Placed_Line[int(Mos_Def)]
        Pallet_Amount = Individual_Shipment_Pallet_Amount[int(Talib)]
        Pallet_Counter_Line = PutAway_Pallet_Counter[int(Talib)]
        ptnum = msg[25]
        ptnum = ptnum[0]
        try:
            ptnum = ptnum[0]
        except TypeError as e:
            pass


        if Pallet_Amount[int(Mos_Def)] == [1, 0.00, 0000, None, '', '']:
            Pallet_Amount[int(Mos_Def)] = [[1, Amount_Placed, ptnum, None, '', User_that_palleted]]
            Conform_To_Society.append([Pallet_Amount])
            Conform_To_Society = pickle.dumps(Conform_To_Society, protocol=2)
            Pallet_Tag_Number = int(ptnum) + 1
            return Conform_To_Society
        else:
            for count, pallet in enumerate(Pallet_Amount[Mos_Def]):
                Pallet_Number = count
            People = Pallet_Number + 2
            Pallet_Amount[int(Mos_Def)].append([People, Amount_Placed, ptnum, None, '', User_that_palleted])

        Conform_To_Society.append([Pallet_Amount])
        Conform_To_Society = pickle.dumps(Conform_To_Society, protocol=2)
        Pallet_Tag_Number = ptnum + 1
        return Conform_To_Society

    def SendErrorMessageToOffice(self, msg, Shipment_Groupby_Refs, Shipment_Reference_List):

        Confirmation_Email = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]
        Confirmation_Email = pickle.dumps(Confirmation_Email, protocol=2)

        Message = msg[27]
        Talib = msg[28]
        Mos_Def = msg[29]
        Message = Message[0]
        Talib = Talib[0]
        Mos_Def = Mos_Def[0]
        print(Message, Talib, Mos_Def)
        Shipment_Item_In_Question = Shipment_Groupby_Refs.get_group(Shipment_Reference_List[Talib])
        eggs_and_ham = len(Shipment_Item_In_Question)
        acoda = []
        adesk = []
        for x in range(0, eggs_and_ham):
            PAK = Shipment_Item_In_Question.iloc[[x]]
            coda = PAK['code'].values
            coda = (','.join(coda))
            desk = PAK['description'].values
            desk = (','.join(desk))
            acoda.append(coda)
            adesk.append(desk)

        Message_To_Send = Message
        List_Of_Emails_To_Send = ['PurchaseLedger@Fleetluxury.com']
        print(Message_To_Send)
        for email in List_Of_Emails_To_Send:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("USERNAME", "PASSWORD")
            server.sendmail(
                "FleetWarehouseApp@gmail.com",
                email,
                Message_To_Send)
            print('Error Message sent to ' + email)
            server.quit()

        return Confirmation_Email