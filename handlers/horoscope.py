# -*- coding: cp1252 -*-
import urllib2
import re

def get_horoscope(horoscope):
    horoscopes = ['oinas', 'härkä', 'kaksonen', 'rapu', 'leijona', 'neitsyt', \
            'vaaka', 'skorpioni', 'jousimies', 'kauris', 'vesimies', 'kalat']
    horoscope = horoscope.lower()
    return_value = 'En ymmärtänyt'
    if horoscope in horoscopes:
        result = ""
        horoscope_url = 'http://www.iltalehti.fi/horoskooppi/'
        horoscope_request = urllib2.Request(horoscope_url)
        horoscope_response = urllib2.urlopen(horoscope_request)
        content = horoscope_response.read().lower()
        splitdata = content.split(horoscope, 1)
        answer = splitdata[1].split('</p>', 1)
        stripped_answer = re.sub(r'</?[a-z][a-z0-9]*[^<>]*>', '', answer[0])
        sentence = stripped_answer.split(". ")
        for part in sentence:
            result += part[0].upper() + part[1:] + '. '
        return_value = horoscope.capitalize() + result[:-2]
        
    return return_value