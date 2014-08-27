#
#   --------------------------------
#      ga-film-predictor  
#      film_data_store.py
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

class filmEntry:
    film = None
    score = 0
    def __init__(self, film, score):
        self.film = film
        self.score = score

class FilmDataStore:
    entries = []
    def add_film(self, film, score):
        self.entries.append( filmEntry(film,score) )

    def number_of_entries(self):
        return len(self.entries)
        
