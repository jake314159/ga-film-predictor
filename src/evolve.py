#
#   --------------------------------
#      ga-film-predictor  
#      evolve.py
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

#
# This program takes some film data in a fds format and will use it to create an evs
#  file which can then be used to make predictions using a GA.
#
# Example usage
#
# $ python3 evolve.py ../film_data.fds "evalScores.evs"
#
#

import time
import random
import operator
import sys
from film_eval import *
from film_store_io import *

sample_size = 220
good_film_threshold = 70

# Used to keep an EvalScore with it's rating on how good it is
class ProcessedScore:
    eval_score = None
    rating = 1000000000
    def __init__(self, eval_score, rating):
        self.eval_score = eval_score
        self.rating = rating

#
# Takes a list of EvalScores and creates (and returns) a list of ProcessedScore objects
# With the rating filled and with the list sorted with the best first
#
def create_processed_list( score_list ):
    score_list_processed = [None]*len(score_list)
    for i in range(len(score_list)):
        correct = 0
        for film_N in range(len(store.entries)):
            score = eval_film(store.entries[film_N].film, score_list[i])
            if (score > 0 and store.entries[film_N].score >= good_film_threshold) or (score < 0 and store.entries[film_N].score < good_film_threshold):
                correct += 1
        score_list_processed[i] = ProcessedScore(score_list[i], correct)
    return sorted(score_list_processed, key=operator.attrgetter('rating'), reverse=True)

# Loads the store from file
store = load_store(sys.argv[1])
print(store)
print("Number of entries: "+str(store.number_of_entries()))

#
# Creates an initial EvalScore list with information on genres, actors, directors and writers
# but with random weights
#
score_list = [None]*sample_size
print(len(score_list))
for i in range(len(score_list)):
    score_list[i] = EvalScores()
    score_list[i].randomize()
    # Add film genre data
    for entry in store.entries:
        for genre in entry.film.genre:
            score_list[i].add_genre_data(genre.replace(" ", ""), entry.score)
        for actor in entry.film.actor:
            score_list[i].add_actor_data(actor.strip(), entry.score)
        for director in entry.film.director:
            score_list[i].add_director_data(director.strip(), entry.score)
        for writer in entry.film.writer:
            score_list[i].add_writer_data(writer.strip(), entry.score)

prc_list = create_processed_list( score_list )
print("Best score... " + str( prc_list[0].rating ))

no_improve_in = 0
to_improve_on = -1
try_number = 0
#
# Try to mutate and cross a good score object stopping when we go
# 50 generations with no improvement
#
while no_improve_in < 50:
    for i in range(len(score_list)):
        if i <= 8: ##Keep top 8 with minor changes
            score_list[i] = prc_list[i].eval_score.clone_self().mutate().mutate()
        else:
            if random.randint(0, 4) == 0: 
                ## Mutate random EvalScore
                score_list[i] = (prc_list[random.randint(0, i-1)].eval_score.clone_self()).mutate().mutate().mutate()
            else:
                ## Cross random pair
                score_list[i] = (prc_list[random.randint(0, i-1)].eval_score.clone_self()).cross(prc_list[random.randint(0, i-1)].eval_score)
    prc_list = create_processed_list( score_list )

    if prc_list[0].rating <= to_improve_on:
        no_improve_in += 1
    else:
        no_improve_in = 0
        to_improve_on = prc_list[0].rating

    # Only print an output every 20 generations
    if try_number%20 == 0:
        print("Best score... " + str( prc_list[0].rating ) + "\t" + str(int(float((prc_list[0].rating)*100.0)/float(store.number_of_entries()))) + "%\t on try " + str(try_number))

    try_number += 1

msg = str(int(float((prc_list[0].rating)*100.0)/float(store.number_of_entries()))) + "% " + str(prc_list[0].rating)
save_eval_scores(prc_list[0].eval_score, msg, sys.argv[2])

