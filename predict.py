# %%

import pandas as pd
from data_cleaner import attach_dataframes 
import pickle

def predict(matches, model):

    home_team = [x[0] for x in matches]
    away_team = [x[1] for x in matches]
    
    prediction_set = {'home_team': home_team,
            'away_team': away_team
            }

    prediction_set = pd.DataFrame(data = prediction_set)
    
    prediction_set = attach_dataframes('home_team', prediction_set)
    prediction_set = attach_dataframes('away_team', prediction_set)
    prediction_set.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis = 1, inplace = True)
    
    final_dummy = pd.read_csv('final_dummy.csv')

    final = pd.get_dummies(prediction_set, prefix=['home_team', 'away_team'],  columns=['home_team', 'away_team'])

    missing_columns = set(final_dummy.columns) - set(final.columns)
    for column in missing_columns:
        final[column] = 0
    final = final[final_dummy.columns]
    
    final = final.drop(['winning_team', 'Unnamed: 0'], axis = 1)

    final.to_csv('final.csv')

    predictions = model.predict(final)
    print(predictions)


    for i in range(len(prediction_set)):
        print(prediction_set.iloc[i, 1] + " and " + prediction_set.iloc[i, 0])
        if predictions[i] == 2:
            print("Winner: " + prediction_set.iloc[i, 1])
        elif predictions[i] == 1:
            print("Tie")
        elif predictions[i] == 0:
            print("Winner: " + prediction_set.iloc[i, 0])
        print('Probability of ' + prediction_set.iloc[i, 1] + ' winning: ' , '%.3f'%(model.predict_proba(final)[i][2]))
        print('Probability of Tie: ', '%.3f'%(model.predict_proba(final)[i][1])) 
        print('Probability of ' + prediction_set.iloc[i, 0] + ' winning: ', '%.3f'%(model.predict_proba(final)[i][0]))
        print("")

logreg = pickle.load(open('trained_model.sav', 'rb'))

group_16 = [('France', 'Argentina'),
            ('Uruguay', 'Portugal'),
            ('Spain', 'Russia'),
            ('Croatia', 'Denmark'),
            ('Brazil', 'Mexico'),
            ('Belgium', 'Japan'),
            ('England', 'Colombia'),
            ('Sweden', 'Switzerland')
            ]

predict(group_16, logreg) 

# quarters = [('Argentina', 'Uruguay'),
#             ('Russia', 'Denmark'),
#             ('Sweden', 'Colombia'),
#             ('Mexico', 'Japan')]

# predict(quarters, logreg)

# semis = [('Uruguay', 'Russia'),
# ('Colombia', 'Japan')]

# predict(semis, logreg)

# final = [('Russia', 'Japan')]

# predict(final, logreg)