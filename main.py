#!/usr/bin/python

import configparser
import json
import paho.mqtt.client as mqtt
import serial


def onMessage(client, userdata, message):
    print(client)
    print(userdata)
    print(message)


def main():
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Load serial commands from file
    commandsFile = open('commands.json', )
    commands = json.load(commandsFile)

    # Initialize serial
    tvSerial = serial.Serial(config.get('tv', 'serialPort'), config.get('tv', 'baudRate'))

    # Initialize MQTT
    client = mqtt.Client(config.get('mqtt', 'clientId'))
    client.username_pw_set(config.get('mqtt', 'username'), config.get('mqtt', 'password'))
    client.connect(config.get('mqtt', 'brokerIp'), int(config.get('mqtt', 'brokerPort')))
    client.subscribe("{}/command".format(config.get('mqtt', 'baseTopic')))
    client.on_message = onMessage
    client.loop_forever()


if __name__ == '__main__':
    main()
