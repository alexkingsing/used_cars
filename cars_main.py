import datetime
from typing_extensions import final

import numpy as np
import streamlit as st
from tensorflow.python.keras.saving.save import load_model

from utils import *

#configs
st.set_page_config(layout="wide")

# Manually adding the RMSE of the Keras model for general purposes.
deviation = 2894.679202

# Loading model, categories and encoders.
model = load_model("Keras Model")
categorical_encoder, numerical_encoder = load_encoders()
base = load_categories()

# creating a separate array for MFG detection
mfg_base = base["manufacturer"].unique()
mfg_base = np.concatenate([np.array([""]), mfg_base]) # adding an empty value at the beginning so the user is forced to manually choose
mfg_base = np.sort(mfg_base)

# Start with titles and landing-page design.
st.title("U.S.A Used vehicles price prediction! (BETA)")
st.caption("Version 0.9")
st.sidebar.subheader("Choose what you want to see!")
opt = st.sidebar.radio("", ["Introduction","Price prediction", "Tool explanation"], )

## COMPLETED
if opt == "Introduction":

    # Intro start
    st.subheader(load_intro("opening"))
    st.write(load_intro("body1"))
    st.write(load_intro("disclaimer"))

    # Intro end
    st.write(load_intro("body2"))
    st.write(load_intro("body3"))

    # Notebook
    st.write(load_intro("notebook"))

    # Contact info
    st.write(load_intro("contact"))


            ############################################ SECTION SEPARATOR FOR VISIBILITY ############################################

