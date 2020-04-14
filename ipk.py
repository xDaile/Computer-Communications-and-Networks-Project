#!/usr/bin/env python3

#   *-------------------------------------------*
#   | ######################################### |
#   | #   FIT VUT Brno 2019 IPK Project 1     # |
#   | #   Author: Michal Zelenák              # |
#   | ######################################### |
#   *-------------------------------------------*

import socket
import sys
import json


#Port for HTTP communication

port = 80


#argument from makefile (city)

city=sys.argv[2]


#Replacement of white spaces by the + for the link that we will encode and send, because white spaces cannot be in link

city.replace(" ","+")


#API key that user have to have, he can register it... read README

apiKey=sys.argv[1]


#The server from where we will collect data

HOST= "api.openweathermap.org"


#creating the string, of data that we will send later

send="GET /data/2.5/weather?q={}&APPID={}&units=metric HTTP/1.1\r\nHOST:api.openweathermap.org\r\n\r\n".format(city, apiKey)


#now the data we have, we must encode into bytes

bytes=send.encode()


#Trying to create socket,
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print ("socket creation failed with error %s" %(err))
    exit(2)


# Connecting to the server

try:
 s.connect((HOST, port))
except:
 print ("Cannot connect to ")
 print (HOST + " on port: " + str(port))
 exit(3)


#Sending our string encoded in bytes to the server
try:
 s.sendall(bytes)
except:
 print ("Failed sending data")
 exit(4)


#Answer from the server

try:
 bData=s.recv(2048)
except:
 print ("mistake during receiving data to ")
 exit(5)


#Now we can close our connection

s.close()


#Translating received bytes

sData=bData.decode("utf-8")

if sData.find("200 OK")== -1:
    print("Bad request, check the key, and city")
    exit(6)

#filtering data for json, first split the string to two, by the first '{'

match=sData.split("{",1)


#because of filtering, we must add back {

sData="{"+match[1]


#Loading data into json module

jsonData=json.loads(sData)


#Print Data that we collected in requested format
print()

#Name of the city
print(jsonData["name"])

#Short description of the weather
print(jsonData["weather"][0]["description"])

#Value of temperature
print("temp:{}°C" .format(jsonData["main"]["temp"]))

#Value of humidity of the air
print("humidity:{}%" .format(jsonData["main"]["humidity"]))

#Value of pressure of the air
print("preassure:{} hPa" .format(jsonData["main"]["pressure"]))

#value of the speed of wind
try:
    print("wind-speed: {} km/h" .format(jsonData["wind"]["speed"]))
except:
    print("Unavailable")

#value of the way of wind in degrees
try:
    print("wind-deg:",jsonData["wind"]["deg"])
except:
    print("Unavailable")
