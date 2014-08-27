GA film predictor
==================

This program is designed to predict whether you are going to enjoy a film which you haven't seen before. The software uses a *Genetic algorithm* along with data on films you have seen before to discover what you like and what you dislike. This can then be used to make predictions on films you haven't seen before with an accuracy of around **88%**.

How effective is it?
-------------------------

The accuracy of the program will depend heavily on the quality of the data being supplied to it. The program was tested using **479** films rated from 0-100 with an average (mean) score of *67.94* and a median score of *72*. A '*good*' film was defined as having a score over or equal to 70 and a '*bad*' film was defined as having below 70.

The evolve.py file was used with this data set to create an evs file which could be used for making predictions. In the table below shows the accuracy scores from the created evs file along with some other methods of prediction as a comparison and how it managed some test data which wasn’t included in the original training data.

| Prediction method                     | Accuracy |
|:--------------------------------------|:--------:|
| Random                                | 50%      |
| Always return 'GOOD'                  | 54%      |
| Using critic scores only              | 65%      |
| predict.py on training data           | **96%**  |
| predict.py on test data               | **88%**  |

As shown above the accuracy of the program is around *85%* when using data points which were not included in the training data set. A breakdown of the outcome from the test data is shown below. The total is weighted to take into account how common each correct response is.

| Expected | Sample size | Correct | Incorrect  |
|:---------|:------------|:-------:|:----------:|
| GOOD     | 9           | 100%    | 0%         |
| BAD      | 11          | 73%     | 27%        |
| TOTAL    | 20          | **88%** | **12%**    |

How to use
----------------

This program is used in two steps. First data on films which you have watched is processed into a .evs (Evaluation Score) file which contains information about what you like and dislike. This is then used in part 2 to decide if you are likely to enjoy a film you haven't seen before (specified with a IMDB ID). Part 1 should only be required to be run once although you should consider running through the first part again is significantly more data becomes available.  

###Part 1

The first part uses a list of films you have seen before along with a score out of 100 (where \< 70 is not good and \> 70 is good). This should be in a csv file in the following format.  
```
film title,my_score,IMDB_URL
```  
eg.  

```
Inglourious Basterds,91,http://www.imdb.com/title/tt0361748/
```  
There should be as much supplied data as possible (ideally over 500 films). The more data that is supplied the accurate the predictions will be.

The CSV itself doesn't contain all the information required so this will first need to be put through the "film_data_collector.py" file. This will collect all the missing data from the internet and create a ".fds" (film data store) file containing all the information. An example which will create a file called "film_data_store.fds" is shown below. This may take some time.  
```bash
python3 film_data_collector.py my_film_scores.csv film_data_store.fds
```  
Once the data is collected you can then process this data ready for making predictions using the "evolve.py" file along with the .fds file you created earlier, an example of which is shown below. This will create a .evs (eval scores) which is all the data and values which are required to make a prediction. Once created the *csv* file and *fds* file is no longer required.  
```
python3 evolve.py film_data_store.fds eval_scores.evs
```

###Part 2

Once you have created an evs file you are then ready to make some predictions! Predictions are made using IMDB ID's. Once you have an ID for a film you can make a prediction on whether you will like it with the command below. The eval_scores.evs is the file you created in part 1.  
```
python3 predictor.py eval_scores.evs tt0076759
```  


##Licence

   Copyright 2014 Jacob Causon

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

