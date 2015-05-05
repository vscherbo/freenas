#!/usr/bin/env python2.7
# -*- coding: utf-8 -
from __future__ import print_function

import sys
from freenas import fnas
from datetime import (date, time, datetime, timedelta)

# TODO command line options: conf file, order's status file
conf = {}
execfile("./fo.conf", conf) # reading username, password


#CIFS2move=['public', 'purchasing', 'system']
CIFS2move=['system']

# fnas_from = fnas('http://192.168.1.57/api/v1.0', (conf['username'], conf['password']))
fnas_from = fnas('http://fnas-alpha-adm.arc.world/api/v1.0', (conf['username'], conf['password']))
#fnas_to = fnas('http://192.168.1.57/api/v1.0')

#fnas_from.PrintList('/storage/volume', ['name', 'vol_fstype', 'status'])
#fnas_from.PrintList('/sharing/cifs/', [ 'cifs_name', 'cifs_path'])
fnas_from.PrintList('/storage/snapshot/', [ 'filesystem', 'id' ] )
#fnas_from.PrintList('/storage/replication', ['repl_filesystem', 'repl_remote_hostname', 'repl_zfs'])
sys.exit()

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

#fnas_from.CIFS_switch2replica('public')
#fnas_from.CIFS_switch2master('public')
#print(fnas_from.CIFSbyName('public') )

#print(fnas_from.ReplTask_List('test'))

#task = fnas_from.ReplTask_Get('fnas-beta.arc.world', 'test')
#task["repl_enabled"] = False
#fnas_from.ReplTask_Update('fnas-beta.arc.world', 'test', task)

snapDelay = timedelta(minutes=5)

(task_id, snapNextTime) = fnas_from.SnapTask_GetNextRun('public') 
print("task_id=", task_id)
print("next=", datetime.combine(datetime.today(), snapNextTime))
print("now=", datetime.now())
print("delta=", datetime.combine(datetime.today(), snapNextTime) - datetime.now())
print("delay=", snapDelay)

if ( ( datetime.combine(datetime.today(), snapNextTime) - datetime.now() ) > snapDelay ):
    print("Too late")
    print("new_next=", (datetime.now() + timedelta(minutes=7)).strftime('%H:%M:%S') )
#    params["task_filesystem"] = fnas_from.CIFS_getVolName('public')  #"vol01/ds_cifs/test"
#    params["task_begin"] = datetime.now().strftime('%H:%M:%S')
#    params["task_end"] = (datetime.now() + timedelta(minutes=7)).strftime('%H:%M:%S')
#    params["task_interval"] = 5
#    params["task_enabled"] = True
    
#    params = fnas_from.def_task_params
#    params["task_filesystem"] = fnas_from.CIFS_getVolName('public')  #"vol01/ds_cifs/test"
#    fnas_from.SnapTask_Update(task_id,params)



