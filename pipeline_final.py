import pandas as pd
import numpy as np
from sqlalchemy import *
import holidays
# Ask for DB credentials
USERNAME = input("Enter your MySQL username: ")
PASSWORD = input("Enter your MySQL password: ")


df_fl = pd.read_csv("flights.csv", low_memory=False)
df_al = pd.read_csv("airlines.csv")
df_ap = pd.read_csv("airports.csv")

# Drop unused columns
df_fl = df_fl.drop(["DIVERTED",
            "CANCELLATION_REASON",
            "AIR_SYSTEM_DELAY",
            "SECURITY_DELAY",
            "AIRLINE_DELAY",
            "LATE_AIRCRAFT_DELAY",
            "WEATHER_DELAY",
            "WHEELS_OFF",
            "TAXI_OUT",
            "ELAPSED_TIME",
            "AIR_TIME",
            "DISTANCE",
            "WHEELS_ON",
            "TAXI_IN",
            "SCHEDULED_ARRIVAL",
            "ARRIVAL_TIME",
            "ARRIVAL_DELAY",
            "SCHEDULED_TIME"
           ],
           axis=1)
#Filter only positive delay values
df_fl["DEPARTURE_DELAY"] = df_fl["DEPARTURE_DELAY"].fillna(0)
#df_fl["DEPARTURE_DELAY"] = df_fl["DEPARTURE_DELAY"].clip(lower=0).astype(int)
df_fl=df_fl[df_fl["DEPARTURE_DELAY"] >0].copy()

#Manage noisy data in the AIRPORT IATA CODES from flight csv

df_fl = df_fl[
    df_fl["ORIGIN_AIRPORT"].astype(str).str.match(r'^[A-Z]{3}$')
].copy()

df_fl = df_fl[
    df_fl["DESTINATION_AIRPORT"].astype(str).str.match(r'^[A-Z]{3}$')
].copy()

# Manage nulls in tail_number
df_fl["TAIL_NUMBER"] = df_fl["TAIL_NUMBER"].fillna("000000")

# Convert flight_number to str of fixed lenght
df_fl["FLIGHT_NUMBER"] = df_fl["FLIGHT_NUMBER"].fillna(0).astype(int).astype(str).str.zfill(4)

# Generate flight_id
df_fl['flight_id'] = df_fl['AIRLINE'] + '-' + df_fl['FLIGHT_NUMBER'] + '-' + df_fl['TAIL_NUMBER']
# Flight date in date format
df_fl["FLIGHT_DATE"] = pd.to_datetime(df_fl[["YEAR", "MONTH", "DAY"]]).dt.strftime("%Y-%m-%d")

df_fl["date_id"] = pd.to_datetime(df_fl[["YEAR", "MONTH", "DAY"]]).dt.strftime("%Y%m%d").astype(int)

# Remove cancelled flights
df_fl = df_fl.loc[df_fl["CANCELLED"] != 1]
df_fl = df_fl.drop(columns=["CANCELLED"])

# Get is_holiday
min_year = pd.to_datetime(df_fl['FLIGHT_DATE']).dt.year.min()
max_year = pd.to_datetime(df_fl['FLIGHT_DATE']).dt.year.max()
us_holidays = holidays.US(years=range(min_year, max_year + 1))

df_fl['is_holiday'] = pd.to_datetime(df_fl['FLIGHT_DATE']).dt.date.isin(us_holidays)


# Match airline code/airline name with their names
mapping = dict(zip(df_al["IATA_CODE"], df_al["AIRLINE"]))
df_fl["AIRLINE_NAME"] = df_fl["AIRLINE"].map(mapping)


df_ap=df_ap.drop(['COUNTRY','LATITUDE','LONGITUDE'],axis=1)


def format_hhmm(col):
    # Convert to string, pad with zeros, and coerce invalids to NaT
    s = col.astype("Int64").astype(str).str.zfill(4)
    s = s.replace("<NA>", pd.NA)

    # Convert to datetime and format as HH:MM
    return pd.to_datetime(s, format="%H%M", errors="coerce").dt.strftime("%H:%M")
df_fl["DEPARTURE_TIME"] = format_hhmm(df_fl["DEPARTURE_TIME"])
df_fl["SCHEDULED_DEPARTURE"] = format_hhmm(df_fl["SCHEDULED_DEPARTURE"])


