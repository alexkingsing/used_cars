import datetime

import numpy as np
import streamlit as st
from tensorflow.python.keras.saving.save import load_model

from utils import *

#configs
st.set_page_config(layout="wide")

# Start
st.title("COOL TITLE FOR COOL APP")
opt = st.sidebar.radio("Let's go!", ["Introduction","Price prediction"], )

# Manually adding the RMSE of the Keras model for plot use.
deviation = 2894.679202

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

    OPT STEP 6:
    * Look for an image of the vehicle and include it as part of the results.

    '''

else:
    st.subheader("To start, select a vehicle manufacturer and model!")
    # Sub-columns to allow both decisions to be in the same position.
    col1, col2 = st.beta_columns(2)

    with col1:
        # Storing the selected manufacturer.
        mfg = st.selectbox("Manufacturer", options=mfg_base)

    if mfg != "":
        # Delimit the current running table based on the MFG choice
        sliced_mfg = slice_categories(base, "manufacturer", mfg)

        # extract the list of known models for the MFG
        model_list = np.sort(sliced_mfg["model"].unique())

        with col2:
            # Storing the selected model
            car_model = st.selectbox(label="Choose a model!", options=model_list)
            
        if car_model != "":
            # Do one final slice of the current table based on model.
            sliced_model = slice_categories(sliced_mfg, "model", car_model)

            # Final instructions
            st.subheader("Finally, decide if you prefer a simple or detailed decision.")

            # creating a column division to make it look better.
            col3, placeholder1, placeholder2 = st.beta_columns(3)

            with col3:
                detailed = st.select_slider(label = "Query type", options=["Simple query", "Detailed query"])
            
            ## supporting variables  ((TRY TO CACHE THIS???))@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            states = np.sort(sliced_model["state"].unique())
            min_odo = sliced_model["odometer"].min().item()
            max_odo = sliced_model["odometer"].max().item()
            min_age = sliced_model["age"].min().item()
            max_age = sliced_model["age"].max().item()
            current_year = int(datetime.date.today().strftime("%Y"))

            with st.form(key= "main_form"):
                # Simplified form is only the model, manufacture year & odometer (slider).
                # These are the default decisions regardless of any other user path.
                year_col, odometer_col, location = st.beta_columns(3)
                
                with year_col:
                    # Since the base does not work with year, but with age, we will perform some transformations before continuing.

                    min_year = current_year - max_age
                    max_year = current_year - min_age

                    if max_year <= min_year:
                        st.write(f"The manufacture year for this vehicle has been set to:")
                        st.write(max_year)
                        age = current_year - max_year 
                    else:
                        age = st.slider(label= "Manufacture year", min_value= min_year, max_value= max_year, step = 1.00)
                        age = current_year - age

                with odometer_col:
                    odometer = st.slider(label="Odometer value in KM's", min_value=min_odo, max_value=max_odo, step=1.00)

                with location:
                    state = st.selectbox(label= "Select your state!", options= states)

                if detailed == "Simple query": 
                    ## If doing a simple query, I will just take the most common response for all the remaining columns
                    condition = sliced_model["condition"].mode().iloc[0]
                    cylinders = sliced_model["condition"].mode().iloc[0]
                    fuel = sliced_model["fuel"].mode().iloc[0]
                    transmission = sliced_model["transmission"].mode().iloc[0]
                    drive = sliced_model["drive"].mode().iloc[0]
                    car_type = sliced_model["type"].mode().iloc[0]
                    color = sliced_model["paint_color"].mode().iloc[0]
                
                ## MISSING THE SUPER DETAILED VIEW @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                else:
                    pass

                features = {"mfg":mfg, "model": car_model, "condition":condition, "cylinders": cylinders, "fuel":fuel, "trans": transmission,
                            "drive": drive, "type": car_type, "color": color, "state": state, "odometer":odometer, "age": age}

                display_table = pd.DataFrame(features, index = [0])
                
                form = st.form_submit_button(label= "Let's go!")
            
            if form == True:

                array_to_predict = transform(display_table, categorical_encoder, numerical_encoder)
                prediction = model.predict(array_to_predict).item()            

                figure = plot(prediction, deviation)

                st.plotly_chart(figure, use_container_width = True) 

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
