#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=cp866

#;--------------------------------------- 
#; It Came Data 2 File
#;
#; Main Module
#; 01/03/21 - v1.5
#; + add prefix "0000_", save order information for pack data
#; + replace symbol "?" to "!0!"
#; 01/02/21 - v1.0
#; + unpack all resource data to folder
#; + compile exe version
#; + write special file aboute data "!!!res_namefile.txt"
#;---------------------------------------
#; (c) Pyhesty, 2021
#; special for old-games.ru
#;---------------------------------------


import numpy as np
import sys
import os

print("Resourse extract from game: It came from Desert")

#sys.arg[0] = 'PEOPLE'

if len (sys.argv) != 2:
    print("need name file resourse")
    print("format: exe name_resourse_it_came")
    input("Press Enter to continue...")
    sys.exit(0)

filename = sys.argv[1]

start_pos  = 0x00

namefile = '!!!res_'+filename + '.txt.';
f = open(namefile,'w',encoding='utf-8')

dt    = np.fromfile(filename,np.uint8)
#dt    = np.fromfile('PEOPLE',np.uint8)
#dt    = np.fromfile('insts',np.uint8)

def r16(pos):
    global dt
    return dt[pos+1]+dt[pos]*0x100

def r32(pos):
    global dt
    return dt[pos]*0x1000000+dt[pos+1]*0x10000+dt[pos+2]*0x100+dt[pos+3]

pos    = start_pos
Nstr   = r16(pos); pos +=2 

fname   = ['']*Nstr
fpos    = [0]*Nstr
fsz     = [0]*Nstr
fsz_d   = [0]*Nstr
dat_pre = []
ftype   = ['unknow']*Nstr

print("N data: ", Nstr)
print("N data: ", Nstr, file=f)

pos += 4
for n in range(Nstr):
    #pos += 1
    sname  = ""
    while dt[pos]!=0x00:
        ch = dt[pos]; pos+=1
        c  = str(ch,"utf-8")
        sname += c
    pos+=1
    data_pos = r32(pos); pos += 4
    fname[n] = sname.ljust(15)
    fpos[n] = data_pos
    fsz[n] = r32(pos); pos += 4

end_tbl = pos

for n in range(Nstr-1):
    fsz_d[n] = fpos[n+1]-fpos[n]

fsz_d[Nstr-1] = len(dt) - fpos[Nstr-1] - end_tbl;

for n in range(Nstr):
    ps = end_tbl + fpos[n]
    if chr(dt[ps])=='L' and chr(dt[ps+1])=='Z':
        ftype[n] ='LZ'
    if chr(dt[ps])=='S' and chr(dt[ps+1])=='M' and chr(dt[ps+2])=='S':
        ftype[n] ='SMS'
    if chr(dt[ps]=='M') and chr(dt[ps+1]=='o') and chr(dt[ps+2])=='v':
        ftype[n] ='Mov'



for n in range(Nstr):
    print(fname[n],":", format(fpos[n], "05X"),":", format(fsz[n], "06"),":",format(fsz_d[n], "06"),":",ftype[n])
    print(fname[n],":", format(fpos[n], "05X"),":", format(fsz[n], "06"),":",format(fsz_d[n], "06"),":",ftype[n], file=f)

f.close()

#for n in range(Nstr):
fdir = 'res_'+filename;
if not os.path.exists(fdir): os.makedirs(fdir)

n = 0
for n in range(Nstr):
    resdt = dt[end_tbl + fpos[n]:end_tbl + fpos[n] + fsz[n]]
    nm = fname[n] 
    prefix = str(n).zfill(4)
    nm = fdir + "\\"+prefix +"_"+ nm.replace("?","!0!")
    resdt.astype('uint8').tofile(nm)

sz_file = len(dt)
sz_data = np.sum(fsz)
sz_data_d = np.sum(fsz_d)
end_data = sz_data + end_tbl

print("size file: ", sz_file)
print("size data: ", sz_data)
print("size data d: ", sz_data_d)
print("end pos: ", end_data)
    
