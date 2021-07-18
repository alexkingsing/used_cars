import numpy as np
import streamlit as st
import time
import datetime
from tensorflow.python.keras.saving.save import load_model

from utils import *

#configs
st.set_page_config(layout="wide")

# Start
st.title("HERE COMES THE BOOM")
opt = st.sidebar.radio("Let's go!", ["Introduction","Price prediction"], )

# Loading model, categories and encoders.
model = load_model("Keras Model")
categorical_encoder, numerical_encoder = load_encoders()
base = load_categories()

# creating a separate array for MFG detection
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
    * Develop the selection side of the app

    STEP 4:
    * Encoder the information and perform prediction test

    STEP 5:
    * Create a plot showing the exact prediction and a range of MAX/MIN based on the models MAE.

    OPT STEP 6:
    * Look for an image of the vehicle and include it as part of the results.

    '''

else:

    st.subheader("To start, let's select a vehicle manufacturer and if we want a simple, or detailed query!")
    # Sub-columns to allow both decisions to be simultaneous.
    col1, col2 = st.beta_columns(2)
    with col1:
        mfg = st.selectbox("Manufacturer", options=mfg_base)
    with col2:
        detailed = st.radio(label = "Query type", options=["Simple query", "Detailed query"])

    if mfg != "":
        sliced_mfg = slice_categories(base, mfg)

        ## supporting variables  ((TRY TO CACHE THIS???))
        states = np.sort(sliced_mfg["state"].unique())
        model_list = np.sort(sliced_mfg["model"].unique())
        min_odo = sliced_mfg["odometer"].min().item()
        max_odo = sliced_mfg["odometer"].max().item()
        min_age = sliced_mfg["age"].min().item()
        max_age = sliced_mfg["age"].max().item()
        current_year = int(datetime.date.today().strftime("%Y"))

        ''' REUSE THIS SECTION LATER TO RUN THE PREDICTIONS
        ## adding an artificial 3 second wait to allow all supporting variables to load.
        # The first placeholder is a string to explain what's going on
        text_placeholder = st.empty()
        text_placeholder.text("Loading...")
        # The second placeholder is the progress bar
        progress_section = st.empty()
        with progress_section:
            prog_bar = st.progress(0)
            for second in range(1,4):
                progress = second * 33
                prog_bar.progress(progress)
                time.sleep(1)
        # clearing both placeholder.
        text_placeholder.empty()
        progress_section.empty()
        '''

        with st.form(key= "main_form"):
            # Simplified form is only the model, manufacture year & odometer (slider).
            # These are the default decisions regardless of any other user path.
            model_col, year_col, odometer_col, location = st.beta_columns(4)
            
            with model_col:
                model = st.selectbox(label= "Choose a model!", options= model_list)

            with year_col:
                # Since the base does not work with year, but with age, we will perform some transformations before continuing.
                min_year = current_year - max_age
                max_year = current_year - min_age
                age = st.slider(label= "Manufacture year", min_value= min_year, max_value= max_year, step = 1.00)
                age = current_year - age

            with odometer_col:
                odometer = st.slider(label="Odometer value in KM's", min_value=min_odo, max_value=max_odo, step=1.00)

            with location:
                state = st.selectbox(label= "Select your state!", options= states)

            if detailed == "Simple query": 
                ## If doing a simple query, I will just take the most common response for all the remainig columns
                condition = sliced_mfg["condition"].mode().iloc[0]
                cylinders = sliced_mfg["condition"].mode().iloc[0]
                fuel = sliced_mfg["fuel"].mode().iloc[0]
                transmission = sliced_mfg["transmission"].mode().iloc[0]
                drive = sliced_mfg["drive"].mode().iloc[0]
                type = sliced_mfg["type"].mode().iloc[0]
                color = sliced_mfg["paint_color"].mode().iloc[0]
            
            else:
                pass

            features = {"mfg":mfg, "model": model, "condition":condition, "cylinders": cylinders, "fuel":fuel, "trans": transmission,
                        "drive": drive, "type": type, "color": color, "odometer":odometer, "age": age}

            st.table(pd.DataFrame(features, index = [0]))
            
            st.form_submit_button(label= "Let's go!")
