#!/usr/bin/env python2.7
# -*- coding: utf-8 -
from __future__ import print_function

from freenas import fnas
from datetime import (date, time, datetime, timedelta)

##################################################
# Main

#CIFS2move=[ 'buhgalteriya']
CIFS2move=[ 'purchasing', 'wpkg', 'assistants', 'distrib', 'public']
#CIFS2move=['wpkg']
#CIFS2move=['design']
#CIFS2move=['automatix', 'bosses', 'delivery', 'FT_Delivery', 'ForeignTrade', 'public', 'sales', 'home', 'arcmail']

#fnas_from = fnas('http://192.168.1.57/api/v1.0')
#fnas_to = fnas('http://192.168.1.57/api/v1.0')
fnas_from_name = 'http://fnas-beta-adm.arc.world'
fnas_from = fnas(fnas_from_name + '/api/v1.0')
fnas_to_name = 'http://fnas-alpha-adm.arc.world'
fnas_to = fnas(fnas_to_name + '/api/v1.0')

#fnas_from.PrintList('/storage/volume', ['name', 'vol_fstype', 'status'])
#fnas_from.PrintList('/sharing/cifs/', [ 'cifs_name', 'cifs_path'])
#fnas_from.PrintList('/storage/replication', ['repl_filesystem', 'repl_remote_hostname', 'repl_zfs'])

params = fnas_from.def_task_params
params["task_filesystem"] = fnas_from.CIFS_getVolName('test')  #"vol01/ds_cifs/test"
#fnas_from.SnapTask_Create(params)

#for t in fnas_from.SnapTask_List('public'):
#    print(t["id"])
    #t["task_enabled"] = False
    #fnas_from.SnapTask_Update(t["id"], t)
    #fnas_from.SnapTask_Delete(t["id"])

#print(fnas_from.SnapTask_List('public1'))
#print(fnas_from.CIFS_getVolName('test'))

for fs in CIFS2move:
# FROM
    print('CIFS_switch2replica(' + fs + ')')
    fnas_from.CIFS_switch2replica(fs)
    print("done")
    for t in fnas_from.SnapTask_List(fs):
        t["task_enabled"] = False
        print('SnapTask_disabled')
        fnas_from.SnapTask_Update(t["id"], t)
        print('done')
    task = fnas_from.ReplTask_Get(fnas_from_name, fs)
    task["repl_enabled"] = False
    print('ReplTask_disabled')
    fnas_from.ReplTask_Update(fnas_from_name, fs, task)
    print("done")
# TO
    print('CIFS_switch2master(' + fs + ')')
    fnas_to.CIFS_switch2master(fs)
    print("done")
    for t in fnas_to.SnapTask_List(fs):
        t["task_enabled"] = True
        print('SnapTask_enabled')
        fnas_to.SnapTask_Update(t["id"], t)
        print("done")



#fnas_from.CIFS_switch2master('public')
#print(fnas_from.CIFSbyName('public') )

#print(fnas_from.ReplTask_List('test'))

#task = fnas_from.ReplTask_Get('fnas-beta.arc.world', 'test')
#task["repl_enabled"] = False
#fnas_from.ReplTask_Update('fnas-beta.arc.world', 'test', task)
