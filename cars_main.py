import streamlit as st
import numpy as np
from utils import *
from tensorflow.python.keras.saving.save import load_model

#configs
st.set_page_config(layout="wide")

# Start
st.title("HERE COMES THE BOOM")
opt = st.sidebar.radio("Let's go!", ["Introduction","Price prediction"], )

# Loading model, categories and encoders.
model = load_model("Keras Model")
categorical_encoder, numerical_encoder = load_encoders()
base = load_categories()

# creating a separate array for MFG
mfg_base = base["manufacturer"].unique()
mfg_base = np.concatenate([np.array([""]), mfg_base]) # adding an empty value at the beginning so the user is forced to manually choose
mfg_base = np.sort(mfg_base)

if opt == "Introduction":

    '''
    STEP 1:
    * Create a small introduction page explaining what the project is, where it came from (in summary) and describe what the project
    is going to do.

    STEP 2: 
    * Create supporting functions so that the front-end side of the application is not loaded with too many options.
    * Cache as many things as possible.

    STEP 3:
    * Decide if using a FORM or using SIDEBAR is more intuitive.
    * Develop the selection side of the app

    STEP 4:
    * Retrieve the relevant categorical / numerical information from the FORM/SIDEBAR
    * Encoder the information and perform prediction test

    STEP 5:
    * Create a plot showing the exact prediction and a range of MAX/MIN based on the models MAE.

    OPT STEP 6:
    * Look for an image of the vehicle and include it as part of the results.

    '''

else:
    st.subheader("To start, let's select a vehicle manufacturer!")
    mfg = st.selectbox("Manufacturer", options=mfg_base)

    if mfg != "":
        sliced_base = slice_categories(base, mfg)

        with st.form(key= "main_form"):
            st.selectbox(label= "OPTION", options= ["TEST1", "TEST2"])
            st.form_submit_button(label= "Let's go!")
