import cv2
import numpy as np
import face_recognition
# lister le fichier ds un repertoire
import os
from fpdf import FPDF, HTMLMixin
import datetime
import sqlite3
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.base import MIMEBase
# from email import encoders
from pathlib import Path
import smtplib


master = input("Entrer Votre Classe : ")
module = input("Module : ")
nom_prof = input("Professeur : ")

#INitailize listes and db conectiion

classNames = []


encodeListKnown = []
db = sqlite3.connect("database.db")
#retrouve faceencoding and class name apartir du bdd
cr = db.cursor()
ir = cr.execute("select * from data")
for ls in ir:
    encodeListKnown.append(np.array(list(ls)))
    
cur = db.cursor()
ir1 = cur.execute("select * from infos")
for ls in ir1:
    classNames.append(ls)


print('Encoding Complete.')
#open a video capture object
cap = cv2.VideoCapture(0)
# initialose une lsite ou il stoke mes donne

liste_des_pres = []
# une boucle pour face_recognition
while True:
    # lire la trame from the video capture
    _, img = cap.read()
# recevoir la trame from the video capture and le converti on rgb
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
# trouve la localisation du visage et encoder dans la trame
    faceCurentFrame = face_recognition.face_locations(imgS)
    encodeCurentFrame = face_recognition.face_encodings(imgS, faceCurentFrame)

    for encodeface, faceLoc in zip(encodeCurentFrame, faceCurentFrame):
        # compare le visage with known faces
        matches = face_recognition.compare_faces(encodeListKnown, encodeface, 0.5)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeface)
        matchIndex = np.argmin(faceDis)
        # si il sont matcher  anonncer l image avec le nom
        if matches[matchIndex]:
            name = classNames[matchIndex][0].upper()
            liste_des_pres.append(classNames[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
        #  sinon dannocer le b unknown
        else:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)
            cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,0,255), cv2.FILLED)
            cv2.putText(img, "Inconnue", (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

    cv2.imshow('Face Recogntion', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()

ens = set(liste_des_pres)
liste = list(ens)

#--------------------------------------------------- PDF -----------------------------------------

class PDF(FPDF, HTMLMixin):
    def header(self):
        # Logo
        self.image('fst.jpeg', 10, 9, 27)
        self.image('Hassan1.jpeg', 160, 8, 40)
        # Arial bold 15
        self.set_font('Arial', 'B', 12)
        # Move to the right
        self.cell(40)
        # Title
        self.cell(100, 10, 'Faculte des sciences et techniques de SETTAT', 0, 1, 'C')
        #---------------------------------------------------------------------------
        self.set_font('Times', 'I', 13)
        self.cell(40)
        self.cell(100, 5, 'Université HASSAN 1ere ', 0, 1, 'C')
        #-------------------------
        self.ln(10)
        self.set_fill_color(0, 0, 0)
        self.cell(180,0.5,"", 1, 0, "L", 1)
    
    def sous_header(self, master, dt, prof, module):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        self.ln(8)
        # Move to the right
        self.cell(35)
        # Title
        self.cell(50, 10, f'La liste des Etudiants de {master}', 0, 1)
        self.set_font('Times', 'B', 13)
        self.cell(70)
        self.cell(60, 10, f'Module {module}', 0, 1)
        self.set_font('Times', 'B', 13)
        self.cell(50)
        self.cell(60, 10, f'Professeur : {prof}', 0, 1)
        self.set_font('Times', 'B', 13)
        self.cell(70)
        self.cell(60, 10, f' {dt}', 0, 1)
        self.ln(15)

# Instantiation of inherited class
la_date = datetime.datetime.now()
if liste:
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.sous_header(master, la_date.strftime("%x %X"), nom_prof, module)
    
    pdf.cell(50)
    pdf.cell(60, 10, "Liste des étudiants présents : ", 0, 1)
    pdf.set_font('Times','b', size=10)
    line_height = pdf.font_size * 2.5
    col_width = pdf.w / 4.5

    lh_list = [] 
    use_default_height = 0
    pdf.set_font_size(size=12)
    for col in ["Nom ", "Prenom", "CNI", "CNE"]:
        pdf.multi_cell(col_width, line_height, col, border=1, align='L', ln=3, max_line_height=pdf.font_size)
    pdf.ln(line_height)
    
    pdf.set_font(style='')
    pdf.set_font_size(size=10)
    for row in liste:
        for data in row:
            word_list = data.split()
            number_of_words = len(word_list)
            if number_of_words>2:
                use_default_height = 1
                new_line_height = pdf.font_size * (number_of_words/2)
        if not use_default_height:
            lh_list.append(line_height)
        else:
            lh_list.append(new_line_height)
            use_default_height = 0
                    
    for j,row in enumerate(liste):
        for data in row:
            line_height = lh_list[j] 
            pdf.multi_cell(col_width, line_height, data, border=1,align='L',ln=3, 
            max_line_height=pdf.font_size)
        pdf.ln(line_height)
    liste1 = []
    for i in classNames :
        if i not in liste :
            liste1.append(i)
    
    pdf.set_font('Times','b', size=12)
    pdf.cell(50)
    pdf.cell(60, 10, "Liste des étudiants abscents : ", 0, 1)
    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4.5
    lh_list1 = [] 
    use_default_height = 0
    pdf.set_font_size(size=12)
    for col in ["Nom ", "Prenom", "CIN", "CNE"]:
        pdf.multi_cell(col_width, line_height, col, border=1, align='L', ln=3, max_line_height=pdf.font_size)
    pdf.ln(line_height)
    
    
    pdf.set_font(style='')
    pdf.set_font_size(size=10)
    for row in liste1:
        for data in row:
            word_list = data.split()
            number_of_words = len(word_list)
            if number_of_words>2:
                use_default_height = 1
                new_line_height = pdf.font_size * (number_of_words/2)
        if not use_default_height:
            lh_list1.append(line_height)
        else:
            lh_list1.append(new_line_height)
            use_default_height = 0
            
    for j,row in enumerate(liste1):
        for data in row:
            line_height = lh_list1[j] 
            #pdf.multi_cell(col_width, line_height, col, border=1, align='L', max_line_height=pdf.font_size)

            pdf.multi_cell(col_width, line_height, data, border=1,align='L',ln=3, 
             max_line_height=pdf.font_size)
        pdf.ln(line_height)
        
    pdf.output(f'{master}.pdf')
    
    # message = MIMEMultipart()
    # message["from"] = "FST SETTAT"
    # message["to"] = mail
    # message["subject"] = f"Presence de classe {master} {la_date.strftime('%d')} {la_date.strftime('%b')} {la_date.year}   {la_date.strftime('%H')}:{la_date.strftime('%M')}"
    # message.attach(MIMEText(f"Bonjour Professeur {nom_prof}.\n Vous Trouverez ci-join La liste des Presence du classe  {master}.\n Bonne reception", "plain"))
    # pdfname = f'{master}.pdf'
    # # open the file in bynary
    # binary_pdf = open(pdfname, 'rb')
    # payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    # payload.set_payload((binary_pdf).read())
    # # enconding the binary into base64
    # encoders.encode_base64(payload)
    # # add header with pdf name
    # payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    # message.attach(payload)

    # with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    #     smtp.ehlo()
    #     smtp.starttls()
    #     smtp.login("aicha.njimat@gmail.com","Njimate.@2001")
    #     smtp.send_message(message)
    #     print("send...")