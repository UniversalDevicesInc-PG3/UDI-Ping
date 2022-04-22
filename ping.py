#!/usr/bin/env python3
"""
This is a NodeServer was created using template for Polyglot v2 written in Python2/3
by Einstein.42 (James Milne) milne.james@gmail.com
v1.0.15
"""
import udi_interface
import sys
import time
import os
import struct
import array
import fcntl
import subprocess
import logging

LOGGER = udi_interface.LOGGER
logging.getLogger('urllib3').setLevel(logging.ERROR)

class Controller(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name):
        super(Controller, self).__init__(polyglot, primary, address, name)
        self.name = 'Ping'
        self.poly = polyglot
        self.firstCycle = True

        polyglot.subscribe(polyglot.START, self.start, address)
        polyglot.subscribe(polyglot.CUSTOMPARAMS, self.parameterHandler)
        polyglot.subscribe(polyglot.POLL, self.poll)

        polyglot.ready()
        polyglot.addNode(self)

    def parameterHandler(self, params):
        for key,val in params.items():
            _netip = val.replace('.','')
            if _netip[:3] == "www":
                netip = _netip[3:17]
            else:
                netip = _netip[:14]
            _key = key[:20]

            if self.poly.getNode(netip) is None:
                self.poly.addNode(hostnode(self.poly, self.address, netip, val, _key))
            else:
                LOGGER.info('Found existing node, do we need to update val and _key?')
                self.poly.getNode(netip).ip = val
                self.poly.getNode(netip).name = _key

    def start(self):
        LOGGER.info('Started Ping')
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()

    def poll(self, polltype):
        if 'shortPoll' in polltype:
            result = self.checkwlan0()        
            for node in self.poly.nodes():
                if node.address != self.address:
                    node.update()

    def query(self):
        self.reportDrivers()
        for node in self.poly.nodes():
            node.reportDrivers()

    def checkwlan0(self):
        response,result = subprocess.getstatusoutput("ifconfig wlan0 | grep UP")
        LOGGER.debug("checkwlan0 %s" ,response)
        return response

    def delete(self):
        LOGGER.info('Deleting Ping NodeServer.')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')


    id = 'controller'
    commands = {
        'QUERY': query
    }
    drivers = [{'driver': 'ST', 'value': 1, 'uom': 2}]

class Ping(object):

    def __init__(self, ip, timeout):
        self.ip = ip
        self.timeout = timeout

    def ping(self):
        response = 0
        try:
            response,result = subprocess.getstatusoutput("ping -c1 -W " + str(self.timeout-1) + " " + self.ip)
            LOGGER.debug("RPi %s " ,response)
            if response == 0:
                return response
        except Exception as e:
            LOGGER.error('Error %s ',e)
            return None
        if response == 127:
            try:
                response = subprocess.call(['/sbin/ping','-c1','-t' + str(self.timeout-1), self.ip], shell=False)
                LOGGER.debug("Polisy %s " ,response)
                if response == 0:
                    return response
            except Exception as e:
                LOGGER.error('Error %s ',e)
                return None
        else:
            return None

class hostnode(udi_interface.Node):
    def __init__(self, controller, primary, address, ipaddress, name):
        super(hostnode, self).__init__(controller, primary, address, name)
        self.ip = ipaddress
        self.scan = 1
        self.missed = 0
        self.timeout = 60

        controller.subscribe(controller.START, self.start, address)
        controller.subscribe(controller.CONFIG, self.cfgHandler)

    def cfgHandler(self, cfg):
        if 'shortPoll' in cfg:
            LOGGER.info('Setting ping timeout to {} seconds'.format(cfg['shortPoll']))
            self.timeout = int(cfg['shortPoll'])

    def start(self):
        self.setOn('DON')
        self.reportDrivers()

    def update(self):
        if (self.scan):
            netstat = Ping(ip=self.ip,timeout=self.timeout)
            result = netstat.ping()

            if (result != None):
                self.missed = 0
                self.setOnNetwork(0)
                LOGGER.debug(self.ip + ': On Network')
            elif (self.missed >= 5):
                self.setOffNetwork()
                if self.missed < 1440: self.missed += 1
                LOGGER.debug(self.ip + ': Off Network')
            elif self.missed >= 0 and self.missed < 5:
                self.missed += 1
                self.setInFault(self.missed)
                LOGGER.debug(self.ip + ': In Fault')


    def setOnNetwork(self,missed):
        self.setDriver('ST', 0)
        self.setDriver('GV0', self.missed)

    def setInFault(self, missed):
        self.setDriver('ST', 1)
        self.setDriver('GV0', self.missed)

    def setOffNetwork(self):
        self.setDriver('ST', 2)
        self.setDriver('GV0', self.missed)

    def setOn(self, command):
        self.missed = 0
        self.setOnNetwork(self.missed)
        self.setDriver('GV1',1)
        self.scan = 1

    def setOff(self, command):
        self.missed = 0
        self.setOffNetwork()
        self.setDriver('GV0', 0)
        self.setDriver('GV1', 0)
        self.scan = 0

    def query(self):
        self.reportDrivers()


    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 25},
        {'driver': 'GV0', 'value': 0, 'uom': 56},
        {'driver': 'GV1', 'value': 1, 'uom': 2}
    ]

    id = 'hostnode'

    commands = {
                    'DON': setOn, 'DOF': setOff, 'QUERY': query
                }
if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([])
        polyglot.start('2.0.0')
        Controller(polyglot, 'controller', 'controller', 'PingNodeServer')
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)

