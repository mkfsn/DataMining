#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= ' 4月 30, 2014 '
__author__= 'mkfsn'

import httplib2
import json

# sudo apt-get install python-pip python-dev build-essential 
# sudo pip install google-api-python-client
import apiclient.discovery 


class GoogleAPI:

    service = None

    def __init__ (self, config):
        self.service = apiclient.discovery.build (
            'plus', 
            'v1', 
            http = httplib2.Http(), 
            developerKey = config['API_KEY']
        )

    def people_get (self, userid):

        if self.service is None:
            return None

        profile = self.service.people().get(userId = userid).execute()
        return profile


    def activities_list (self, userid):

        if self.service is None:
            return None

        activities = self.service.activities().list(userId = userid,
                collection='public').execute()
        return activities


    def people_search (self, query):

        if self.service is None:
            return None

        people = self.service.people().search(query = query).execute()
        return people


def test ():
    # XXX: Enter in your API key from  https://code.google.com/apis/console
    json_data = open ('mkfsn_secrets.json')
    secrets = json.load (json_data)

    google = GoogleAPI(secrets)
    
    #userid = "101184229781272153227" #gentoo
    #profile = google.people_get(userid)
    #print json.dumps(profile, indent = 1)


if __name__ == '__main__':
    test()
