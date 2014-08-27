#
#   --------------------------------
#      ga-film-predictor  
#      film_store_io.py
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

import sys
from film_data import *
from film_data_store import *

#
# Takes the filename of a csv file with the format:
# title,my_score,IMRB_URL
#
#   eg.
# Inglourious Basterds,91,http://www.imdb.com/title/tt0361748/
#
# and creates a new FilmDataStore object which is used to create a
# EvalScore object during evlolution. The data store simply contains
# a list of films and the users rating of that film. Go to the file
# "film_data_store.py" for more detail
#
def make_store_from_csv( filename ):

    line_pattern = re.compile("(?P<TITLE>[^,]*),(?P<SCORE>[^,]*),(?P<URL>[^,]*)")
    url_pattern = re.compile(".*/title/(?P<ID>[^,]*)/")

    print(filename)

    lines = [line.strip() for line in open(filename)]

    store = FilmDataStore()

    for line in lines:
        match = line_pattern.search(line)
        if match.group("URL") != None:
            id_match = url_pattern.search(match.group("URL"))
        else:
            id_match = None

        sys.stdout.write(match.group("TITLE"))
        sys.stdout.write("\t")
        if match != None and match.group("SCORE") != None and id_match != None and id_match.group("ID") != None:
            store.add_film( create_film_from_imdb( id_match.group("ID") ), int(match.group("SCORE")) )
            print("Success")
        else:
            print("Fail")

    print("Final size:")
    print(store.number_of_entries())

    return store

#
# Save a FilmDataStore to file for future use
#
def save_store(store, filename):
    import pickle
    print("Saving... "+str(filename))
    with open(filename, 'wb') as output:
        for film in store.entries:
            pickle.dump(film, output, pickle.HIGHEST_PROTOCOL)

#
# Load a FilmDataStore from file for use
#
def load_store(filename):
    import pickle
    store = FilmDataStore()
    print("Loading... "+str(filename))
    with open(filename, 'rb') as input:
        try:
            while True:
                e = pickle.load(input)
                store.add_film(e.film, e.score)
        except EOFError:
            print("DONE")
    return store

