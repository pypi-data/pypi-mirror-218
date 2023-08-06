from ..data import load_stock_returns_on_calls, load_call_statements
from .config import default_role_weights, default_section_weights, default_statement_type_weights, default_holding_period
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

import pickle
import warnings
warnings.filterwarnings('ignore')


stock_return_data = load_stock_returns_on_calls(
    'train')[['call_uid', 'excess_return', 'holding_period']]
call_statement_data = load_call_statements('train')


def train(feature_files=[],
          role_weights=default_role_weights,
          section_weights=default_section_weights,
          statement_type_weights=default_statement_type_weights,
          sell_quantile=0.35,
          buy_quantile=0.65,
          holding_period=default_holding_period,
          classifier='logistic_regression',
          save_model='model.pkl'):
    """
    Train a model using the provided feature files and parameters.

    Parameters:
        - feature_files: A list of paths to feature files.
        - role_weights: A dictionary of weights for different presentor roles.
        - section_weights: A dictionary of weights for different sections.
        - statement_type_weights: A dictionary of weights for different statement types.
        - sell_quantile: The quantile value for determining the sell threshold. Defaults to 0.35.
        - buy_quantile: The quantile value for determining the buy threshold. Defaults to 0.65.
        - holding_period: The holding period for the stock return data.
        - classifier: The type of classifier to use for training ('logistic_regression', 'random_forest', or 'neural_network'). Defaults to 'logistic_regression'.
        - save_model: The path to save the trained model.

    Returns:
        None
    """
    # load features
    feature_df = call_statement_data[[
        'statement_uid', 'call_uid', 'presentor_role', 'section', 'statement_type']].set_index('statement_uid')

    feature_cols = []
    for feature_file in feature_files:
        feature_data = pd.read_parquet(feature_file)
        # merge on index
        feature_df = pd.merge(feature_df, feature_data,
                              left_index=True, right_index=True)
        feature_cols += feature_data.columns.tolist()

    # aggregate features to call_uid level by the weights provided
    agg_feature_df = pd.DataFrame(
        columns=feature_cols, index=feature_df.call_uid.unique())
    for call_uid, call_feature in feature_df.groupby('call_uid'):
        agg_feature = call_feature[feature_cols].multiply(
            call_feature.presentor_role.map(role_weights), axis=0).multiply(
            call_feature.section.map(section_weights), axis=0).multiply(
            call_feature.statement_type.map(statement_type_weights), axis=0).sum()
        agg_feature_df.loc[call_uid] = agg_feature

    X = agg_feature_df.sort_index()

    # quantize excess return to -1, 0, 1 base on the quantile
    hp_stock_return_data = stock_return_data[stock_return_data.holding_period == holding_period]
    sell_excess_return = hp_stock_return_data.excess_return\
        .quantile(sell_quantile)
    buy_excess_return = hp_stock_return_data.excess_return\
        .quantile(buy_quantile)
    print('sell excess return threshold: ', sell_excess_return)
    print('buy excess return threshold: ', buy_excess_return)
    actions = hp_stock_return_data.excess_return.map(
        lambda x: 1 if x > buy_excess_return else -1 if x < sell_excess_return else 0)

    y = pd.DataFrame(
        actions.values, index=hp_stock_return_data.call_uid).sort_index()
    # consolidate to intersection of X.call_uid and y.call_uid
    intersection_call_uid = X.index.intersection(y.index)
    print(len(intersection_call_uid))
    X = X.loc[intersection_call_uid]
    y = y.loc[intersection_call_uid]

    print('Number of calls: ', len(y))
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Define the parameter grid for hyperparameter tuning
    if classifier == 'logistic_regression':
        param_grid = {
            'C': [0.1, 1.0, 10.0],
            'penalty': ['l1', 'l2'],
        }
        # Create Logistic Regression classifier
        classifier_obj = LogisticRegression()
    elif classifier == 'random_forest':
        param_grid = {
            'n_estimators': [100, 200, 500],
            'max_depth': [None, 5, 10],
        }
        # Create Random Forest classifier
        classifier_obj = RandomForestClassifier()
    elif classifier == 'neural_network':
        param_grid = {
            'hidden_layer_sizes': [(50, 25,), (100, 50,), (200, 100,)],
            'activation': ['logistic', 'tanh', 'relu'],
        }
        # Create Neural Network classifier
        classifier_obj = MLPClassifier()
    else:
        raise Exception('Invalid classifier')

    # Perform hyperparameter tuning using GridSearchCV with cross-validation
    print('Hyper-parameter Tuning')
    grid_search = GridSearchCV(
        estimator=classifier_obj, param_grid=param_grid, cv=5)
    grid_search.fit(X_train, y_train)

    # Get the best hyperparameters
    if classifier == 'logistic_regression':
        best_C = grid_search.best_params_['C']
        best_penalty = grid_search.best_params_['penalty']
        print(f'Best C: {best_C}, penalty type: {best_penalty}')
        print('Train Logistic Regression with best hyperparameters')
        classifer_best = LogisticRegression(
            C=best_C, penalty=best_penalty)
    elif classifier == 'random_forest':
        best_n_estimators = grid_search.best_params_['n_estimators']
        best_max_depth = grid_search.best_params_['max_depth']
        print(
            f'Best n_estimators: {best_n_estimators}, max_depth: {best_max_depth}')
        print('Train Random Forest with best hyperparameters')
        classifer_best = RandomForestClassifier(
            n_estimators=best_n_estimators, max_depth=best_max_depth)
    elif classifier == 'neural_network':
        best_hidden_layer_sizes = grid_search.best_params_[
            'hidden_layer_sizes']
        best_activation = grid_search.best_params_['activation']
        print(
            f'Best hidden_layer_sizes: {best_hidden_layer_sizes}, activation: {best_activation}')
        print('Train Neural Network with best hyperparameters')
        classifer_best = MLPClassifier(
            hidden_layer_sizes=best_hidden_layer_sizes, activation=best_activation)
    else:
        raise Exception('Invalid classifier')

    classifer_best.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = classifer_best.predict(X_test)

    # Print classification report
    print('Classification Report')
    print(classification_report(y_test, y_pred))

    # Save the model
    with open(save_model, 'wb') as f:
        pickle.dump(classifer_best, f)
