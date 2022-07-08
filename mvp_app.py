import streamlit as st
from ResyBot_class import ResyBot
from ResyLogin import ResyLogin
import pandas as pd
import numpy as np
import functools
from datetime import date, datetime, timedelta

days_of_week = {
    6: "Sunday",
    5: "Saturday",
    4: "Friday",
    3: "Thursday",
    2: "Wednesday",
    1: "Tuesday",
    0: "Monday"
}

user_email = st.text_input(label="enter your Resy email", value="elijahflomen@gmail.com")
user_password = st.text_input(label="enter your Resy password", value="nfn!hyp!nyx_ymp5KXC")
login_button = st.button("connect to Resy")
if user_email and user_password and login_button:
    resy_login = ResyLogin(username=user_email, password=user_password)
    auth, payment = resy_login.login()
    if auth and payment:
        st.write(f"successfully logged in {user_email}")

rest_df = pd.read_csv("venue_data.csv").drop_duplicates()
rest_df.location = rest_df.location.str.lower()

rest_names = rest_df.name.unique()
st.write(f"Our data holds {len(rest_names)} restaurants")
rest_locations = rest_df.location.unique()
rest_types = rest_df.food.unique()
prices = {1: '$', 2:'$$', 3:'$$$', 4:'$$$$'}

user_start_date = st.date_input(label="start date", value=datetime.strptime("2022-07-21", '%Y-%m-%d'))
user_end_date = st.date_input(label="end date",  value=datetime.strptime("2022-07-21", '%Y-%m-%d'))

num_reservations = st.number_input(label="how many reservations would you like to make this week?", value=1)

avoid_dates = st.multiselect(label="are there any days of the week that week you are not available: ", options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
user_party_size = st.number_input(label="party size", value=2)

res_prefs = {}

st.write(f"Please enter your preferences for this week's {num_reservations} reservations")
input_locations = st.multiselect(options=rest_locations, label=f"Neighbourhoods for res 1", default=rest_locations)
input_food = st.multiselect(options=rest_types, label=f"Cuisines for res 1", default=rest_types)

price_1 = st.checkbox(prices[1], value=True)
price_2 = st.checkbox(prices[2], value=True)
price_3 = st.checkbox(prices[3], value=True)
price_4 = st.checkbox(prices[4], value=True)

input_prices = []

if price_1: input_prices.append(1)
if price_2: input_prices.append(2)
if price_3: input_prices.append(3)
if price_4: input_prices.append(4)

def convert_dt_str(dt):
    return dt.strftime("%Y-%m-%d")

dates_to_keep = []
min_avg_rating = st.slider(min_value=0.0,max_value=5.0, step=0.1, label="Min. average rating", value=3.5)
dates_list = (pd.date_range(user_start_date,user_end_date-timedelta(days=1),freq='d'))
for i, date in enumerate(dates_list):
    day_of_week = datetime.weekday(date)
    string_day = days_of_week[day_of_week]
    if string_day not in avoid_dates:
        dates_to_keep.append(date)
    else:
        continue

str_dates_to_keep = list(map(convert_dt_str, dates_to_keep))
print("Dates to consider for tables: ", str_dates_to_keep)

find_me_food = st.button("Find me reservations")
if find_me_food:
    def conjunction(*conditions):
        return functools.reduce(np.logical_and, conditions)

    c_1 = rest_df.location.isin(input_locations)
    c_2 = rest_df.food.isin(input_food)
    c_3 = rest_df.price.isin(input_prices)
    c_4 = rest_df.avg_rating >= min_avg_rating

    if input_food and input_locations:
        rest_data_filtered = rest_df[conjunction(c_1,c_2, c_3, c_4)]
        st.dataframe(rest_data_filtered)
        restaurant_open_tables = []
        # pick any random 2 restaurants that fit the user filters
        rest_data_filtered = rest_data_filtered.sample(2)
        # Now, for each option, lets see what their availabilties are on each day of their range
        for option in rest_data_filtered.index:
            restaurant_id = rest_data_filtered.loc[option, "id"]
            restaurant_name = rest_data_filtered.loc[option, "name"]
            restaurant_times = {}
            restaurant_times["venue_id"] = restaurant_id
            restaurant_times["venue_name"] = restaurant_name
            restaurant_times["dates_times"] = {}
            for date in str_dates_to_keep:
               
                # need to make a new bot for each date... this is stupid, change the class to accept a list of dates
                res_bot = ResyBot(
                    res_date=date,
                    party_size=user_party_size,
                    venue_id=restaurant_id,
                    table_time="19:30"
                )
                resy_login = ResyLogin(username=user_email, password=user_password)
                auth, payment = resy_login.login()
                best_table = res_bot.find_table(auth_token=auth, venue_id=restaurant_id)
                reservation_options = {}
                if best_table:
                    print(f"Found table for {restaurant_name} on {date}")
                    time_options = best_table["date"]["start"].split(" ")[1]
                    restaurant_times["dates_times"][date] = [time_options]
                    restaurant_open_tables.append(restaurant_times)
                else:
                    print(f"No table found for {restaurant_name} on {date}")
                    continue
        
    if restaurant_open_tables:
        user_selections_list = []
        st.write("Here are some options we think you would like")

        for restaurant in restaurant_open_tables:
            print(restaurant, "\n")
            st.header(restaurant.get("venue_name"))
            selection = st.selectbox(label=f"res options for {restaurant.get('venue_name')}", options=restaurant.get("dates_times").items(), key=str(restaurant.get("venue_name")))
                
    else:
        st.write("No tables found 😢")

            # for restautant, table in restaurant_open_tables.items():
            #     restaurant_name = rest_data_filtered[rest_data_filtered.id==restautant].name.values[0]
            #     st.write(f"{restaurant_name} has an opening for {user_party_size} on {user_start_date} at {table['date']['start']}")