## IN COMPLETED
elif opt == "Price prediction":
    st.subheader("To start, select a vehicle manufacturer and model!")
    # Sub-columns to allow both decisions to be in the same position.
    col1, col2 = st.beta_columns(2)

    with col1:
        # Storing the selected manufacturer.
        mfg = st.selectbox("Manufacturer", options=mfg_base, 
        help="Click on the dropdown a box and select a manufacturer! **It's the most important feature to determine a price**.")

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
                detailed = st.radio(label = "Query type", options=["Simple query", "Detailed query"], 
                help="A simple query only has 2 parameters to customize. A detailed query has 10 parameters!")
            
            ## supporting variables for the simple general form
            max_odo = sliced_model["odometer"].max().item()
            min_age = sliced_model["age"].min().item()
            max_age = sliced_model["age"].max().item()
            current_year = int(datetime.date.today().strftime("%Y"))
            
            ############################################ SECTION SEPARATOR FOR VISIBILITY ############################################
            with st.form(key= "main_form"):
                # Simplified form is only the model, manufacture year & odometer (slider).
                # These are the default decisions regardless of any other user path.
                year_col, odometer_col = st.beta_columns(2)
                
                with year_col:
                    # Since the base does not work with year, but with age, we will perform some transformations before continuing.
                    min_year = current_year - max_age # get the lower boundary by substracting the max age from the current year.
                    max_year = current_year - min_age # get the upper boundar by substracting the min age from current year.
                    if max_year <= min_year: # if the boundaries are equal or strange, set it to the closest time.
                        st.write(f"The manufacture year for this vehicle has been set to: **{max_year}**")
                        age = current_year - max_year 
                    else:
                        age = st.slider(label= "Manufacture year", min_value= min_year, max_value= max_year, step = 1.00,
                        help="Set the manufacture year for the vehicle. **This is the 2nd most important feature**! The older the car the more value it loses!")
                        age = current_year - age

                with odometer_col:
                    odometer = st.slider(label="Odometer value in miles", min_value=0.00, max_value=max_odo, step= 100.00,
                    help="The range of miles in the vehicles odometer. The higher this value, **the more value the car loses!**")

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
                
                elif detailed == "Detailed query":
                    detail_col1, detail_col2, detail_col3, detail_col4 = st.beta_columns(4)

                    with detail_col1:
                        condition = detailed_view(sliced_model, "condition")
                        if isinstance(condition, str) == True:
                            st.write(f"Car's condition has been set to **{condition}**")
                        else:
                            condition = st.selectbox("Car's condition", options=condition)
                        
                        cylinders = detailed_view(sliced_model, "cylinders")
                        if isinstance(cylinders, str) == True:
                            st.write(f"Car's cylinders have been set to **{cylinders}**")
                        else:
                            cylinders = st.selectbox("Car's cylinders", options=cylinders)
                    
                    with detail_col2:
                        fuel = detailed_view(sliced_model, "fuel")
                        if isinstance(fuel, str) == True:
                            st.write(f"Car's fuel type has been set to: **{fuel}**")
                        else:
                            fuel = st.selectbox("Car's fuel", options=fuel)
                        
                        state = detailed_view(sliced_model, "state")
                        state = st.selectbox("Buyer's state", options=state)
                    
                    with detail_col3:
                        drive = detailed_view(sliced_model, "drive")
                        if isinstance(drive, str) == True:
                            st.write(f"Car's drive type has been set to: **{drive}**")
                        else:
                            drive = st.selectbox("Drive type", options=drive)
                        
                        transmission = detailed_view(sliced_model, "transmission")
                        if isinstance(transmission, str) == True:
                            st.write(f"Transmission type set to: **{transmission}**")
                        else:
                            transmission = st.selectbox("Transmission type", options=transmission)
                    
                    with detail_col4:
                        car_type = detailed_view(sliced_model, "type")
                        if isinstance(car_type, str) == True:
                            st.write(f"Car's type has been set to: **{car_type}**")
                        else:
                            car_type = st.selectbox("Car type", options=car_type)
                        
                        color = detailed_view(sliced_model, "paint_color")
                        if isinstance(color, str) == True:
                            st.write(f"Car's color has been set to: **{color}**")
                        else:
                            color = st.selectbox("Car's color", options=color)
                

                features = {"mfg":mfg, "model": car_model, "condition":condition, "cylinders": cylinders, "fuel":fuel, "trans": transmission,
                            "drive": drive, "type": car_type, "color": color, "state": state, "odometer":odometer, "age": age}

                # Creating a dataframe if later on the user wants to see the form of the data being passed to the NN
                display_table = pd.DataFrame(features, index = [0])
                
                form = st.form_submit_button(label= "Let's go!")

            ############################################ SECTION SEPARATOR FOR VISIBILITY ############################################

            if form == True:
                
                array_to_predict = transform(display_table, categorical_encoder, numerical_encoder)
                prediction = model.predict(array_to_predict).reshape(1)
                upper_limit = (prediction + (2*deviation)).reshape(1)
                lower_limit = (prediction - (2*deviation)).reshape(1)
                
                #  Setting a dataframe for easier solution rendering.
                upper_limit = pd.DataFrame(
                    {'Maximum price': upper_limit}, index=[""])
                #  Setting a dataframe for easier solution rendering.
                prediction = pd.DataFrame(
                    {'Expected price': prediction}, index=[""])
                #  Setting a dataframe for easier solution rendering.
                lower_limit = pd.DataFrame(
                    {'Minimum price': lower_limit}, index=[""])

                #v2 change: Instead of plot, tables.
                final1, final2, final3 = st.beta_columns(3)

                with final1:
                    st.table(upper_limit)
                
                with final2:
                    st.table(prediction)

                with final3:
                    st.table(lower_limit)

## PENDING
elif opt == "Tool explanation":

    st.header("*SECTION CURRENTLY UNDER CONSTRUCTION...*")

    # ML SECTION
    st.write(load_exp("intro"))
    st.header(load_exp("ml_title"))

    exp_col1, exp_col2 = st.beta_columns(2)
    with exp_col1:
        st.write(load_exp("ml_intro"))
        button = st.button("Tell me!")
    if button == True:
        with exp_col2:
            st.image(load_exp("horse"))
    st.write(load_exp("ml_close"))

    # MODEL INTRO SECTION
    st.header(load_exp("model_title"))
    st.write(load_exp("model_intro"))
    st.image(load_exp("model_image"), caption="The Neural Network powering your queries!", width=750)

    # MODEL INPUTS SECTION
    st.header(load_exp("model_inputs_title"))

    st.table(np.array([["Car manufacturer","Car model", "Manufacture year", "Odometer", "Car's condition", "Fuel type", "Drive type",
    "Car's type", "Car's cylinders", "Buyer's state", "Transmission type", "Car's color"]]))
