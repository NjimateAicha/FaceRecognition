
import cv2
import numpy as np
import face_recognition
import os
from fpdf import FPDF, HTMLMixin
import datetime
import sqlite3

print("Start\n")
path = 'persons'
images = []
classNames = []
personsList = os.listdir(path)

for cl in personsList:
    curPersonn = cv2.imread(f'{path}/{cl}')
    images.append(curPersonn)
    classNames.append(os.path.splitext(cl)[0])


def findEncodeings(image):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

list_known = findEncodeings(images)

db = sqlite3.connect('database.db')

# db.execute("create table infos (name text , CNI text, CNE text, apogee text)")
cur = db.cursor()
for element in classNames:
    tr = element.split(",")
    cur.execute(f"insert into infos values ('{tr[0]}','{tr[1]}','{tr[2]}','{tr[3]}')")
# db.execute("create table data (p0 real,p1 real,p2 real,p3 real,p4 real,p5 real,p6 real,p7 real,p8 real,p9 real,p10 real,p11 real,p12 real,p13 real,p14 real,p15 real,p16 real,p17 real,p18 real,p19 real,p20 real,p21 real,p22 real,p23 real,p24 real,p25 real,p26 real,p27 real,p28 real,p29 real,p30 real,p31 real,p32 real,p33 real,p34 real,p35 real,p36 real,p37 real,p38 real,p39 real,p40 real,p41 real,p42 real,p43 real,p44 real,p45 real,p46 real,p47 real,p48 real,p49 real,p50 real,p51 real,p52 real,p53 real,p54 real,p55 real,p56 real,p57 real,p58 real,p59 real,p60 real,p61 real,p62 real,p63 real,p64 real,p65 real,p66 real,p67 real,p68 real,p69 real,p70 real,p71 real,p72 real,p73 real,p74 real,p75 real,p76 real,p77 real,p78 real,p79 real,p80 real,p81 real,p82 real,p83 real,p84 real,p85 real,p86 real,p87 real,p88 real,p89 real,p90 real,p91 real,p92 real,p93 real,p94 real,p95 real,p96 real,p97 real,p98 real,p99 real,p100 real,p101 real,p102 real,p103 real,p104 real,p105 real,p106 real,p107 real,p108 real,p109 real,p110 real,p111 real,p112 real,p113 real,p114 real,p115 real,p116 real,p117 real,p118 real,p119 real,p120 real,p121 real,p122 real,p123 real,p124 real,p125 real,p126 real,p127 real)")

cr = db.cursor()
for a in list_known:
    cr.execute(f"insert into data values({a[0]},{a[1]},{a[2]},{a[3]},{a[4]},{a[5]},{a[6]},{a[7]},{a[8]},{a[9]},{a[10]},{a[11]},{a[12]},{a[13]},{a[14]},{a[15]},{a[16]},{a[17]},{a[18]},{a[19]},{a[20]},{a[21]},{a[22]},{a[23]},{a[24]},{a[25]},{a[26]},{a[27]},{a[28]},{a[29]},{a[30]},{a[31]},{a[32]},{a[33]},{a[34]},{a[35]},{a[36]},{a[37]},{a[38]},{a[39]},{a[40]},{a[41]},{a[42]},{a[43]},{a[44]},{a[45]},{a[46]},{a[47]},{a[48]},{a[49]},{a[50]},{a[51]},{a[52]},{a[53]},{a[54]},{a[55]},{a[56]},{a[57]},{a[58]},{a[59]},{a[60]},{a[61]},{a[62]},{a[63]},{a[64]},{a[65]},{a[66]},{a[67]},{a[68]},{a[69]},{a[70]},{a[71]},{a[72]},{a[73]},{a[74]},{a[75]},{a[76]},{a[77]},{a[78]},{a[79]},{a[80]},{a[81]},{a[82]},{a[83]},{a[84]},{a[85]},{a[86]},{a[87]},{a[88]},{a[89]},{a[90]},{a[91]},{a[92]},{a[93]},{a[94]},{a[95]},{a[96]},{a[97]},{a[98]},{a[99]},{a[100]},{a[101]},{a[102]},{a[103]},{a[104]},{a[105]},{a[106]},{a[107]},{a[108]},{a[109]},{a[110]},{a[111]},{a[112]},{a[113]},{a[114]},{a[115]},{a[116]},{a[117]},{a[118]},{a[119]},{a[120]},{a[121]},{a[122]},{a[123]},{a[124]},{a[125]},{a[126]},{a[127]})")
db.commit()
db.close()

print("End ! Add Successful ")