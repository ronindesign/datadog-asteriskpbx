#
# requires pyst2 for Asterisk Manager Interface
# https://github.com/rdegges/pyst2
#
# requires re for regular expression matching on asterisk output
#
#
# This is a python script that illustrates the output from Asterisk do not use with DataDog Agent
#
# update the host/user/secret variables below
#
# Usage : python asteriskpbx_sample.py
#

import asterisk.manager
import re

host    = "localhost"
port    = 5038
user    = "user"
secret  = "secret"


mgr = asterisk.manager.Manager()
mgr.connect(host,port)
mgr.login(user,secret)
call_volume = mgr.command('core show calls')

current_call_vol = call_volume.data.split('\n')

current_call_vol = current_call_vol[0].replace('active call','')
current_call_vol = current_call_vol.replace('s','')
current_call_vol = current_call_vol.replace(' ','')

print('Current Call Volume')
print(current_call_vol)

pri = mgr.command('pri show channels')

pri_channels = pri.data.split('\n')

pri_channels[0] = None
pri_channels[1] = None

openchannels = 0
for chan in pri_channels:
    if chan != None:
        chan_data = chan.split()
        if len(chan_data) > 2 and chan_data[3] == "No":
            openchannels += 1

print('Current in use PRI Channels')
print(openchannels)

sip_result = mgr.command('sip show peers')

sip_results = sip_result.data.split('\n')

siptotals = sip_results[len(sip_results)-3]

siptotal = re.findall(r'([0-9]+) sip peer',siptotals)[0]

monitored_peers = re.findall(r'Monitored: ([0-9]+) online, ([0-9]+) offline',siptotals)[0]
unmonitored_peers = re.findall(r'Unmonitored: ([0-9]+) online, ([0-9]+) offline',siptotals)[0]

print('Total SIP Peers')
print(siptotal)
print('Monitored SIP Peers online/offline')
print(monitored_peers)
print('Unmonitored SIP Peers online/offline')
print(unmonitored_peers)

iax_result = mgr.command('iax2 show peers')

iax_results = iax_result.data.split('\n')

iax_total_line = iax_results[len(iax_results)-3]

iax_peers_total = re.findall(r'([0-9]+) iax2 peers',iax_total_line)[0]
iax_peers_online = re.findall(r'\[([0-9]+) online',iax_total_line)[0]
iax_peers_offline = re.findall(r'([0-9]+) offline',iax_total_line)[0]
iax_peers_unmonitored = re.findall(r'([0-9]+) unmonitored',iax_total_line)[0]


print('Total IAX2 Peers')
print(iax_peers_total)
print('IAX2 Peers Online')
print(iax_peers_online)
print('IAX2 Peers Offline')
print(iax_peers_offline)
print('IAX2 Peers Unmonitored')
print(iax_peers_unmonitored)