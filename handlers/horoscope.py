# -*- coding: cp1252 -*-
import urllib2
import re

def get_horoscope(horoscope):
    horoscopes = ['oinas', 'härkä', 'kaksonen', 'rapu', 'leijona', 'neitsyt', \
            'vaaka', 'skorpioni', 'jousimies', 'kauris', 'vesimies', 'kalat']
    horoscope = horoscope.lower()
    return_value = 'En ymmärtänyt'
    if horoscope in horoscopes:
        horoscope_url = 'http://www.iltalehti.fi/horoskooppi/'
        horoscope_request = urllib2.Request(horoscope_url)
        horoscope_response = urllib2.urlopen(horoscope_request)
        content = horoscope_response.read().lower()
        splitdata = content.split(horoscope, 1)
        answer = splitdata[1].split('</p>', 1)
        result = ""
        sentence = answer[0].split(". ")
        for part in sentence:
            result += part[0].upper() + part[1:] + '. '
        return_value = horoscope.capitalize() + result[:-2]
        return_value = re.sub(r'</?[a-z][a-z0-9]*[^<>]*>', '', return_value)

    return return_value