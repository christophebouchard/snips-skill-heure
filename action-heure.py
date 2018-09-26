#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from hermes_python.hermes import Hermes
from datetime import datetime
from pytz import timezone
import requests

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

def verbalise_air_quality(aqi):
	if aqi >= 80:
		return 'bonne'
	elif aqi >= 60:
		return 'moyenne'
	else:
		return 'mauvaise'

def intent_received(hermes, intent_message):

	print()
	print('start debug')
	
	city = intent_message.slots.city.first().value
	print(city)
	responseApiXy = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+city+'&key=AIzaSyAXJ589rS7Lpp7pUFHww59qxwOcD5kMeoM')
	print(responseApiXy)
	print(responseApiXy.content)
	dataApiXy = responseApiXy.json()
	print(dataApiXy)
	lat = dataApiXy['results'][-1]['geometry']['location']['lat']
	print(lat)
	lng = dataApiXy['results'][-1]['geometry']['location']['lng']
	print(lng)
	headers = {'accept': 'application/json', 'authorization': 'Basic anVub246UlFXSnVub25YcG0yWA=='}
	#response = requests.get('https://junon---develop-sr3snxi-ma2sa5nwhuqdk.fr-1.platformsh.site/v1/air/quality?lat=12.971599&lon=77.594563', headers=headers)
	url = 'https://junon---develop-sr3snxi-ma2sa5nwhuqdk.fr-1.platformsh.site/v1/air/quality?lat='+lat+'&lon='+lng+'
	print(url)
	response = requests.get('https://junon---develop-sr3snxi-ma2sa5nwhuqdk.fr-1.platformsh.site/v1/air/quality?lat=12.971599&lon=77.594563', headers=headers)
	print(response)
	print(response.content)
	data = response.json()
	print(data)
	aqi = data['breezometer_aqi']
	print(aqi)
	quality_word = 'mauvaise'
	if aqi >= 80:
	  quality_word = 'bonne'
	elif aqi >= 60:
	  quality_word = 'moyenne'

	print(quality_word)
	print(intent_message.intent.intent_name)
	print()

	if "askTime" in intent_message.intent.intent_name:
		
		sentence = "La qualitai de l'air a "+ city +" est "
		print(intent_message.intent.intent_name)
		
		sentence += verbalise_air_quality(aqi)
		print(sentence)
		hermes.publish_end_session(intent_message.session_id, sentence)
		
	elif "cityForAirQuality" in intent_message.intent.intent_name:
	#elif intent_message.intent.intent_name == 'Joseph:cityForAirQuality':
		sentence = "La qualitai de l'air a "+ city +" est "
		print(intent_message.intent.intent_name)
		
		sentence += verbalise_air_quality(aqi)
		print(sentence)
		hermes.publish_end_session(intent_message.session_id, sentence)
		
	elif "greetings" in intent_message.intent.intent_name:
	#elif intent_message.intent.intent_name == 'Joseph:greetings':

		hermes.publish_end_session(intent_message.session_id, "De rien!")


with Hermes(MQTT_ADDR) as h:
	h.subscribe_intents(intent_received).start()
