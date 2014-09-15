#
#   --------------------------------
#      ga-film-predictor  
#      film_data.py
#   -------------------------------- 
#
#        Author: Jacob Causon            
#                August 2014 
#
#   Licensed under the Apache License, Version 2.0 (the "License"); 
#    you may not use this file except in compliance with the License. 
#    You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software distributed
#    under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#    CONDITIONS OF ANY KIND, either express or implied. See the License for the
#    specific language governing permissions and limitations under the License.
#
#

import urllib.request
import re

class Film:
    """Film class containing information about a film"""
    title= ""
    genre = []
    director = []
    writer = []
    actor = []
    imdb_score = 5
    meta_score = 50
    tomato_score = 50
    tomato_user_score = 50
    imdb_id = ""

    def __init__(self, imdb_id):
        self.imdb_id = imdb_id

def create_film_from_imdb( imdb_id ):
    f = Film(imdb_id)
    
    url = "http://www.omdbapi.com/?tomatoes=true&i=" + imdb_id + "&t="
    data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "film-predictor"}))

    pattern = re.compile("((\"Title\":\"(?P<TITLE>[^\"]*)\"|\"Genre\":\"(?P<GENRE>[^\"]*)\"|\"Director\":\"(?P<DIRECTOR>[^\"]*)\"|\"Writer\":\"(?P<WRITER>[^\"]*)\"|\"Actors\":\"(?P<ACTORS>[^\"]*)\"|\"imdbRating\":\"(?P<IMDB_SCORE>[^\"]*)\"|\"Metascore\":\"(?P<META_SCORE>[^\"]*)\"|\"tomatoMeter\":\"(?P<TOMATO_SCORE>[^\"]*)\"|\"tomatoUserMeter\":\"(?P<TOMATO_USER_SCORE>[^\"]*)\"|\"Response\":\"(?P<RESPONSE>[^\"]*)\"|.))*")

    match = pattern.search(str(data.read()))

    # Check if something valid was found
    if match.group("RESPONSE") != "True":
        return None
    else:
        f.title = match.group("TITLE")
        f.genre = match.group("GENRE").split(",")
        f.director = match.group("DIRECTOR").split(",")
        f.writer = match.group("WRITER").split(",")
        f.actor = match.group("ACTORS").split(",")
        try:
            f.imdb_score = float(match.group("IMDB_SCORE"))
        except ValueError:
            pass
        try:
            f.meta_score = int(match.group("META_SCORE"))
        except ValueError:
            pass
        try:
            f.tomato_score = int(match.group("TOMATO_SCORE"))
        except ValueError:
            pass
        try:
            f.tomato_user_score = int(match.group("TOMATO_USER_SCORE"))
        except ValueError:
            pass

        return f

