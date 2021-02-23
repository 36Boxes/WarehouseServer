import pickle
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import datetime

class CheckingModeMessages:

    global Picked_Checked_DFS

    def BootupCheckingMode(self, Picked_DFS, Checking_Reference_List, Checking_Status_List):

        No_Refs_Today_Msg = [[1], [2]]
        No_Refs_Today_Msg = pickle.dumps(No_Refs_Today_Msg, protocol=2)

        if isinstance(Picked_DFS, pd.DataFrame) is False:
            print('No Checks Yet')
            return No_Refs_Today_Msg
        else:
            print("Received Checking Mode Bootup Message, Responding With Checks.")
            Ready_to_send_Check_refs = [['First'], ['I did this']]
            Ready_to_send_Check_refs.append(Checking_Reference_List)
            Ready_to_send_Check_refs.append(Checking_Status_List)
            msg = pickle.dumps(Ready_to_send_Check_refs, protocol=2)
            return msg

    def CheckingModeViewDetailedReference(self, msg, Checking_Reference_List,
                                          Picking_Reference_List, Individual_Picking_Users,
                                          Individual_Checking_Status, Picked_DFS):

        print("Received Checking Mode See more detail Message, Responding With Filtered Lists.")
        Confirmation_Email_9 = [[1],[2],[3],[4],[5],[6],[7],[8],[9]]
        Confirmation_Email_9 = pickle.dumps(Confirmation_Email_9, protocol=2)
        MBDTF = msg[11]
        MBDTF = MBDTF[0]
        pag = len(Checking_Reference_List)
        if int(MBDTF) > pag:
            return Confirmation_Email_9
        if int(MBDTF) == pag:
            return Confirmation_Email_9
        ref_weare_using = Checking_Reference_List[int(MBDTF)]
        for count, ref in enumerate(Picking_Reference_List):
            if ref == ref_weare_using:
                choopa = count

        check_user_to_send = Individual_Picking_Users[choopa]
        checking_status = Individual_Checking_Status[int(MBDTF)]
        Ref_In_Question = Checking_Reference_List[int(MBDTF)]
        pick_to_check = Picked_DFS.groupby('reference')
        pick_to_check = pick_to_check.get_group(Ref_In_Question)
        end_of_line = len(pick_to_check)
        print(pick_to_check)
        codes = []
        Catron = []
        for num in range(0, end_of_line):
            ROW = pick_to_check.iloc[[num]]
            code = ROW['code'].values
            active_reference = ROW['reference'].values
            active_reference = (",".join(active_reference))
            catron = ROW['QuantityofCartons'].values
            catron = ", ".join(str(i) for i in catron)
            Catron.append(catron)
            code = (",".join(code))
            codes.append(code)
        READIED_DATA = [['The College Dropout'], ['Late Registration'], ['Graduation'], ['808s & Heartbreak'],
                        ['MBDTF'], ['Yeezus, TLOP & Ye']]
        READIED_DATA.append(Catron)
        READIED_DATA.append(active_reference)
        READIED_DATA.append(codes)
        READIED_DATA.append(check_user_to_send)
        READIED_DATA.append(checking_status)
        to_send = pickle.dumps(READIED_DATA, protocol=2)
        return to_send

    def SendEmailToOffice(self, Picked_Checked_DFS):
        print("Received Checking Mode Send Email Message, Sending Email To Office And Confirming On The App.")

        Confirmation_Email = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]
        Confirmation_Email = pickle.dumps(Confirmation_Email, protocol=2)

        list_of_mails = ['NG@fleetluxury.com', 'DL@fleetluxury.com', 'MS@fleetluxury.com', 'CH@fleetluxury.com',
                         'Chloe@fleetluxury.com']
        pp19 = Picked_Checked_DFS.groupby('documentDate')
        PAK = datetime.date.today()
        mp5 = pp19.get_group(PAK)
        mp5.to_excel('Daily_Picks.xlsx', engine='xlsxwriter')
        for email in list_of_mails:
            SUBJECT = "Email Data"
            msg = MIMEMultipart()
            msg['Subject'] = 'Daily Picklists'
            msg['From'] = "FleetWarehouseApp@gmail.com"
            msg['To'] = email
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open("Daily_Picks.xlsx", "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="output.xlsx"')
            msg.attach(part)
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("USERNAME", "PASSWORD")
            server.sendmail("FleetWarehouseApp@gmail.com", email, msg.as_string())
            server.quit()

        return Confirmation_Email

    def CheckingModeViewIndividualItem(self, msg, Checking_Reference_List, Checking_Groupby_Refs,
                                       Picking_Reference_List, Individual_Picking_Errors, Individual_Picking_Users):

        Confirmation_Email_9 = [[1],[2],[3],[4],[5],[6],[7],[8],[9]]
        Confirmation_Email_9 = pickle.dumps(Confirmation_Email_9, protocol=2)

        print("Received Checking Mode Send MBDTF & Throne Message, Responding With Filtered Lists.")
        MBDTF = msg[12]
        Throne = msg[13]
        MBDTF = MBDTF[0]
        Throne = Throne[0]
        Ref = Checking_Reference_List[int(MBDTF)]
        Check_In_Question = Checking_Groupby_Refs.get_group(Ref)
        if int(Throne) + 1 > len(Check_In_Question):
            return Confirmation_Email_9
        endomie = len(Check_In_Question)
        for count, ref in enumerate(Picking_Reference_List):
            if ref == Ref:
                chops = count
                break
        error_line_needed = Individual_Picking_Errors[int(chops)]
        User_line_needed = Individual_Picking_Users[int(chops)]
        check_in_q = Checking_Groupby_Refs.get_group(Ref)
        endra = len(check_in_q)
        Codes = []
        Descri = []
        QOP = []
        QOC = []
        locs = []
        for n in range(0, endra):
            pop = check_in_q.iloc[[n]]
            code = pop['code'].values
            code = (",".join(code))
            dez = pop['description'].values
            dez = (",".join(dez))
            locopp = pop['name2'].values
            locopp = (",".join(locopp))
            piece = pop['QuantityofPieces'].values
            cart = pop['QuantityofCartons'].values
            piece = ", ".join(str(i) for i in piece)
            cart = ", ".join(str(i) for i in cart)
            Codes.append(code)
            Descri.append(dez)
            QOP.append(piece)
            QOC.append(cart)
            locs.append(locopp)
        Pack_it_UP = [['Cash'], ['Rules'], ['Everything'], ['Around Me'], [Ref]]
        Pack_it_UP.append(error_line_needed)
        Pack_it_UP.append(User_line_needed)
        Pack_it_UP.append(Codes)
        Pack_it_UP.append(Descri)
        Pack_it_UP.append(QOP)
        Pack_it_UP.append(QOC)
        Pack_it_UP.append(locs)
        People = pickle.dumps(Pack_it_UP, protocol=2)
        return People

    def QuickMarkAsChecked(self, msg, Individual_Checking_Status, Individual_Checking_Users, Checking_Status_List):
        Answer = msg[11]
        print("Received Checking Mode Quick Mark Message, Marking as " + Answer[0] + '.')
        MBDTF = msg[12]
        Throne = msg[13]
        User = msg[14]
        pitter_patta = Individual_Checking_Status[int(MBDTF)]
        pitter_patta[int(Throne)] = Answer[0]
        pitter_patter = Individual_Checking_Users[int(MBDTF)]
        if Answer[0] == 'No':
            User = ''
        pitter_patter[int(Throne)] = User
        john_stockton = [Checking_Status_List, Individual_Checking_Status[int(MBDTF)]]
        john_stockton = pickle.dumps(john_stockton, protocol=2)
        return john_stockton

    def Mark_Item_As_Checked(self, msg, Individual_Checking_Status, Individual_Checking_Users,
                             Checking_Reference_List, Checking_Groupby_Refs, Individual_Checking_Errors,
                             Checking_Status_List):


        MBDTF = msg[13]
        Throne = msg[14]
        User = msg[15]
        print(MBDTF, Throne, User)
        Pick_Check_Status = Individual_Checking_Status[int(MBDTF[0])]
        Pick_Check_Status[int(Throne[0])] = 'Yes'
        Pick_Check_User = Individual_Checking_Users[int(MBDTF[0])]
        Pick_Check_User[int(Throne[0])] = User[0]
        print(Individual_Checking_Status)
        print(Individual_Checking_Users)
        counter = 0
        Challenger = 11
        Challengerd = 0
        if isinstance(MBDTF, int) is True:
            wrist = Individual_Checking_Status[MBDTF]
            poportwo = 1
        else:
            poportwo = 2
            wrist = Individual_Checking_Status[MBDTF[0]]
        for count, status in enumerate(wrist):
            if status == 'Yes':
                counter += 1
            if status == 'Yes E':
                counter += 1
                Challengerd = 1
            wra = (len(wrist))
            if counter == wra:
                Challenger = 0
                if isinstance(MBDTF, int) is True:
                    chops = MBDTF
                else:
                    chops = MBDTF[0]
                rad = Checking_Reference_List[chops]
                refti = Checking_Groupby_Refs.get_group(rad)
                rolling = len(refti)
                Checked_reflist = []
                Checked_datelist = []
                Checked_codes = []
                Checked_describ = []
                Checked_QOC = []
                Checked_locs = []
                Checked_QOP = []
                Checked_picked = []
                Checked_errors = []
                Checked_users = []
                for SL in range(0, rolling):
                    YSL = refti.iloc[[SL]]
                    reflist = YSL['reference'].values
                    reflist = (",".join(reflist))
                    dateos = YSL['documentDate'].values
                    ce = YSL['code'].values
                    ce = (','.join(ce))
                    describ = YSL['description'].values
                    describ = (",".join(describ))
                    QuanOC = YSL['QuantityofCartons'].values
                    QuanOC = QuanOC[0]
                    QuanOC = str(QuanOC)

                    loc_down = YSL['name2'].values
                    loc_down = (",".join(loc_down))
                    QuanOP = YSL['QuantityofPieces'].values
                    QuanOP = QuanOP[0]
                    QuanOP = str(QuanOP)

                    pickop = YSL['picked'].values
                    pickop = (",".join(pickop))
                    pick_ere = YSL['errors'].values
                    pick_ere = pick_ere[0]
                    try:
                        pick_ere = (",".join((pick_ere)))
                    except TypeError as e:
                        pass

                    use = YSL['user'].values
                    use = (",".join(use))
                    Checked_reflist.append(reflist)
                    Checked_datelist.append(dateos)
                    Checked_codes.append(ce)
                    Checked_describ.append(describ)
                    Checked_QOC.append(QuanOC)
                    Checked_locs.append(loc_down)
                    Checked_QOP.append(QuanOP)
                    Checked_picked.append(pickop)
                    Checked_errors.append(pick_ere)
                    Checked_users.append(use)
                dates = [datetime.date.today()] * len(Checked_reflist)
                reference = pd.DataFrame({'reference': Checked_reflist})
                documentDate = pd.DataFrame({'documentDate': dates})
                code = pd.DataFrame({'code': Checked_codes})
                description = pd.DataFrame({'description': Checked_describ})
                nam = pd.DataFrame({'QuantityofCartons': Checked_QOC})
                name2 = pd.DataFrame({'name2': Checked_locs})
                name3 = pd.DataFrame({'QuantityofPieces': Checked_QOP})
                pickeder = pd.DataFrame({'picked': Checked_picked})
                errors = pd.DataFrame({'errors': Checked_errors})
                users = pd.DataFrame({'user': Checked_users})
                checkder = pd.DataFrame({'checked': Individual_Checking_Status[chops]})
                cherror = pd.DataFrame({'checkError': Individual_Checking_Errors[chops]})
                cheuser = pd.DataFrame({'checkUser': Individual_Checking_Users[chops]})
                Picked_Checked_DF = (pd.concat(
                    [reference, documentDate, code, description, nam, name2, name3, pickeder, errors, users, checkder,
                     cherror, cheuser], axis=1))
                try:
                    print(Picked_Checked_DFS)
                    Picked_Checked_DFS = pd.concat([Picked_Checked_DFS, Picked_Checked_DF])

                    print(Picked_Checked_DFS)

                except NameError as e:
                    print('This is the First Check of the day')
                    Picked_Checked_DFS = Picked_Checked_DF
        if Challenger == 0:
            if Challengerd == 1:
                print(Checking_Status_List)
                Checking_Status_List[chops] = 'Checked Error'
                passitback = [Checking_Status_List, Individual_Checking_Status[chops], 3, 4, 5, 6, 7, 8, 9, 0]
                passitback = pickle.dumps(passitback, protocol=2)
                return passitback
            else:
                print(Checking_Status_List)
                Checking_Status_List[chops] = 'Checked'
                passitback = [Checking_Status_List, Individual_Checking_Status[chops], 3, 4, 5, 6, 7, 8, 9, 0]
                passitback = pickle.dumps(passitback, protocol=2)
                return passitback
        else:
            if poportwo == 1:
                print(Checking_Status_List)
                Checking_Status_List[MBDTF[0]] = 'Incomplete'
                passitback = [Checking_Status_List, Individual_Checking_Status[MBDTF[0]], 3, 4, 5, 6, 7, 8, 9]
                passitback = pickle.dumps(passitback, protocol=2)
                return passitback
            if poportwo == 2:
                print(Checking_Status_List)
                Checking_Status_List[MBDTF[0]] = 'Incomplete'
                passitback = [Checking_Status_List, Individual_Checking_Status[MBDTF[0]], 3, 4, 5, 6, 7, 8, 9]
                passitback = pickle.dumps(passitback, protocol=2)
                return passitback


    def LogError(self, msg, Checking_Reference_List, Checking_Groupby_Refs, Individual_Checking_Errors,
                 Individual_Checking_Users, Individual_Checking_Status, Checking_Status_List):
        User = msg[13]
        MBDTF = msg[14]
        Throne = msg[15]
        Error = msg[16]
        MBDTF = int(MBDTF[0])
        Throne = int(Throne[0])
        ref_we_need = Checking_Reference_List[MBDTF]
        reffed = Checking_Groupby_Refs.get_group(ref_we_need)
        error_line = Individual_Checking_Errors[MBDTF]
        error_line[Throne] = Error
        Status_line = Individual_Checking_Users[MBDTF]
        Status_line[Throne] = str(User[0])
        Panko = Individual_Checking_Status[MBDTF]
        Panko[Throne] = 'Yes E'
        counter = 0
        Challenger = 11
        Challengerd = 0
        if isinstance(MBDTF, int) is True:
            wrist = Individual_Checking_Status[MBDTF]
            poportwo = 1
        else:
            poportwo = 2
            wrist = Individual_Checking_Status[MBDTF[0]]
        for count, status in enumerate(wrist):
            if status == 'Yes':
                counter += 1

            if status == 'Yes E':
                counter += 1
                Challengerd = 1

            wra = (len(wrist))
            if counter == wra:
                Challenger = 0
                if isinstance(MBDTF, int) is True:
                    chops = MBDTF
                else:
                    chops = MBDTF[0]
                    rad = Checking_Reference_List[chops]
                    refti = Checking_Groupby_Refs.get_group(rad)
                    rolling = len(refti)
                    Checked_reflist = []
                    Checked_datelist = []
                    Checked_codes = []
                    Checked_describ = []
                    Checked_QOC = []
                    Checked_locs = []
                    Checked_QOP = []
                    Checked_picked = []
                    Checked_errors = []
                    Checked_users = []
                    for SL in range(0, rolling):
                        YSL = refti.iloc[[SL]]
                        reflist = YSL['reference'].values
                        reflist = (",".join(reflist))
                        dateos = YSL['documentDate'].values
                        ce = YSL['code'].values
                        ce = (','.join(ce))
                        describ = YSL['description'].values
                        describ = (",".join(describ))
                        QuanOC = YSL['QuantityofCartons'].values
                        QuanOC = QuanOC[0]
                        QuanOC = str(QuanOC)

                        loc_down = YSL['name2'].values
                        loc_down = (",".join(loc_down))
                        QuanOP = YSL['QuantityofPieces'].values
                        QuanOP = QuanOP[0]
                        QuanOP = str(QuanOP)

                        pickop = YSL['picked'].values
                        pickop = (",".join(pickop))
                        pick_ere = YSL['errors'].values
                        pick_ere = pick_ere[0]
                        try:
                            pick_ere = (",".join((pick_ere)))
                        except TypeError as e:
                            print(e)

                        use = YSL['user'].values
                        use = (",".join(use))
                        Checked_reflist.append(reflist)
                        Checked_datelist.append(dateos)
                        Checked_codes.append(ce)
                        Checked_describ.append(describ)
                        Checked_QOC.append(QuanOC)
                        Checked_locs.append(loc_down)
                        Checked_QOP.append(QuanOP)
                        Checked_picked.append(pickop)
                        Checked_errors.append(pick_ere)
                        Checked_users.append(use)

                    dates = [datetime.date.today()] * len(Checked_reflist)
                    reference = pd.DataFrame({'reference': Checked_reflist})
                    documentDate = pd.DataFrame({'documentDate': dates})
                    code = pd.DataFrame({'code': Checked_codes})
                    description = pd.DataFrame({'description': Checked_describ})
                    nam = pd.DataFrame({'QuantityofCartons': Checked_QOC})
                    name2 = pd.DataFrame({'name2': Checked_locs})
                    name3 = pd.DataFrame({'QuantityofPieces': Checked_QOP})
                    pickeder = pd.DataFrame({'picked': Checked_picked})
                    errors = pd.DataFrame({'errors': Checked_errors})
                    users = pd.DataFrame({'user': Checked_users})
                    checkder = pd.DataFrame({'checked': Individual_Checking_Status[chops]})
                    cherror = pd.DataFrame({'checkError': Individual_Checking_Errors[chops]})
                    cheuser = pd.DataFrame({'checkUser': Individual_Checking_Users[chops]})
                    Picked_Checked_DF = (pd.concat(
                        [reference, documentDate, code, description, nam, name2, name3, pickeder, errors, users,
                         checkder, cherror, cheuser], axis=1))
                    try:
                        print(Picked_Checked_DFS)
                        Picked_Checked_DFS = pd.concat([Picked_Checked_DFS, Picked_Checked_DF])
                        print(Picked_Checked_DFS)

                    except NameError as e:
                        print('This is the First Check of the day')
                        Picked_Checked_DFS = Picked_Checked_DF
        if Challenger == 0:
            if Challengerd == 1:
                print(Checking_Status_List)
                Checking_Status_List[MBDTF] = 'Checked Error'
                passitback = [Checking_Status_List, Individual_Checking_Status[MBDTF], 3, 4, 5, 6, 7, 8, 9, 0]
                passitback = pickle.dumps(passitback, protocol=2)
                return passitback
            else:
                print(Checking_Status_List)
                Checking_Status_List[MBDTF] = 'Checked'
                passitback = [Checking_Status_List, Individual_Checking_Status[MBDTF], 3, 4, 5, 6, 7, 8, 9, 0]
                passitback = pickle.dumps(passitback, protocol=2)
                return passitback
        else:
            if poportwo == 1:
                print(Checking_Status_List)
                Checking_Status_List[MBDTF] = 'Incomplete'
                passitback = [Checking_Status_List, Individual_Checking_Status[MBDTF], 3, 4, 5, 6, 7, 8, 9, 0]
                passitback = pickle.dumps(passitback, protocol=2)
                return passitback
            if poportwo == 2:
                print(Checking_Status_List)
                Checking_Status_List[MBDTF] = 'Incomplete'
                passitback = [Checking_Status_List, Individual_Checking_Status[MBDTF], 3, 4, 5, 6, 7, 8, 9, 0]
                passitback = pickle.dumps(passitback, protocol=2)
                return passitback