#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from hermes_python.hermes import Hermes
from datetime import datetime
from pytz import timezone
import requests

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


def verbalise_hour(i):
	if i == 0:
		return "minuit"
	elif i == 1:
		return "une heure"
	elif i == 12:
		return "midi"
	elif i == 21:
		return "vingt et une heures"
	else:
		return "{0} heures".format(str(i)) 

def verbalise_minute(i):
	if i == 0:
		return ""
	elif i == 1:
		return "une"
	elif i == 21:
		return "vingt et une"
	elif i == 31:
		return "trente et une"
	elif i == 41:
		return "quarante et une"
	elif i == 51:
		return "cinquante et une"
	else:
		return "{0}".format(str(i))

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
	headers = {'accept': 'application/json', 'authorization': 'Basic anVub246UlFXSnVub25YcG0yWA=='}
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
	city = intent_message.slots.city.first().value
	print(city)
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
		sentence = 'La qualitai de lair est '
		print(intent_message.intent.intent_name)
		
		sentence += verbalise_air_quality(aqi)
		print(sentence)
		hermes.publish_end_session(intent_message.session_id, sentence)
		
	elif "greetings" in intent_message.intent.intent_name:
	#elif intent_message.intent.intent_name == 'Joseph:greetings':

		hermes.publish_end_session(intent_message.session_id, "De rien!")


with Hermes(MQTT_ADDR) as h:
	h.subscribe_intents(intent_received).start()
