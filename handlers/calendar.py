# -*- coding: cp1252 -*-
import urllib2

def get_nameday():
    nameday_url = 'http://www.jkauppi.fi/nimipaivat/'
    nameday_request = urllib2.Request(nameday_url)
    nameday_response = urllib2.urlopen(nameday_request)
    content = nameday_response.read()
    find = ': '
    splitdata = content.split(find, 1)
    answer = splitdata[1].split(' <br />', 1)[0]

    return answer
