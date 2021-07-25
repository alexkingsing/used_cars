import datetime
import time

import numpy as np
import streamlit as st
from tensorflow.python.keras.saving.save import load_model

from utils import *

#configs
st.set_page_config(layout="wide")

# Start
st.title("Used vehicles price prediction")
st.sidebar.subheader("Choose what you want to see!")
opt = st.sidebar.radio("", ["Introduction","Price prediction"], )

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

    st.write(load_intro("opening"))
    st.write(load_intro("body"))

    '''
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
        model_list = np.concatenate([np.array([""]), model_list])

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
            
            ## supporting variables for the simple general form
            min_odo = sliced_model["odometer"].min().item()
            max_odo = sliced_model["odometer"].max().item()
            min_age = sliced_model["age"].min().item()
            max_age = sliced_model["age"].max().item()
            current_year = int(datetime.date.today().strftime("%Y"))

            with st.form(key= "main_form"):
                # Simplified form is only the model, manufacture year & odometer (slider).
                # These are the default decisions regardless of any other user path.
                year_col, odometer_col = st.beta_columns(2)
                
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

                ############################################ SECTION SEPARATOR FOR VISIBILITY ############################################

                if detailed == "Simple query": 
                    ## If doing a simple query, I will just take the most common response for all the remaining columns
                    condition = sliced_model["condition"].mode().iloc[0]
                    cylinders = sliced_model["cylinders"].mode().iloc[0]
                    fuel = sliced_model["fuel"].mode().iloc[0]
                    transmission = sliced_model["transmission"].mode().iloc[0]
                    drive = sliced_model["drive"].mode().iloc[0]
                    car_type = sliced_model["type"].mode().iloc[0]
                    color = sliced_model["paint_color"].mode().iloc[0]
                    state = sliced_model["state"].mode().iloc[0]
                
                elif detailed == "Detailed query": ## THINK OF SOME SIMPLIFICATIONS IN THE CASE WHERE THERE'S ONLY ONE OPTION
                    detail_col1, detail_col2, detail_col3, detail_col4 = st.beta_columns(4)

                    with detail_col1:
                        condition = st.selectbox("Car's condition", options=sliced_model["condition"].unique())
                        cylinders = st.selectbox("Car's cylinders", options=sliced_model["cylinders"].unique())
                    
                    with detail_col2:
                        fuel = st.selectbox("Car's fuel", options=sliced_model["fuel"].unique())
                        state = st.selectbox("Buyer's state", options=sliced_model["state"].str.upper().unique())
                    
                    with detail_col3:
                        drive = st.selectbox("Drive type", options=sliced_model["drive"].unique())
                        transmission = st.selectbox("Transmission type", options=sliced_model["transmission"].unique())
                    
                    with detail_col4:
                        car_type = st.selectbox("Car type", options=sliced_model["type"].unique())
                        color = st.selectbox("Car's color", options=sliced_model["paint_color"].unique())
                

                features = {"mfg":mfg, "model": car_model, "condition":condition, "cylinders": cylinders, "fuel":fuel, "trans": transmission,
                            "drive": drive, "type": car_type, "color": color, "state": state, "odometer":odometer, "age": age}

                # Creating a dataframe if later on the user wants to see the form of the data being passed to the NN
                display_table = pd.DataFrame(features, index = [0])
                
                form = st.form_submit_button(label= "Let's go!")

            ############################################ SECTION SEPARATOR FOR VISIBILITY ############################################

            if form == True:
                
                ## adding an artificial 2 second for dramatic effect!
                # The first placeholder is a string to explain what's going on
                text_placeholder = st.empty()
                text_placeholder.text("Loading...")
                # The second placeholder is the progress bar
                progress_section = st.empty()
                with progress_section:
                    prog_bar = st.progress(0)
                    for second in range(1,3):
                        progress = second * 50
                        prog_bar.progress(progress)
                        time.sleep(1)
                # clearing both placeholder.
                text_placeholder.empty()
                progress_section.empty()
                
                array_to_predict = transform(display_table, categorical_encoder, numerical_encoder)
                prediction = model.predict(array_to_predict).item()            

                figure = plot(prediction, deviation)

                st.plotly_chart(figure, use_container_width = True) 


