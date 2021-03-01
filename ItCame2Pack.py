#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=cp866

#;--------------------------------------- 
#; It Came Data Forder files 2 Pack
#;
#; Main Module
#; 01/03/21 - v1.0
#; + pack resource from folder name "res_FILENAME" to FILENAME 
#; + replace symbol "!0!" to "?"
#;---------------------------------------
#; (c) Pyhesty, 2021
#; special for old-games.ru
#;---------------------------------------

import numpy as np
import sys, os
from os import listdir
from os.path import isfile, join

print("Resourse pack data for  Game: It came from Desert from folder with files ")
print("Prefix folder with data: 'res_', example: 'res_PEOPLE' for resourse 'PEOPLE'")

#sys.arg[0] = 'PEOPLE'

if len (sys.argv) != 2:
    print("need name file resourse")
    print("format: exe name_resourse_it_came")
    input("Press Enter to continue...")
    sys.exit(0)

filename = sys.argv[1]

def w16(pos, data):
    global dt
    dt[pos]   = data//0x100;
    dt[pos+1] = data%0x100;
    return 

def w2str(pos, str):
    global dt
    u = str.encode(); # unicode(str, "utf-8")
    for n in range(len(u)):
        dt[pos+n] = u[n]
    return 

def w32(pos, data):
    global dt
    dt[pos]   = data//0x1000000;
    dt[pos+1] = (data%0x1000000)//0x10000;
    dt[pos+2] = (data%0x10000)//0x100;
    dt[pos+3] = data%0x100;
    return 

def r16(pos):
    global dt
    return dt[pos+1]+dt[pos]*0x100

def r32(pos):
    global dt
    return dt[pos]*0x1000000+dt[pos+1]*0x10000+dt[pos+2]*0x100+dt[pos+3]


fdir = 'res_'+filename;
if not os.path.exists(fdir):
    print("not found folder with resource file: ", fdir)
    input("Press Enter to continue...")
    sys.exit(0)  

allfiles = [f for f in listdir(fdir) if isfile(join(fdir, f))]

print("all file in folder ", fdir," with size :")
fullsize = 6                       #  how many resource for people 0x00EE + size header 
headsize = 0
for n in range(len(allfiles)):
    file = allfiles[n]
    ph = fdir + "\\" + file
    sz = os.stat(ph).st_size
    file = file.replace("!0!","?")
    ph   = ph.replace("!0!","?")
    print(ph, ":", sz)
    if file[4] != '_':
        print("problem file name resource: ", file)
    fullsize += sz + len(file) - 5 + 8 + 1 # 5 - prefix 0000, 8 - two pointer, 1 zero str 0x00 after file name_ 
    headsize += len(file) -5 + 8 + 1

print("calc pack size:  ", fullsize)
print("calc head size:  ", headsize)

dt = np.zeros(fullsize);

w16(0x00, len(allfiles))
w32(0x02,      headsize)

curpos    = 0x06
curoffset = 0x00
for n in range(len(allfiles)):
    file = allfiles[n]
    ph = fdir + "\\" + file
    sz = os.stat(ph).st_size    
    file_no_prefix = file[5:]
    file_no_prefix = file_no_prefix.replace("!0!","?")
    w2str(curpos, file_no_prefix);
    curpos += len(file_no_prefix) + 1
    w32(curpos,curoffset) 
    curoffset += sz
    curpos += 4
    w32(curpos,sz) 
    curpos += 4

for n in range(len(allfiles)):
    file = allfiles[n]
    ph = fdir + "\\" + file
    dtfile = np.fromfile(ph,np.uint8)
    sz = len(dtfile)
    dt[curpos:curpos+sz] = dtfile[:]
    curpos += sz

dt.astype('uint8').tofile(filename)

print("pack data complite in file : ", filename )
