import os
import sys
import subprocess
import psutil
from time import sleep
from Adafruit_IO import MQTTClient

aio_key = os.environ['AIOKEY']
aio_user = os.environ['AIOUSER']
aio_mqtt = MQTTClient(aio_user, aio_key)
mqtt_feed_sub = 'fireplace'

def connected(client):
    print('Connected to AIO!  Listening for '+mqtt_feed_sub+' changes...')
    client.subscribe(mqtt_feed_sub)

def disconnected(client):
    print('Disconnected from AIO!')
    # mqtt_run()

def start_fireplace():
    # test that the video is not already running
    if "omxplayer" in (p.name() for p in psutil.process_iter()):
        print('Fireplace already on')
        return
    # start video
    print('Turning on fireplace')
    p = subprocess.Popen(["omxplayer","-o","local","/home/pi/videoloop/fireplace.mp4"])
    print('Fireplace is on')

def stop_fireplace():
    print('Turning off fireplace')
    p = subprocess.Popen(["killall","omxplayer.bin"])
    print('Fireplace is off')

def message(client, feed_id, payload, retain):
    print('Feed {feed} received new value: {message}'.format(feed=mqtt_feed_sub, message=payload))
    if payload == 'on':
        start_fireplace()
    elif payload == 'off':
        stop_fireplace()

def setup_mqtt():
    aio_mqtt.on_connect = connected
    aio_mqtt.on_disconnect = disconnected
    aio_mqtt.on_message = message

def mqtt_run():
    aio_mqtt.connect()
    for i in range(20):
        try:
            aio_mqtt.loop_blocking()
            break
        except:
            print('Error:', sys.exc_info()[0])
            print('Failed loop, waiting 5s...')
            sleep(5)
            continue

if __name__ == '__main__':
    setup_mqtt()
    mqtt_run()

