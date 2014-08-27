#
#   --------------------------------
#      ga-film-predictor  
#      film_eval.py
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

from film_data import *
import random

mutation_rate = 0.2
number_of_parts = 10
#    0,1,2  genre[]
#    3,     director[]
#    4,     writer[]
#    5,     actor[]
#    6,     imdb_score
#    7,     meta_score
#    8,     tomato_score
#    9,     tomato_user_score

class EvalScores:
    vals = [1.0]*number_of_parts
    genre_total = {}
    genre_count = {}

    actor_total = {}
    actor_count = {}

    director_total = {}
    director_count = {}

    writer_total = {}
    writer_count = {}

    def __init__(self):
        self.vals = [1.0]*number_of_parts

    def add_genre_data(self, genre, score):
        if genre in self.genre_total and genre in self.genre_count:
            self.genre_total[genre] += (score-70)
            self.genre_count[genre] += 1
        else:
            self.genre_total[genre] = (score-70)
            self.genre_count[genre] = 1

    def get_genre_score(self, genre):
        if genre in self.genre_total and genre in self.genre_count:
            return float(self.genre_total[genre])/float(self.genre_count[genre])
        else:
            return 0

    def add_actor_data(self, actor, score):
        if actor in self.actor_total and actor in self.actor_count:
            self.actor_total[actor] += (score-70)
            self.actor_count[actor] += 1
        else:
            self.actor_total[actor] = (score-70)
            self.actor_count[actor] = 1

    def get_actor_score(self, actor):
        if actor in self.actor_total and actor in self.actor_count:
            return float(self.actor_total[actor])/float(self.actor_count[actor])
        else:
            return 0

    def add_director_data(self, director, score):
        if director in self.director_total and director in self.director_count:
            self.director_total[director] += (score-70)
            self.director_count[director] += 1
        else:
            self.director_total[director] = (score-70)
            self.director_count[director] = 1

    def get_director_score(self, director):
        if director in self.director_total and director in self.director_count:
            return float(self.director_total[director])/float(self.director_count[director])
        else:
            return 0

    def add_writer_data(self, writer, score):
        if writer in self.writer_total and writer in self.writer_count:
            self.writer_total[writer] += (score-70)
            self.writer_count[writer] += 1
        else:
            self.writer_total[writer] = (score-70)
            self.writer_count[writer] = 1

    def get_writer_score(self, writer):
        if writer in self.writer_total and writer in self.writer_count:
            return float(self.writer_total[writer])/float(self.writer_count[writer])
        else:
            return 0

    def clone_self(self):
        ret = EvalScores()
        for i in range(len(self.vals)):
            ret.vals[i] = self.vals[i]
        ret.genre_total = self.genre_total
        ret.genre_count = self.genre_count
        ret.actor_total = self.actor_total
        ret.actor_count = self.actor_count
        ret.director_total = self.director_total
        ret.director_count = self.director_count
        ret.writer_total = self.writer_total
        ret.writer_count = self.writer_count
        return ret

    def randomize(self):
        for i in range(len(self.vals)):
            if random.randint(0, 1) == 0:
                self.vals[i] = random.random()
            else:
                self.vals[i] = -random.random()
        return self

    def mutate(self):
        element = random.randint(0, len(self.vals)-1)
        if random.randint(0, 1) == 0:
            # Mutate down
            self.vals[element] *= 1.0 - (random.random()*mutation_rate)
        else:
            # Mutate up
            self.vals[element] *= 1.0 + (random.random()*mutation_rate)
        return self

    def cross(self, otherScores):
        for i in range(len(self.vals)):
            r = random.randint(0, 1)
            if r == 0:
                self.vals[i] = otherScores.vals[i]
        return self

def eval_film( film, evalScores ):
    value = 0.0

    i=0
    for genre in film.genre:
        value += evalScores.get_genre_score( genre )*evalScores.vals[i]
        if i<2:
            i += 1

    count = 0
    total = 0
    for actor in film.actor:
        total += evalScores.get_actor_score(actor)
        count += 1
    value += (total/count)*evalScores.vals[5]

    count = 0
    total = 0
    for director in film.director:
        total += evalScores.get_director_score(director)
        count += 1
    value += (total/count)*evalScores.vals[3]

    count = 0
    total = 0
    for writer in film.writer:
        total += evalScores.get_writer_score(writer)
        count += 1
    value += (total/count)*evalScores.vals[4]

    value += film.imdb_score * evalScores.vals[6]
    value += film.meta_score * evalScores.vals[7]
    value += film.tomato_score * evalScores.vals[8]
    value += film.tomato_user_score * evalScores.vals[9]

    return value

#
# Note: The 'msg' is just a string which identifies the evalScores obj (eg. It's success rate)
# It is placed at the start so it is easy to find with a hexdump
#
def save_eval_scores(evalScores, msg, filename):
    import pickle
    with open(filename, 'wb') as output:
        pickle.dump(msg, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(evalScores, output, pickle.HIGHEST_PROTOCOL)

def load_eval_scores(filename):
    import pickle
    msg = ""
    evalScores = None
    with open(filename, 'rb') as input:
        msg = pickle.load(input)
        evalScores = pickle.load(input)
    return evalScores

