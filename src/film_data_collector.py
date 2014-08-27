#
#   --------------------------------
#      ga-film-predictor  
#      film_data_collector.py
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
# Uses a csv in the format
# film_title,my_score,IMDB_URL
#
# And collects all the data together ready into a output file
# 
# Run with the command:
#    $ python3 film_data_collector.py csv_file output_file
#
# The output file should have the ext ".fds" (film data store)
#
# This file is required by the "evolve.py" script but will not
# be needed once a EvalScore has been created
#

import sys
from film_data import *
from film_data_store import *
from film_store_io import *

my_store = make_store_from_csv( sys.argv[1] )
save_store(my_store, sys.argv[2])
print(my_store)
print(my_store.number_of_entries())

