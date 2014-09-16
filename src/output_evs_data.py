#
#   --------------------------------
#      ga-film-predictor  
#      output_evs_data.py
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
from film_eval import *

eScore = load_eval_scores(sys.argv[1])

print("########## ACTORS  ##########")
actor_list = []

for actor in eScore.actor_total.keys():
    if eScore.actor_count[actor] <=1:
        continue
    percent = (eScore.actor_total[actor])/eScore.actor_count[actor]
    actor_list.append( (actor, percent, eScore.actor_count[actor]) )

actor_list.sort(reverse=True, key=lambda x: x[1])

for g in actor_list:
    sys.stdout.write("'%s'"%g[0])
    pad = 30-len(g[0])
    if pad>0:
        for i in range(pad):
            sys.stdout.write(" ")
        
    print(("%f (%d)") % (g[1], g[2]))

print("########## DIRECTOR  ##########")
director_list = []

for director in eScore.director_total.keys():
    if eScore.director_count[director] <=1:
        continue
    percent = (eScore.director_total[director])/eScore.director_count[director]
    director_list.append( (director, percent, eScore.director_count[director]) )

director_list.sort(reverse=True, key=lambda x: x[1])

for g in director_list:
    sys.stdout.write("'%s'"%g[0])
    pad = 30-len(g[0])
    if pad>0:
        for i in range(pad):
            sys.stdout.write(" ")
        
    print(("%f (%d)") % (g[1], g[2]))

print("########## GENRES  ##########")
genre_list = []

for genre in eScore.genre_total.keys():
    percent = (eScore.genre_total[genre])/eScore.genre_count[genre]
    genre_list.append( (genre, percent, eScore.genre_count[genre]) )

genre_list.sort(reverse=True, key=lambda x: x[1])

for g in genre_list:
    sys.stdout.write("'%s'"%g[0])
    pad = 17-len(g[0])
    if pad>0:
        for i in range(pad):
            sys.stdout.write(" ")
        
    print(("%f (%d)") % (g[1], g[2]))

print("########## WEIGHTS ##########")
print("Genre 1:         %f" % eScore.vals[0])
print("Genre 2:         %f" % eScore.vals[1])
print("Genre 3:         %f" % eScore.vals[2])
print("Director:        %f" % eScore.vals[3])
print("Writer:          %f" % eScore.vals[4])
print("Actor:           %f" % eScore.vals[5])
print("imdb_score:      %f" % eScore.vals[6])
print("meta_score:      %f" % eScore.vals[7])
print("tomato_score:    %f" % eScore.vals[8])
print("tom_user_score:  %f" % eScore.vals[9])


