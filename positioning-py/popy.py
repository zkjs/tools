#-*- encoding=utf-8 -*-
#author: ganben

from socketIO_client import SocketIO
import logging
import math, random, time
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('__main__')

#below is the data auto generating section and simulated data
APs=[]

AP1 = { 'lnglat': [113.943814,22.529188],
        'id': 1
        }

AP2 = { 'lnglat': [113.94361,22.529163],
        'id': 2
        }

AP3 = { 'lnglat': [113.943637,22.529069],
        'id': 3
        }

APs.append(AP1)
APs.append(AP2)
APs.append(AP3)

ps = []



for i in range(20):
    #gen 20 lnglat points
    #lnglat = ap(i%3(which ap), i%2(lng or lat), dm = random (1-5)
    dm = 4 - random.randint(0, 7)
    ls = [[113.943814,22.529188], [113.94361,22.529163], [113.943637,22.529069]]
    lnglat = ls[i%3]
    lnglat[i%2] += float(180) * math.asin(float(dm)/6378000)/math.pi
    logger.info('new position {0}'.format(str(lnglat)))
    ps.append(lnglat)


    #scan = {'apid': , 'blid': , 'rssi': 35+drssi}

def drssi_dlnglat(p1, p2):
    dlng = p1[0] - p2[0]
    dlat = p1[1] - p2[1]
    dlnglat = math.sqrt(math.pow(dlng, 2) + math.pow(dlat, 2))
    # direct from dlnglat to drssi
    # 10m ~ 65 rssi linear,
    dm = 6378000.0 * dlnglat /180 * math.pi
    drssi = int(dm / 25.0 * 60)
    logger.info('dlnglat={0}, dm={1}, drssi={2}, p1={3}, p2={4}'.format(dlnglat, dm, drssi, str(p1), str(p2)))

    return drssi

def dlnglat_drssi(drssi):
    #reverse the  lnglat to drssi
    dm = drssi / 65 * 10
    dlnglat = dm * 180 /( math.pi * 6378000)
    logger.info('dm={0}, dlnglat={1}'.format(dm, dlnglat))
    return dlnglat

def solve_lnglat():
    #solve a equation which has defined three radius and centered, return a lnglat;

    return

def auto_generate():
    #
    #simulate the rssi respect to aps
    for i in ps:
        time.sleep(3)
        for ap in APs:
            drssi = drssi_dlnglat(i, ap.get('lnglat'))
            send('{0} {1} {2}'.format(ap.get('id'), '131', drssi))

        #we have 3 AP; lnglat = [113.943814,22.529188], [113.94361,22.529163], [113.943637,22.529069]
        #we have 1 bracelet: ID = 131, rssi strength f(0) = 35, f(10) = 99
        #let it be a linear projection
        #
        #so the simulated data for a route [[], [], [], [], []]
        #




def send(args):
    socketIO.emit('publish', {
        'topic': 'demo',
        'msg': args,
        'qos': 1
        })


def on_socket_connect_ack(args):
    print 'on_socket_connect_ack', args
    socketIO.emit('connect_v2', {'appkey': '58117375374bd76b1b5b690a', 'customid': 'python_demo'})

def on_connack(args):
    print 'on_connack', args
    socketIO.emit('subscribe', {'topic': 'demo'})

    print "publish2_to_alias"
    socketIO.emit('publish2_to_alias', {'alias': 'alias_mqttc_sub', 'msg': "hello to alias from publish2_to_alias"});

def on_puback(args):
    print 'on_puback', args
    if args['messageId'] == '11833652203486491112':
        print '  [OK] publish with given messageId'

def on_suback(args):
    print 'on_suback', args
    socketIO.emit('publish', {'topic': 'testtopic2', 'msg': 'from python', 'qos': 1})

    socketIO.emit('publish', {
        'topic': 'demo',
        'msg': 'string message1: sub succeed, loop started. . .',
        'qos': 1
        })

    socketIO.emit('set_alias', {'alias': 'mytestalias1'})
    auto_generate()

def on_message(args):
    print 'on_message', args
    #TODO: from msg to cached data and do positioning

def on_set_alias(args):
    print 'on_set_alias', args

    socketIO.emit('publish2', {
        'topic': 'testtopic2',
        'msg': 'from publish2',
        "opts": {
            'qos': 1,
            'apn_json':  {"aps":{"sound":"bingbong.aiff","badge": 3, "alert":"douban"}}
        }
    })


    socketIO.emit('get_alias')
    socketIO.emit('publish_to_alias', {'alias': 'mytestalias1', 'msg': "hello to alias"})
    socketIO.emit('get_topic_list', {'alias': 'mytestalias1'})
    socketIO.emit('get_state', {'alias': 'mytestalias1'})

def on_get_alias(args):
    print 'on_get_alias', args

def on_alias(args):
    socketIO.emit('get_alias_list', {'topic': 'testtopic2'})
    print 'on_alias', args

def on_get_topic_list_ack(args):
    print 'on_get_topic_list_ack', args

def on_get_alias_list_ack(args):
    print 'on_get_alias_list_ack', args

def on_publish2_ack(args):
    print 'on_publish2_ack', args
    if args['messageId'] == '11833652203486491113':
        print '  [OK] publish2 with given messageId'

def on_publish2_recvack(args):
    print 'on_publish2_recvack', args

def on_get_state_ack(args):
    print 'on_get_state_ack', args

socketIO = SocketIO('sock.yunba.io', 3000)
socketIO.on('socketconnectack', on_socket_connect_ack)
socketIO.on('connack', on_connack)
socketIO.on('puback', on_puback)
socketIO.on('suback', on_suback)
socketIO.on('message', on_message)
socketIO.on('set_alias_ack', on_set_alias)
socketIO.on('get_topic_list_ack', on_get_topic_list_ack)
socketIO.on('get_alias_list_ack', on_get_alias_list_ack)
socketIO.on('puback', on_publish2_ack)
socketIO.on('recvack', on_publish2_recvack)
socketIO.on('get_state_ack', on_get_state_ack)
socketIO.on('alias', on_alias)                # get alias callback

socketIO.wait()
