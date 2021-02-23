import pickle
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import datetime

class CheckingModeMessages:

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
            server.login("FleetWarehouseApp", "Luxury123")
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