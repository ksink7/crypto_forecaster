## Cryptocurrency Forecaster
# Maintains a database of historical pricing data, builds out features to be used for ML models, trains those ML models, and logs predictions to csv file.

## MAIN FUNCTION DOES THE FOLLOWING IN ORDER:\
    1. Updates Database (CURRENTLY JUST BITTREX DATA, MORE EXCHANGES WILL BE ADDED IN THE FUTURE)\
    2. Rebuilds Feature Set (CURRENTLY ONLY FEATURES FOR LINEAR REGRESSION, MORE TO COME)
        2a. As more ML models are added to section 3, feature set builders need added here\
    3. Rebuilds and saves out models to be used for projections
        3a. Input other models here (LSTM, SVR..)
    4. Update Prediction Logs (CURRENTLY JUST OUTPUTS TO CSV FILES, MORE    EFFICIENT TECHNIQUES TO COME)\

## Arguments to run prediction builder from command line:
    -D - Update Database (ex. D=Yes will update the database for all coins set in prediction_builder file)\
    -F - Update Feature datasets\
    -M - Update all models\
    -L - Update prediction logs\

    ***All default to No, can change within the main function in prediction_builder***
    
    example command line:
    crypto_forecaster $ python prediction_builder.py D=Yes F=Yes M=Yes L=Yes
        -This will rerun all sections of the program from database updating to building the logs


## Arguments to run prediction_grapher from command line:
    -Functionality to come...\


## Improvements to come:
-requirements.txt file\
-Replace function arguments with correct arg/kwargs syntax (main function corrected)\
-Ability to pass arguments from command line (currently only functional for prediction_grapher.py)\
-Accurate prediction log times(time zone issues have been corrected and defaults to US/Mountain)\
-Improved graphing options(Will be a dash or flask app that graphs future projections LIVE on any timeframe)\
-Backtesting file for testing model projections with various strategies (eventual reinforcement learning algo will replace this)\
-Live/paper trading program for further testing/verification -Orderbook database for more features to use in different models -Web Scraper to be used for sentiment analysis\

***
-PROGRAM IS CURRENTLY JUST A FRAMEWORK FOR BUILDING PREDICTIVE ML MODELS AT SCALE
-MODEL/FEATURE BUILDER HELPER FILES CONTAIN FUNCTIONS FOR A SIMPLE LINEAR REGRESSION MODEL FORECASTING AT VARIOUS PERIODS
-NEW TECHNIQUES (LIKE LSTM NETWORKS) CAN BE ADDED INTO THESE HELPER FUNCTIONS AND RAN FROM THE MAIN PREDICTION BUILDER FILE
***
