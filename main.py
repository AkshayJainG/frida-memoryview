# -*- coding: utf-8 -*-
import logging
import frida,sys
from flask import Flask, jsonify, make_response, request, Response
import base64
import platform
import threading

app = Flask(__name__)
pf = platform.system()

nullfile = ""
if pf == 'Windows':
    nullfile = "nul"
elif pf == 'Darwin':
    nullfile = "/dev/null"
elif pf == 'Linux':
    nullfile = "/dev/null"

#Do not output unnecessary logs
l = logging.getLogger()
l.addHandler(logging.FileHandler(nullfile))

def log(message):
    app.logger.info(message)

#Returns the process name
@app.route('/init',methods=["GET"])
def init():
    return PACKAGE   

#Returns the address to be monitored
@app.route('/check',methods=["GET"])
def check():
    ret = api.check()
    if(ret==0):
        return "null"
    else:
        return str(ret)

#Forward on Intercept
@app.route('/forward',methods=["GET"])
def forward():
    ret = api.forward()
    return "null"

#Reads the memory and returns a byte data
@app.route('/readmem',methods=["POST"])
def readmem():
    json = request.get_json()
    ADDRESS = json["address"]
    SIZE = json["size"]
    ret = api.readmem(ADDRESS,SIZE)
    if(ret==False):
        return "error"
    else:
        return ret

#Write to memory
@app.route('/writemem',methods=["POST"])
def writemem():
    json = request.get_json()
    ADDRESS = json["address"]
    BUFFER = json["buffer"]
    ret = api.writemem(ADDRESS,BUFFER)
    return "null"

#For android
def get_device():
    mgr = frida.get_device_manager()
    changed = threading.Event()
    def on_changed():
        changed.set()
    mgr.on('changed', on_changed)
    
    device = None
    while device is None:
        devices = [dev for dev in mgr.enumerate_devices() if dev.type =='usb']
        if len(devices) == 0:
            print ('Waiting for usb device...')
            changed.wait()
        else:
            device = devices[0]
            
    mgr.off('changed', on_changed)
    return device

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs) 
    if argc != 2:
        print('Usage: # python %s processname' % argvs[0])

    #get processname
    PACKAGE = sys.argv[1]

    ###1.for windows,linux,mac###
    #session=frida.attach(PACKAGE)

    ###2.for android device###
    session = get_device().attach(PACKAGE)

    with open("memory.js") as f:
        jscode = f.read()

    script=session.create_script(jscode)

    def on_message(message ,data):
        print(message)

    script.on("message" , on_message)
    script.load()
    api = script.exports
    app.run(host='0.0.0.0', port = 5000,debug = False)