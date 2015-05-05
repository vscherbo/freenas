#!/usr/bin/env python2.7
# -*- coding: utf-8 -

import requests
import json

#fnas_api = 'http://fnas-alpha-adm.arc.world/api/v1.0'
fnas_api = 'http://192.168.1.57/api/v1.0'
#CIFS2move=['public', 'purchasing', 'system']
CIFS2move=['system']

conf = {}
execfile("./fo.conf", conf) # reading username, password


s = requests.Session()
s.auth = (conf['username'], conf['password'])
s.headers.update({'Content-Type': 'application/json'})
s.verify = False

"""
r = s.get(fnas_api + '/storage/volume/')

j = json.loads(r.text)
j.sort()

for vol in j:
    print vol["name"], vol["status"]
"""


def snapTask_create(volCIFS, interval, ret_unit):
    params = {
              "task_filesystem": volCIFS,
              "task_recursive": "false",
              "task_ret_unit": ret_unit,
              "task_interval": interval,
             }
    p = s.post(fnas_api + '/storage/task/' ,
               data=json.dumps(params),
               )

print p.status_code
print p.headers['content-type']
print p.headers['vary']                
print p.text



# Update Task 
"""
p = s.put(fnas_api + '/storage/task/2/' ,
                    data=json.dumps({
                            "task_interval": 30,
                    }),
                )
"""


    
"""
for task in j:
    for fs in CIFS2move:
        #print 'fs=', fs
        #print task['task_filesystem']
        #print task['task_filesystem'].count(fs)
        if #task['task_filesystem'].count(fs): 
            if task['task_enabled']:
                print task['task_filesystem'], task['id']
                p = s.post(
                    fnas_api + '/storage/task/' + str(task['id']) + '/' ,
                    #auth = (conf['username'], conf['password'])
                    #headers = {'Content-Type': 'application/json'},
                    data=json.dumps({
                      #'task_enabled': 'false'
                      "task_interval": 30
                    }),
                )
                print p.status_code
                print p.headers['content-type']
                print p.headers['vary']                
                print p.text

                #for k in task.keys():
                #    print u'   ' + k + u' -> ' + str(task[k])
"""


  
