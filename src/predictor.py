#
#   --------------------------------
#      ga-film-predictor  
#      predictor.py
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
# Takes a .evs EvalScore file (created with evolve.py) and an imdb id code
# and makes a prediction on whether the person the evs file was create for
# is going to like the film.
#
#      Example usage
#  $ python3 evalScore.evs tt1291150
#
#      Example with explanation
#  $ python3 evalScore.evs tt1291150 explain

import sys
from film_data import *
from film_store_io import *
from film_eval import *

f = create_film_from_imdb(sys.argv[2])
evalScore = load_eval_scores(sys.argv[1])

explain = False
if len(sys.argv)>3 and sys.argv[3] == "explain":
    explain = True

score = eval_film(f, evalScore, explain)

sys.stdout.write(f.title)

pad = 49-len(f.title)
if pad > 0:
    for i in range(pad):
        sys.stdout.write(" ")
sys.stdout.write(" ")

if score > 0:
    sys.stdout.write("GOOD")
else:
    sys.stdout.write("BAD ")

sys.stdout.write("    " + str(score) + "\n")

