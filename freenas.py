#!/usr/bin/env python2.7
# -*- coding: utf-8 -
from __future__ import print_function

import requests
import json
from datetime import (date, datetime, timedelta)

class fnas(object):
    def_task_params = {
        "task_ret_count": 4,
        "task_repeat_unit": "weekly",
        "task_enabled": False,
        "task_recursive": False,
        "task_end": "20:00:00",
        "task_interval": 120,
        "task_byweekday": "1,2,3,4,5",
        "task_begin": "09:00:00",
        "task_filesystem": "",
        #"id": 1,
        "task_ret_unit": "day"
    }
    def __init__(self, url, auth): #===========================
        self.fnas_api = url
        self.sess = requests.Session()
        self.sess.auth = auth 
        self.sess.headers.update({'Content-Type': 'application/json'})
        self.sess.verify = False
    def run(self, cmd, subj, data=None): #===========================
        self.url = self.fnas_api + subj
        if cmd.upper() not in ['GET', 'POST', 'PUT', 'DELETE']:
            raise Exception("wrong cmd=" + cmd)
        req = requests.Request(cmd.upper(), self.url, data=data)
        prepped = self.sess.prepare_request(req)
        r = self.sess.send(prepped)
        self.status_code = r.status_code
        self.headers = r.headers   #['content-type'] ['vary']
        self.text = r.text
        if 'DELETE' != cmd.upper() and 'POST' != cmd.upper():
            self.j = json.loads(self.text)
            
    def PrintList(self, subj, field_list): #===========================
        self.run('get', subj)
        if 200 != self.status_code:
            raise Exception("Error while get "+subj +", status=" + str(self.status_code) )
        else:
            print(u' '.join(field_list) )
            for item in self.j:
                print(u' '.join([ item[f] for f in field_list
                                 ]))
                
    def CIFS_getVolName(self, CIFSname): #===========================
        r = self.run('get', '/sharing/cifs/')
        return next((fs["cifs_path"].replace('/mnt/', '') for fs in self.j if fs["cifs_name"].lower() == CIFSname.lower()), None)

    def SnapTask_Create(self, task_params): #===========================
        "create snapshot Task with task_params"
        self.run('post', '/storage/task/',
                        data=json.dumps(task_params) 
                      )     
        if 201 != self.status_code:
            raise Exception("Error in SnapTask_Create params="+task_params +", status=" + str(self.status_code) )
    
    def SnapTask_List(self, volCIFS): #===========================
        "return list of snapshot Tasks for volCIFS"
        self.run('get', '/storage/task/',
                      )   
        if 200 != self.status_code:
            raise Exception("Error in SnapTask_List vol="+ volCIFS +", status=" + str(self.status_code) )
        return [task for task in self.j if task["task_filesystem"] == self.CIFS_getVolName(volCIFS)]

    def SnapTask_Delete(self, task_id): #===========================
        "delete Task with task_id"
        self.run('delete', '/storage/task/'+str(task_id)+'/',
                      )   
        if 204 != self.status_code:
            raise Exception("Error in SnapTask_Delete task_id" +task_id+ ", status=" + str(self.status_code) )

    def SnapTask_Update(self, task_id, task_params): #===========================
        "update Task with task_id set task_params"
        self.run('put', '/storage/task/'+str(task_id)+'/',
                        data=json.dumps(task_params)
                      )   
        if 200 != self.status_code:
            raise Exception("Error in SnapTask_Update task_id"+task_id +", status=" + str(self.status_code) )

    def SnapTask_dtrange(self, task): #===========================
        from_date = datetime.strptime(task["task_begin"],'%H:%M:%S')
        to_date = datetime.strptime(task["task_end"],'%H:%M:%S')
        while from_date < to_date:
            yield from_date
            from_date = from_date + timedelta(minutes=task["task_interval"])
            
    def SnapTask_GetNextRun(self, fs): #===========================
        "TODO"
        self.run('get', '/storage/task/',
                      )
        if 200 != self.status_code:
            raise Exception("Error in SnapTask_GetNextRun fs="+fs +", status=" + str(self.status_code) )
        
        task = (t_item for t_item in self.j if t_item["task_filesystem"] == self.CIFS_getVolName(fs)).next()
        #? is task enabled
        if task["task_enabled"]:
            #? isoweekday(today) in task_byweekday
            if date.isoweekday(date.today()) in [int(s) for s in task["task_byweekday"].split(',')]:
                #? now() BETWEEN (task_begin+N*task_interval AND task_end)
                return task["id"], [snap_t.time() for snap_t in self.SnapTask_dtrange(task) if snap_t.time() > datetime.now().time()][0]

        

    def CIFSbyName(self, CIFSname): #===========================
        "return CIFS "
        self.run('get', '/sharing/cifs/',
                      )   
        if 200 != self.status_code:
            raise Exception("Error in CIFSbyName "+CIFSName +", status=" + str(self.status_code) )
        return (fs for fs in self.j if fs["cifs_name"].lower() == CIFSname.lower()).next()

    def CIFS_Update(self, cifs_id, cifs_params): #===========================
        "update Task with task_id set task_params"
        self.run('put', '/sharing/cifs/'+str(cifs_id)+'/',
                        data=json.dumps(cifs_params)
                      )   
        if 200 != self.status_code:
            raise Exception("Error in CIFS_Update id="+cifs_id +", status=" + str(self.status_code) )

    def CIFS_switch2replica(self, CIFSname): #===========================
        "set 'readonly' and add 'replica' to comment of CIFS share"
        fs = self.CIFSbyName(CIFSname)
        fs["cifs_ro"] = True
        
        if None == fs["cifs_comment"]:
            fs["cifs_comment"] = 'replica'
        elif fs["cifs_comment"].startswith(u'replica'):
            pass
        else:
            fs["cifs_comment"] = 'replica' + ' ' + fs["cifs_comment"]
        self.CIFS_Update(fs["id"], fs)

    def CIFS_switch2master(self, CIFSname): #===========================
        "set 'readwrite' and remove 'replica' from comment of CIFS share"
        fs = self.CIFSbyName(CIFSname)
        fs["cifs_ro"] = False
        
        if fs["cifs_comment"].startswith('replica'):
            fs["cifs_comment"] = fs["cifs_comment"].replace('replica', '').strip()
            #print("_"+fs["cifs_comment"]+"_")
        self.CIFS_Update(fs["id"], fs)

    def ReplTask_List(self, volCIFS): #===========================
        "return replication Task for volCIFS"
        self.run('get', '/storage/replication/')   
        if 200 != self.status_code:
            raise Exception("Error in ReplTask_List vol="+volCIFS +", status=" + str(self.status_code) )
        return [task for task in self.j if task["repl_filesystem"] == self.CIFS_getVolName(volCIFS)]

    def ReplTask_Get(self, fnas_to, volCIFS): #===========================
        "return replication Task to fnas_to for volCIFS"
        self.run('get', '/storage/replication/')   
        if 200 != self.status_code:
            raise Exception("Error in ReplTask_Get, status=" + str(self.status_code) )
        return (task for task in self.j if task["repl_filesystem"] == self.CIFS_getVolName(volCIFS) and task["repl_remote_hostname"] == fnas_to).next()

    def ReplTask_Update(self, fnas_to, volCIFS, repl_params): #===========================
        "update replication Task to fnas_to for volCIFS"
        task = self.ReplTask_Get(fnas_to, volCIFS)

        self.run('put', '/storage/replication/' + str(task["id"]) + '/',
                        data=json.dumps(repl_params)
                      )   
        if 200 != self.status_code:
            raise Exception("Error in ReplTask_Update, status=" + str(self.status_code) + ', text=' + self.text \
                            + ', url=' + self.url)

    def Snapshots_List(self, vol): #===========================
        "return replication Task to fnas_to for volCIFS"
        self.run('get', '/storage/replication/')   
        if 200 != self.status_code:
            raise Exception("Error in ReplTask_Get, status=" + str(self.status_code) )
        return (task for task in self.j if task["repl_filesystem"] == self.CIFS_getVolName(volCIFS) and task["repl_remote_hostname"] == fnas_to).next()


##################################################
# Main
if __name__ == '__main__':
    pass
else:
    pass

