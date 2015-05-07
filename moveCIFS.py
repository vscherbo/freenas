#!/usr/bin/env python2.7
# -*- coding: utf-8 -
from __future__ import print_function

from freenas import fnas
from datetime import (date, time, datetime, timedelta)

##################################################
# Main

# CIFS2move=[ 'buhgalteriya']
# CIFS2move=[ 'purchasing', 'wpkg', 'assistants', 'distrib', 'public']
CIFS2move=['distrib']
# CIFS2move=['design']
# CIFS2move=['automatix', 'bosses', 'delivery', 'FT_Delivery', 'ForeignTrade', 'public', 'sales', 'home', 'arcmail']

# TODO command line options: conf file, order's status file
conf = {}
execfile("./fo.conf", conf) # reading username, password

api_str = '/api/v1.0'
fnas_from_name = 'http://fnas-beta-adm.arc.world'
fnas_from = fnas(fnas_from_name, api_str, (conf['username'], conf['password']))
fnas_to_name = 'http://fnas-alpha-adm.arc.world'
fnas_to = fnas(fnas_to_name, api_str, (conf['username'], conf['password']))

for fs in CIFS2move:
# FROM
    print('CIFS_switch2replica(' + fs + ')')
    fnas_from.CIFS_switch2replica(fs)
    print("done")
    for t in fnas_from.SnapTask_List(fs):
        t["task_enabled"] = False
        print(fnas_from.fnas_name + ': disable SnapTask for vol:' + t["task_filesystem"])
        fnas_from.SnapTask_Update(t["id"], t)
        print('done')
    RTList = fnas_from.ReplTask_List(fs)
    for rt in RTList:
        rem_host = rt['repl_remote_hostname']
        # print(rem_host)
        task = fnas_from.ReplTask_Get(rem_host, fs)
        task["repl_enabled"] = False
        print('Disable ReplTask to ' + rem_host)
        fnas_from.ReplTask_Update(rem_host, fs, task)
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

