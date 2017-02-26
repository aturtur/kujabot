# -*- coding: cp1252 -*-
import urllib2

def get_prediction(question):
    clean_question = urllib2.quote(question)
    orcale_url = 'http://www.lintukoto.net/viihde/oraakkeli/index.php?kysymys={}&html'\
            .format(clean_question)
    oracle_request = urllib2.Request(orcale_url)
    oracle_response = urllib2.urlopen(oracle_request)
    answer = oracle_response.read()
    return answer