# Create time dataframe for "time" dimensional table
def get_period_of_day(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

minutes_in_day = range(24 * 60)  # 0 to 1439
data = []

for _, total_min in enumerate(minutes_in_day, start=1):
    hour = total_min // 60
    minute = total_min % 60
    full_time = f"{hour:02d}:{minute:02d}:00"
    period = get_period_of_day(hour)
    time_id = f"{hour:02d}:{minute:02d}"
    data.append((time_id, full_time, hour, minute, period))


df_time = pd.DataFrame(
    data, columns=["time_id", "full_time", "hour_of_day", "minute_of_hour", "period_of_day"]
)

# Rename columns
df_fl = df_fl.rename(columns={
    'FLIGHT_DATE': 'full_date',
    'AIRLINE': 'airline_code',
    'AIRLINE_NAME': 'airline_name',
    'FLIGHT_NUMBER': 'flight_number',
    'TAIL_NUMBER': 'tail_number',
    'ORIGIN_AIRPORT': 'origin_airport',
    'DESTINATION_AIRPORT': 'destination_airport',
    'SCHEDULED_DEPARTURE': 'scheduled_departure',
    'DEPARTURE_TIME': 'departure_time',
    'DEPARTURE_DELAY': 'departure_delay'
})


df_flight_info = df_fl[['flight_id', 'airline_code', 'airline_name', 'flight_number', 'tail_number']]
df_flight_info = df_flight_info.drop_duplicates()

df_date = df_fl[['date_id', 'full_date', 'is_holiday']]
df_date = df_date.drop_duplicates()
df_time = df_time.drop_duplicates()


#################
# LOAD into mysql
#################
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@127.0.0.1:3306/flight_delays")


# dim_date table
df_date[['date_id', 'full_date', 'is_holiday']].drop_duplicates(subset=['full_date']) \
    .to_sql(
    'dim_date',
    con=engine,
    if_exists='append',
    index=False,
    dtype={
        'date_id': Integer(),
        'full_date': Date(),
        'is_holiday': Boolean()
    }
)

# dim_time table
df_time[['time_id', 'full_time', 'hour_of_day', 'minute_of_hour', 'period_of_day']] \
    .to_sql(
    'dim_time',
    con=engine,
    if_exists='append',
    index=False,
    dtype={
        'time_id': VARCHAR(5),
        'full_time': Time(),
        'hour_of_day': Integer(),
        'minute_of_hour': Integer(),
        'period_of_day': VARCHAR(10)
    }
)

# dim_airport table
df_ap[['IATA_CODE', 'AIRPORT', 'STATE', 'CITY']] \
    .rename(columns={'IATA_CODE': 'airport_id'}) \
    .rename(columns={'AIRPORT': 'airport_name'}) \
    .rename(columns={'STATE': 'state'}) \
    .rename(columns={'CITY': 'city'}) \
    .to_sql(
    'dim_airport',
    con=engine,
    if_exists='append',
    index=False,
    dtype={
        'airport_id': VARCHAR(5),
        'airport_name': VARCHAR(100),
        'state': VARCHAR(4),
        'city': VARCHAR(50)
    }
)

# dim_flight_info table
df_flight_info[['flight_id', 'airline_code', 'airline_name', 'flight_number', 'tail_number']] \
    .to_sql(
    'dim_flight_info',
    con=engine,
    if_exists='append',
    index=False,
    dtype={
        'flight_id': VARCHAR(20),
        'airline_code': CHAR(2),
        'airline_name': VARCHAR(35),
        'flight_number': CHAR(4),
        'tail_number': VARCHAR(10)
    }
)

# fact_delay table
df_fl[['flight_id', 'date_id', 'scheduled_departure', 'departure_time', 'origin_airport', 'destination_airport', 'departure_delay']] \
    .rename(columns={'scheduled_departure': 'hour_scheduled_id'}) \
    .rename(columns={'departure_time': 'hour_departure_id'}) \
    .rename(columns={'origin_airport': 'origin_airport_id'}) \
    .rename(columns={'destination_airport': 'destination_airport_id'}) \
    .to_sql(
    'fact_delay',
    con=engine,
    if_exists='append',
    index=False,
    dtype={
        'flight_id': VARCHAR(20),
        'date_id': Integer(),
        'hour_scheduled_id': VARCHAR(5),
        'hour_departure_id': VARCHAR(5),
        'origin_airport_id': VARCHAR(5),
        'destination_airport_id': VARCHAR(5),
        'departure_delay': Integer()
    }
)



