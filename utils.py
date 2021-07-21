import numpy as np
import pandas as pd
from pandas.core.arrays import categorical
import streamlit as st
from joblib import load


## COMPLETED
@st.cache  # caching all the loaders to avoid overhead lag
def load_encoders() -> tuple:
    '''
    A simple function to mask and simplify the loading of both encoders.
    
    Parameters
    ----------
    None

    Returns
    -------
    A tuple of encoders 
    '''

    categorical_encoder = load("categorical_encoder.pkl")
    numerical_encoder = load("numerical_encoder.pkl")

    return categorical_encoder, numerical_encoder

## COMPLETED
@st.cache  # caching all the loaders to avoid overhead lag
def load_categories() -> pd.DataFrame:
    '''
    This function loads the dataframe that contains the labels used during training of the model.
    All manufacturers and models not included in this dataframe are not supported by this project.

    Parameters
    ----------
    None

    Returns
    -------
    A tuple of encoders
    '''
    sample_base = load("categories_file.pkl")

    return sample_base

## COMPLETED
@st.cache # caching the filtered base so that it's only reloaded if the manufacturer is changed.
def slice_categories(base: pd.DataFrame, filter) -> pd.DataFrame:
    '''
    Take a base dataframe and slice it based on the filter.
    This function caches the result of the slice so that if attributes other than the filter are changed the base is not reloaded.

    Parameters
    ----------
    base: A Pandas dataframe that holds the base data.
    filter: String that filters the manufacturer column.

    Returns
    -------
    A sliced-off Pandas Dataframe.
    '''

    return base[base["manufacturer"] == filter]

def transform(data, cat_enc, num_enc) -> np.array:
    '''
    Function to transform input data into a prediction-ready array.

    Parameters
    ----------
    data: Pandas Dataframe holding the data needed for prediction.
    cat_enc: Pre-fit categorical encoder to transform the categorical features into integers via one-hot encoding.
    num_enc: Pre-fit encoder to transform numerical features into a scaled form.

    Returns
    -------
    a numpy array with the transformed array of data, prediction-ready.
    '''
    
    # Extracting the features from the parent dataframe based on their type
    categorical_vars = data.select_dtypes(include= "object")
    numerical_vars= data.select_dtypes(exclude = "object")

    # Since we are only doing one prediction at a time, let's do the dimensional transformation right away
    categorical_vars = categorical_vars.to_numpy().reshape(1, -1)
    numerical_vars = numerical_vars.to_numpy().reshape(1, -1)

    categorical_vars = cat_enc.transform(categorical_vars)
    numerical_vars = num_enc.transform(numerical_vars)

    result_array = np.concatenate([categorical_vars, numerical_vars], axis=1)

    return result_array

def plot():
    pass
