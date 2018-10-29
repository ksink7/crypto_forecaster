# crypto_prediction_builder
##Maintains a database of historical pricing data, builds out features to be used for ML models, trains those ML models, and logs predictions to csv file.

###MAIN FUNCTION DOES THE FOLLOWING IN ORDER:\
  -UPDATES DATABASE (CURRENTLY JUST BITTREX DATA, MORE EXCHANGES WILL BE ADDED IN THE FUTURE)\
  -REBUILDS FEATURE SETS (CURRENTLY JUST FOR LINEAR REGRESSION, FUNCTIONS NEEDED FOR INPUTS FOR LSTM TRAINING)\
    -THIS IS WHERE YOU PUT THE FEATURES YOU WANT BUILT, THERE ARE ONLY A FEW BASIC EXAMPLES IN THE BUILDER FUNCTIONS\
  -REBUILDS MODELS \
  -UPDATES PREDICTION LOGS (CURRENTLY JUST OUTPUTS TO CSV FILES, MORE EFFICIENT TECHNIQUES TO COME)\


***\
-IGNORE FORECASTER FOLDER\
-PROGRAM IS JUST A FRAMEWORK FOR BUILDING PREDICTIVE ML MODELS AT SCALE\
-MODEL/FEATURE BUILDER HELPER FILES CONTAIN FUNCTIONS FOR A SIMPLE LINEAR REGRESSION MODEL FORECASTING AT VARIOUS PERIODS\
-NEW TECHNIQUES (LIKE LSTM NETWORKS) CAN BE ADDED INTO THESE HELPER FUNCTIONS AND RAN FROM THE MAIN PREDICTION BUILDER FILE\
***\

###Improvements to come in the near future:\
-requirements.txt file\
-Replace function arguments with correct arg/kwargs syntax\
-Ability to pass arguments from command line (currently only functional for prediction_grapher.py)\
-Accurate prediction log times(time zone issues have been corrected and defaults to US/Mountain)\
-Improved graphing options(Will be a dash or flask app that graphs future projections LIVE on any timeframe)\
-Backtesting file for testing model projections with various strategies (eventual reinforcement learning algo will replace this)\
-Live/paper trading program for further testing/verification



