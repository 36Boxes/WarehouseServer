import pickle
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

class PutAwayModeMessages:

    def BootUp_PutAwayMode(self, PutAway_Reference_List, PutAway_Status_List):
        print("Received Put-Away Mode Bootup Message, Responding With Put-Away Lists.")
        Message_i_wanna_send = ['pizza', 'tablets', 'grapes', PutAway_Reference_List, PutAway_Status_List]
        Message_i_wanna_send = pickle.dumps(Message_i_wanna_send, protocol=2)
        return Message_i_wanna_send

    def ViewDetailedPutAwayList(self, msg, Shipment_Reference_List, PutAway_Reference_List, Individual_Shipment_Pallet_Amount, PutAway_Pallet_Counter, PutAway_Groupby_Refs, Individual_PutAway_Status):
        Tom = msg[30]
        Tom = Tom[0]
        for count, ref in enumerate(Shipment_Reference_List):
            try:
                if ref == PutAway_Reference_List[int(Tom)]:
                    talib = count
                    break
            except IndexError as e:
                msg2return = [['No'], ['Item']]
                msg2return = pickle.dumps(msg2return, protocol=2)
                return msg2return

        Number_of_pallets = Individual_Shipment_Pallet_Amount[talib]
        Pallet_Counter_Line = PutAway_Pallet_Counter[talib]
        print(Number_of_pallets)
        Ref_Clicked = PutAway_Reference_List[int(Tom)]
        DF_Clicked = PutAway_Groupby_Refs.get_group(Ref_Clicked)
        Tumbleweed = len(DF_Clicked)
        Codes = []
        for x in range(0, Tumbleweed):
            TT = DF_Clicked.iloc[[x]]
            Code = TT['code'].values
            Code = (",".join(Code))
            Codes.append(Code)
        Paxson = Pallet_Counter_Line
        Statuses = Individual_PutAway_Status[int(Tom)]
        Magic = [Codes, Statuses, Number_of_pallets, Paxson]
        Magic = pickle.dumps(Magic, protocol=2)
        return Magic

    def ViewDetailedIndividualItem(self, msg, PutAway_Reference_List, Shipment_Reference_List, Individual_Shipment_Pallet_Amount, PutAway_Groupby_Refs, Individual_PutAway_Status, Individual_PutAway_Users, Individual_PutAway_Errors, Individual_PutAway_Location):
        Tom = msg[30]
        Jerry = msg[31]
        Tom = Tom[0]
        Jerry = Jerry[0]
        Ref_We_Clicked = PutAway_Reference_List[int(Tom)]
        for count, ref in enumerate(Shipment_Reference_List):
            if ref == Ref_We_Clicked:
                Talib = count
                break
        Pallets = Individual_Shipment_Pallet_Amount[Talib]
        print(Pallets)
        Df_Clocked = PutAway_Groupby_Refs.get_group(Ref_We_Clicked)
        Tabloid = len(Df_Clocked)
        Put_away_stats = Individual_PutAway_Status[int(Tom)]
        Put_away_users = Individual_PutAway_Users[int(Tom)]
        Put_away_errors = Individual_PutAway_Errors[int(Tom)]
        Put_away_locs = Individual_PutAway_Location[int(Tom)]

        Descriptions = []
        Product_Codes = []
        Carton_Var = []
        Piece_Var = []
        Cartons_Placed = []
        for x in range(0, Tabloid):
            TAP = Df_Clocked.iloc[[x]]
            dep = TAP['description'].values
            cod = TAP['code'].values
            pieceio = TAP['name'].values
            cartonio = TAP['name2'].values
            qaps = TAP['quantity'].values
            cartons_placed = TAP['cartonsReceipted'].values
            dep = (','.join(dep))
            cod = (','.join(cod))
            pieceio = (','.join(pieceio))
            cartonio = (','.join(cartonio))
            ASCII = ord(cartonio[0])
            ASCIII = ord(pieceio[0])
            if ASCII == 82:
                cartons = str(cartonio)
                carton = cartonio[1:]
            elif ASCII == 67:
                cartons = str(cartonio)
                carton = cartonio[2:]
            elif ASCII == 80:
                cartons = str(cartonio)
                carton = cartonio[1:]
            elif ASCII == 69:
                carton = cartonio
                carton = 1
            if ASCIII == 82:
                box_amount = str(pieceio)
                inbox = pieceio[1:]
            elif ASCIII == 67:
                box_amount = str(pieceio)
                inbox = pieceio[2:]
            elif ASCIII == 80:
                box_amount = str(pieceio)
                inbox = pieceio[1:]
            elif ASCIII == 69:
                inbox = pieceio
                inbox = 1
            inbox = float(qaps) * int(inbox)
            carton = int(inbox) / int(carton)
            Carton_Var.append(carton)
            Piece_Var.append(inbox)
            Product_Codes.append(cod)
            Descriptions.append(dep)
            Cartons_Placed.append(cartons_placed)
        placco = []
        for x in range(0, len(Cartons_Placed)):
            popsi = Cartons_Placed[x]
            popsi = 1 * float(popsi)
            placco.append(popsi)
        print(placco)
        Data2Send = [Put_away_errors, Put_away_locs, Put_away_stats, Put_away_users, Product_Codes, Descriptions,
                     Piece_Var, Carton_Var, placco, Pallets]
        Data2Send = pickle.dumps(Data2Send, protocol=2)
        return Data2Send

    def MarkLocationPlaced(self, msg, PutAway_Reference_List, Shipment_Reference_List, Individual_Shipment_Pallet_Amount,
                           PutAway_Pallet_Counter, Individual_PutAway_Status, PutAway_Status_List):
        User_who_done_it = msg[28]
        User_who_done_it = User_who_done_it[0]
        Location_Placed = msg[29]
        My_Pallet_Num = msg[30]
        Tom = msg[31]
        Jerry = msg[32]
        Tom = Tom[0]
        Jerry = Jerry[0]
        My_Pallet_Num = My_Pallet_Num[0]
        Location_Placed = Location_Placed[0]
        Ref_That_User_Selected = PutAway_Reference_List[int(Tom)]
        for count, ref in enumerate(Shipment_Reference_List):
            if ref == Ref_That_User_Selected:
                Talib = count
                break
        Pallets = Individual_Shipment_Pallet_Amount[Talib]
        Pallet_Counter_Line = PutAway_Pallet_Counter[Talib]
        Palletsq = Pallets[int(Jerry)]
        print(Palletsq)
        Pallets = Palletsq[My_Pallet_Num]
        print(Pallets)
        Pallets[3] = Location_Placed
        Pallets[4] = User_who_done_it
        print(Pallets)
        rest = ['Ceasar', 'IS HOME']
        rest = pickle.dumps(rest, protocol=2)
        piece = PutAway_Pallet_Counter[Talib]
        Pallet_Counter_Line[int(Jerry)] += 1
        palpal = Individual_PutAway_Status[int(Tom)]
        palpal[int(Jerry)] = 'In Progress'
        Status_Qo = Individual_PutAway_Status[int(Tom)]
        if Pallet_Counter_Line[int(Jerry)] == len(Palletsq):
            pap = Individual_PutAway_Status[int(Tom)]
            pap[int(Jerry)] = 'Put-Away'
        else:
            Status_Qo[int(Jerry)] = 'In Progress'
        pillows = 0
        for stat in Status_Qo:
            if stat == 'Put-Away':
                pillows += 1
        if Pallet_Counter_Line[int(Jerry)] > 0:
            PutAway_Status_List[int(Tom)] = 'In Progress'

        if pillows == len(Status_Qo):
            PutAway_Status_List[int(Tom)] = 'Put-Away'
        return rest

    def MarkPutAwayGroupAsPutAway(self, msg, Individual_PutAway_Status, PutAway_Reference_List, Shipment_Reference_List, Individual_Shipment_Pallet_Amount, PutAway_Status_List):
        Tom = msg[32]
        Tom = Tom[0]
        Jerry = msg[33]
        Jerry = Jerry[0]
        Status_Qo = Individual_PutAway_Status[int(Tom)]
        Ref_That_User_Selected = PutAway_Reference_List[int(Tom)]
        for count, ref in enumerate(Shipment_Reference_List):
            if ref == Ref_That_User_Selected:
                Talib = count
                break
        Pallets = Individual_Shipment_Pallet_Amount[Talib]
        Palletsq = Pallets[int(Jerry)]
        for pallet in Palletsq:
            if pallet[3] == None:
                msg = [[1], [2], [3], [4], [5]]
                msg = pickle.dumps(msg, protocol=2)
                return msg
        Status_Qo[int(Jerry)] = 'Put-Away'
        pillows = 0
        for stat in Status_Qo:
            if stat == 'Put-Away':
                pillows += 1
        print(len(Status_Qo))

        if pillows == len(Status_Qo):
            PutAway_Status_List[int(Tom)] = 'Put-Away'
        else:
            if pillows > 0:
                PutAway_Status_List[int(Tom)] = 'In Progress'

        data2send = ['Kanye', 'is', 'the', 'goat']
        data2send = pickle.dumps(data2send, protocol=2)
        print(pillows)
        return data2send

    def SendPutAwayToOffice(self, msg, PutAway_Reference_List, Shipment_Reference_List, Shipment_Arrival_List,
                            PutAway_Groupby_Refs, Individual_Shipment_Pallet_Amount, PutAway_Pallet_Counter,
                            Individual_PutAway_Status, PutAway_DFS, Shipment_Status_List):
        Tom = msg[33]
        Jerry = msg[34]
        Tom = Tom[0]
        Jerry = Jerry[0]
        print(Tom, Jerry)
        Container = PutAway_Reference_List[int(Tom)]
        for count, ref in enumerate(Shipment_Reference_List):
            if ref == Container:
                Talib = count
                break
        arrival_date = Shipment_Arrival_List[Talib]
        PutAway_Df = PutAway_Groupby_Refs.get_group(Container)
        Stop_it = len(PutAway_Df)
        Product_Codes = []
        EXProduct_Codes = []
        Descriptions = []
        EXDescriptions = []
        Quantities = []
        EXQuantities = []
        Pieces_Variable = []
        EXPieces_Variable = []
        Cartons_Variable = []
        EXCartons_Variable = []
        pallet_quans = []
        palnumbers = []
        pallocats = []
        userpal = []
        pletuse = []
        for zam in range(0, Stop_it):
            RR = PutAway_Df.iloc[[zam]]
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
        Pallets = Individual_Shipment_Pallet_Amount[Talib]
        Pallet_Counter_Line = PutAway_Pallet_Counter[Talib]
        shapo_up = 0
        Puttyaway = Individual_PutAway_Status[int(Tom)]
        meetingz = len(Puttyaway)

        Packit_in_mate = []
        for count, pallet_LIST in enumerate(Pallets):
            for pallet in pallet_LIST:
                print(pallet)
                quant_onpla = pallet[1]
                palnums = pallet[2]
                pallocs = pallet[3]
                don_dada = pallet[4]
                user_that_pals = pallet[5]
                EXProduct_Codes.append(Product_Codes[count])
                EXCartons_Variable.append(Cartons_Variable[count])
                EXQuantities.append(Quantities[count])
                EXDescriptions.append(Descriptions[count])
                EXPieces_Variable.append(Pieces_Variable[count])
                pallet_quans.append(quant_onpla)
                palnumbers.append(palnums)
                pallocats.append(pallocs)
                userpal.append(don_dada)
                pletuse.append(user_that_pals)

        references = [Container] * (len(EXPieces_Variable))
        arrivals = [arrival_date] * (len(EXPieces_Variable))

        for quan in EXQuantities:
            p = float(quan) * 1
            Packit_in_mate.append(p)
        for answer in Puttyaway:
            if answer == 'Put-Away':
                shapo_up += 1

        if shapo_up == meetingz:
            reference = pd.DataFrame({'reference': references})
            arriba = pd.DataFrame({'arrivalDate': arrivals})
            coder = pd.DataFrame({'code': EXProduct_Codes})
            desk = pd.DataFrame({'description': EXDescriptions})
            qaps = pd.DataFrame({'quantity': Packit_in_mate})
            nam = pd.DataFrame({'name': EXPieces_Variable})
            name2 = pd.DataFrame({'name2': EXCartons_Variable})
            palletz = pd.DataFrame({'Pallet Number': palnumbers})
            palpo = pd.DataFrame({'Pallet Quantity': pallet_quans})
            palputations = pd.DataFrame({'Pallet Location': pallocats})
            don_DaDa = pd.DataFrame({'Put-Away By': userpal})
            pappo = pd.DataFrame({'Palletized By': pletuse})

            PutAway_DF = (
                pd.concat([reference, arriba, coder, desk, qaps, nam, name2, palletz, palpo, palputations, don_DaDa],
                          axis=1))
            print(PutAway_DF)
            Two_Step_Verification = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11],
                                     [12], [13], [14], [15], [16], [17], [18], [19], [20], [21]]
            Two_Step_Verification = pickle.dumps(Two_Step_Verification, protocol=2)

            if isinstance(PutAway_DFS, pd.DataFrame) is False:
                PutAway_DFS = PutAway_DF
                print(PutAway_DFS)
                Shipment_Status_List[int(Talib)] = 'Receipted'
                Message_To_Send = str(PutAway_DFS)
                list_of_emails = ['NG@fleetluxury.com', 'DL@fleetluxury.com', 'MS@fleetluxury.com',
                                  'CH@fleetluxury.com', 'Chloe@fleetluxury.com', 'PS@fleetluxury.com',
                                  'Peter@fleetluxury.com']
                PutAway_DFS.to_excel('output.xlsx', engine='xlsxwriter')
                for email in list_of_emails:
                    SUBJECT = "Email Data"

                    msg = MIMEMultipart()
                    msg['Subject'] = 'Put Away Sheet'
                    msg['From'] = "FleetWarehouseApp@gmail.com"
                    msg['To'] = email

                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(open("output.xlsx", "rb").read())
                    encoders.encode_base64(part)

                    part.add_header('Content-Disposition', 'attachment; filename="output.xlsx"')

                    msg.attach(part)
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.login("FleetWarehouseApp", "Luxury123")
                    server.sendmail("FleetWarehouseApp@gmail.com", email, msg.as_string())
                    server.quit()
                    return Two_Step_Verification
            else:
                PutAway_DFS = pd.concat([PutAway_DFS, PutAway_DF])
                print(PutAway_DFS)
                Shipment_Status_List[int(Talib)] = 'Receipted'
                return Two_Step_Verification

        U_Are_Not_Ready = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15],
                           [16], [17]]
        U_Are_Not_Ready = pickle.dumps(U_Are_Not_Ready, protocol=2)

        return U_Are_Not_Ready
