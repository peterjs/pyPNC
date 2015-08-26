#!/usr/bin/python
# pyPNC, program na zalohovanie, branch ftps
import sys
import os
import zipfile
from time import gmtime, strftime
from ftplib import FTP_TLS 
meno=[]
ps=[]
my_list=[]
def chyba():
    print "Nezadal si vsetky potrebne parametre programu."
    print "Syntax: python pypnc.py cesta_k_zdroj_zlozke cesta_k_ciel_zlozke meno_suboru"
    print "cesta_k_zdroj_zlozke = cesta k zlozke ktora sa ma komprimovat \ncesta_k_ciel_zlozke = cesta k zlozke kam ma byt presunuty komprimovany subor \nmeno_suboru.zip = nazov pod ktorym sa komprimovany subor ulozi. Pripona .zip bude pridana automaticky.\n"

if len(sys.argv)<=3: #program vyzaduje 3 parametre
   chyba()
else:
    print "Cakajte prosim, program robi co moze. Naozaj sa snazi."
    odkial=sys.argv[1]
    kam=sys.argv[2]
    meno=sys.argv[3]
    source=odkial
    cas=strftime("_%Y-%m-%d_%H:%M:%S", gmtime())
    subor=meno+cas+".zip"
    zip=zipfile.ZipFile(subor, 'w',zipfile.ZIP_DEFLATED) # nezipuje velke subory (treba zip64 extension)!
    rootlen=len(source)+1
    for base,dirs,files in os.walk(source):
        for file in files:
            fn=os.path.join(base,file)
            souborek=zip.write(fn,fn[rootlen:])
            suborik=str(souborek)
    print "[OK]\nSubor sa nachadza v urcenom adresary",kam
    with open('/home/peter/pwd','r') as infile:
        data=infile.read()
    my_list=data.splitlines()
    meno=my_list[0]
    ps=my_list[1]
    path=my_list[2]
    server=my_list[3]
    ftp=FTP_TLS(server,meno,ps) 
    ftp.prot_p()
    ftp.cwd(my_list[2])
    ftp.retrlines("LIST")
    print "Posielam subor. Znova cakajte..."
    ftp.sendcmd("STOR suborik")
    ftp.close()
