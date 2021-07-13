import pandas as pd
import streamlit as st

from tensorflow.keras.models import load_model
from joblib import load, dump

model = load_model("Keras Model")

categorical_encoder = load("categorical_encoder.pkl")
numerical_encoder = load("numerical_encoder.pkl")

## dimensional characteristics -- > 11 dimensions

st.write(categorical_encoder.get_feature_names())  ### GET THE MANUFACTURERS AND MODELS FROM THE TABLES INSTEAD OF THE ENCODERS.

### EXPORT THE TABLE OF NUNIQUE? OR PERFORM MANUFACTURER-WISE QUERYING.