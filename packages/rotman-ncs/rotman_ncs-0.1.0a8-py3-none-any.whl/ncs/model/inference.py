'''
Run evaluation on the test set
'''
from .config import default_role_weights, default_section_weights, default_statement_type_weights
from ..data import load_call_statements
import pandas as pd
import os
import pickle
import warnings
warnings.filterwarnings('ignore')


cur_dir = os.path.dirname(os.path.realpath(__file__))

call_statement_data = load_call_statements('test')


def inference(feature_files=[],
              role_weights=default_role_weights,
              section_weights=default_section_weights,
              statement_type_weights=default_statement_type_weights,
              model_file='model.pkl',
              action_file='actions.csv'):
    """load features and model to generate actions of test set

    Args:
        feature_files (list, optional): a list of feature files index by call_uid. Defaults to [].
        model_file (str, optional): file path of trained model. Defaults to 'model.pkl'.
        action_file (str, optional): file path of actions to save. Defaults to 'actions.csv'.

    Returns:
        save actions to file action_file

    Content of action_file:
        call_uid,action
        f28cf056-f2df-4d94-ad36-4219506cd8b5,1
        f304ac10-f92c-404a-b3cc-f02ab8baa2c8,1
        22be863c-f8e5-4855-8523-44c6b398369b,1

    call_uid: unique identifier of the call in test set
    action: 1 for buy, -1 for sell, 0 for hold
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

    # load model
    with open(model_file, 'rb') as f:
        model = pickle.load(f)
    # generate actions
    actions = model.predict(agg_feature_df)
    actions = pd.DataFrame(
        {'call_uid': agg_feature_df.index, 'action': actions})
    actions.to_csv(action_file, index=False)
