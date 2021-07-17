import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
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
    Take a base dataframe and slice it 

    Parameters
    ----------
    None

    Returns
    -------
    A tuple of encoders
    '''

    return base[base["manufacturer"] == filter]

def transform(data, cat_enc, num_enc) -> np.array:
    '''
    Function to transform input data into a prediction-ready array.

    Parameters
    ----------
    data: Iterable, numpy array or Pandas Dataframe holding the data needed for prediction.
    cat_enc: Pre-fit categorical encoder to transform the categorical features into integers via one-hot encoding.
    num_enc: Pre-fit encoder to transform numerical features into a scaled form.

    Returns
    -------
    a numpy array with the transformed array of data, prediction-ready.
    '''
    pass

def plot():
    pass
