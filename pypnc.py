#!/usr/bin/python
# pyPNC, program na zalohovanie, branch ftps
import sys
import os
import zipfile
from time import gmtime, strftime
from ftplib import FTP_TLS 
import fnmatch

meno=[]
ps=[]
my_list=[]
file_to_zip=""
cas=""
#velkost_ftp="1234" #test
velkost_ftp=""
velkost_local=""
reconnect=0
max_recon=1 

def nazov(timestamp_arg): 
    if timestamp_arg == "time":
        cas=strftime("_%Y-%m-%d_%H:%M:%S", gmtime()) 
    elif timestamp_arg == "notime":
        cas=""
    else:
        chyba()
    return cas

def chyba():
    print "Nezadali ste vsetky potrebne parametre programu."
    print "Syntax: python pypnc.py cesta_k_zdroj_zlozke cesta_k_ciel_zlozke meno_suboru timestamp (time pre ulozenie casu do mena suboru, notime pre vynechanie timestampu)"
    print "cesta_k_zdroj_zlozke = cesta k zlozke ktora sa ma komprimovat \ncesta_k_ciel_zlozke = cesta k zlozke kam ma byt presunuty komprimovany subor \nmeno_suboru.zip = nazov pod ktorym sa komprimovany subor ulozi. Pripona .zip bude pridana automaticky.\n"
    sys.exit()

def connect(velkost_ftp):
    ftp=FTP_TLS(server,meno2,ps)   
    ftp.prot_p()
    ftp.cwd(my_list[2]) 
    ftp.retrlines("LIST")
    print "Posielam subor. Cakajte prosim."
    ftp.storbinary('STOR '+file_to_send, open(file_to_send, 'rb'),)
    print "Subor odoslany [OK]"
    size_ftp=ftp.nlst()
    velkost_ftp_subor=size_ftp[0] #berie len prvy subor zo zoznamu
    ftp.sendcmd("TYPE i")
    velkost_ftp=ftp.size(velkost_ftp_subor) #test
    ftp.close()
    return velkost_ftp

def resend(reconnect,max_recon):
    print "Velkosti suborov sa lisia, pravdepodobne doslo k chybe.\nOpakujem posielanie suboru."
    while reconnect <= max_recon :
          reconnect=reconnect+1
          connect(velkost_ftp)
    print "Subor bol preposlany. Zistujem ci sa napravila chyba."
    if velkost_local!=connect(velkost_ftp):
       print "Chybu sa nepodarilo odstranit, skontrolujte subory manualne."

def check_file_size(velkost_local):
    if velkost_local!=connect(velkost_ftp):
        resend(reconnect,max_recon)
    else :
        print "Meno a velkost preneseneho suboru sa zhoduju. [OK]"
    sys.exit()

if len(sys.argv)<=3: #program vyzaduje 3 parametre
   chyba()
else:
    print "Cakajte prosim, program vytvara .zip subor. V zavislosti od velkosti to moze trvat niekolko minut." 
    odkial=sys.argv[1]
    kam=sys.argv[2]
    meno=sys.argv[3]
    timestamp_arg=sys.argv[4]
    source=odkial
    subor=meno+nazov(timestamp_arg)+".zip" 
    zip=zipfile.ZipFile(subor, 'w',zipfile.ZIP_DEFLATED,"allowZip64=True") 
    rootlen=len(source)+1
    for base,dirs,files in os.walk(source):
        for file in files:
            fn=os.path.join(base,file)
            file_to_zip=zip.write(fn,fn[rootlen:]) 
    print "Subor sa nachadza v urcenom adresary",kam,"[OK]"
    with open('/home/peter/pwd','r') as infile:
        data=infile.read()
    my_list=data.splitlines()
    meno2=my_list[0]
    ps=my_list[1]
    path=my_list[2]
    server=my_list[3]
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,"*.zip"):
            file_to_send=str(file) 
    velkost_local=os.path.getsize(file_to_send)
    check_file_size(velkost_local)
    connect(velkost_ftp)
