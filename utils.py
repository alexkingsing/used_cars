import numpy as np
import pandas as pd
import plotly.graph_objects as go
from joblib import load
from streamlit import cache

import intro    

## COMPLETED
@cache  # caching all the loaders to avoid overhead lag
def load_intro(section: str) -> str:
    return intro.intro[section]

## COMPLETED
@cache  # caching all the loaders to avoid overhead lag
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
@cache  # caching all the loaders to avoid overhead lag
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
@cache # caching the filtered base so that it's only reloaded if the manufacturer is changed.
def slice_categories(base: pd.DataFrame, column: str, filter) -> pd.DataFrame:
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

    return base[base[column] == filter]

## COMPLETED
@cache # caching the filtered base so that it's only reloaded if the manufacturer is changed.
def detailed_view(base: pd.DataFrame, column: str):
    
    unique_elements = base[column].unique()

    if len(unique_elements) < 2:
        return base[column].unique().item()
    else:
        return base[column].unique()

## COMPLETED.
# Not worth caching as this func only runs at the end of a new data stream.
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

## COMPLETED
# Not worth caching as this func only runs at the end of a new data stream.
def plot(prediction, deviation):
    '''
    Function to create plotly-figure plot to display the results of the prediction.

    Parameters
    ----------
    Prediction: Target value predicted by the TF-Keras algorithm.
    Deviation: Expected error (RMSE) of the algorithm based on test values

    Returns
    -------
    A display-ready plotly figure.
    '''

    upper_bound = prediction + deviation
    lower_bound = prediction - deviation

    # I don't want any zero, close-to-zero, or negative lower bounds so let's add some logic here.
    if lower_bound < 1000:
        lower_bound = None
    else:
        pass

    if lower_bound is not None:
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=[1],
                y=[lower_bound],
                mode="markers",
                name="Minimum price",
                marker=dict(
                    color="green"
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[1],
                y=[prediction],
                mode="markers",
                name="Expected price",
                marker=dict(
                    color="black"
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[1],
                y=[upper_bound],
                mode="markers",
                name="Maximum price",
                marker=dict(
                    color="red"
                )
            )
        )

        # Horizontal delimeter for the lower bound
        fig.add_shape(
            type="line",
            x0=0,
            y0=lower_bound,
            x1=2,
            y1=lower_bound,
            line=dict(
                color="green",
                dash="dot"
            )
        )

        # Horizontal delimeter for the upper bound
        fig.add_shape(
            type="line",
            x0=0,
            y0=upper_bound,
            x1=2,
            y1=upper_bound,
            line=dict(
                color="red",
                dash="dot"
            )
        )
    
    ## This is the case when the lower bound is too small we'd rather ignore it.
    else:
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=[1],
                y=[prediction],
                mode="markers",
                name="Expected price",
                marker=dict(
                    color="black"
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[1],
                y=[upper_bound],
                mode="markers",
                name="Maximum price",
                marker=dict(
                    color="red"
                )
            )
        )

        # Horizontal delimeter for the upper bound
        fig.add_shape(
            type="line",
            x0=0,
            y0=upper_bound,
            x1=2,
            y1=upper_bound,
            line=dict(
                color="red",
                dash="dot"
            )
        )

    return fig
