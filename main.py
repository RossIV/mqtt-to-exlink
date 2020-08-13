#!/usr/bin/python

import configparser
import paho.mqtt.client as mqtt
import serial
import ast

tvSerial = None
commands = None


def onMessage(client, userdata, message):
    decodedMessage = message.payload.decode("utf-8")
    if decodedMessage in commands:
        tvSerial.write(commands[decodedMessage].encode('latin1'))


def main():
    global tvSerial, commands
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Load serial commands from file
    commandsFile = open('commands.txt', )
    file = open("commands.txt", "r")
    contents = file.read()
    commands = ast.literal_eval(contents)
    file.close()

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
