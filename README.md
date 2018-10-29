# crypto_prediction_builder

## Builds prediction logs for cryptocurrencies on different intervals/prediction periods
### -Builds and maintains OHLC data in local folder to be used in model building/predictions

### MAIN FUNCTION DOES THE FOLLOWING IN ORDER:\
  1. Updates Database (CURRENTLY JUST BITTREX DATA, MORE EXCHANGES WILL BE ADDED IN THE FUTURE)\
  2. Rebuilds Feature Set (CURRENTLY JUST FOR LINEAR REGRESSION, FUNCTIONS NEEDED FOR INPUTS FOR LSTM TRAINING)\
    2a. THIS IS WHERE YOU PUT THE FEATURES YOU WANT BUILT, THERE ARE ONLY A FEW BASIC EXAMPLES IN THE BUILDER FUNCTIONS\
  3. Rebuilds and saves out models to be used for projections \
    3a. Input other models here (LSTM, SVR..)
  4. Update Prediction Logs (CURRENTLY JUST OUTPUTS TO CSV FILES, MORE EFFICIENT TECHNIQUES TO COME)\


### Improvements to come in the near future:\
-requirements.txt file\
-Replace function arguments with correct arg/kwargs syntax\
-Ability to pass arguments from command line (currently only functional for prediction_grapher.py)\
-Accurate prediction log times(time zone issues have been corrected and defaults to US/Mountain)\
-Improved graphing options(Will be a dash or flask app that graphs future projections LIVE on any timeframe)\
-Backtesting file for testing model projections with various strategies (eventual reinforcement learning algo will replace this)\
-Live/paper trading program for further testing/verification
-Orderbook database for more features to use in different models
-Web Scraper to be used for sentiment analysis



***\
    -PROGRAM IS CURRENTY JUST A FRAMEWORK FOR BUILDING PREDICTIVE ML MODELS AT SCALE\
    -MODEL/FEATURE BUILDER HELPER FILES CONTAIN FUNCTIONS FOR A SIMPLE LINEAR REGRESSION MODEL FORECASTING AT VARIOUS PERIODS\
    -NEW TECHNIQUES (LIKE LSTM NETWORKS) CAN BE ADDED INTO THESE HELPER FUNCTIONS AND RAN FROM THE MAIN PREDICTION BUILDER FILE\
***\

