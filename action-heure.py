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
	
	
	print(intent_message.intent.intent_name)
	print()
		
	if "cityForAirQuality" in intent_message.intent.intent_name:
		
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
		url = 'https://junon---develop-sr3snxi-ma2sa5nwhuqdk.fr-1.platformsh.site/v1/air/quality?lat='+str(lat)+'&lon='+str(lng)
		print(url)
		response = requests.get(url, headers=headers)
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
		
		sentence = "La qualitai de l'air a "+ city +" est "
		print(intent_message.intent.intent_name)
		
		sentence += verbalise_air_quality(aqi)
		sentence += " il n'est pas recommandai de faire des efforts a l'extairieur. Souhaitez vous que je vous propose une alternative."
		print(sentence)
		hermes.publish_end_session(intent_message.session_id, sentence)
		
	elif "proposition1" in intent_message.intent.intent_name:
		
		print(intent_message.intent.intent_name)
		sentence = "Il est praivue que la qualitai de l'air s'amailiore, vous pouvez aller courir a partir de 19 heures"
		print(sentence)
		hermes.publish_end_session(intent_message.session_id, sentence)
		
	elif "proposition2" in intent_message.intent.intent_name:
		
		print(intent_message.intent.intent_name)
		sentence = "Je peux vous proposer un programme de fitness sur votre TV. Souhaitez-vous lancer le programme ?"
		print(sentence)
		hermes.publish_end_session(intent_message.session_id, sentence)
		
	elif "proposition3" in intent_message.intent.intent_name:
		
		print(intent_message.intent.intent_name)
		sentence = "Je praipare l'ambiance et c'est parti !"
		print(sentence)
		hermes.publish_end_session(intent_message.session_id, sentence)
		
	else:
		
		sentence = "Je ne vous ai pas compris reformulez votre demande !"
		print(sentence)
		hermes.publish_end_session(intent_message.session_id, sentence)


with Hermes(MQTT_ADDR) as h:
	h.subscribe_intents(intent_received).start()
