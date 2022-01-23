import pandas as pd
import numpy as np
from operator import itemgetter



def create_dfs():
  readings_data={"Sensor1": [20.0, 20.1, 20.0], 
                "Sensor2": [19.4, 19.4, 19.4], 
                "Sensor3": [21.3, 21.2, 21.0], 
                "Sensor4": [20.5, 20.4, 20.6]}
  readings_index=pd.to_datetime(["2020-12-01 00:00:00", 
                                "2020-12-01 00:11:34", 
                                "2020-12-01 00:20:00"])
  prediction_data={"Sensor1": [np.nan, 20.2, 19.9, 20.0, 20.1], 
                  "Sensor2": [19.5, np.nan, 19.6,np.nan, np.nan], 
                  "Sensor3": [21.1, np.nan, np.nan, np.nan, np.nan], 
                  "Sensor4": [20.3, 20.2, 20.4, np.nan, 20.5]}
  prediction_index=pd.to_datetime(["2020-12-01 00:00:30", 
                                  "2020-12-01 00:07:24", 
                                  "2020-12-01 00:17:15", 
                                  "2020-12-01 00:19:00", 
                                  "2020-12-01 00:21:30"])
  reading_df=pd.DataFrame(readings_data, index= readings_index)
  prediction_df=pd.DataFrame(prediction_data, index= prediction_index)
  reading_df=add_timestamp_column(reading_df)
  prediction_df=add_timestamp_column(prediction_df)

  return reading_df, prediction_df

def add_timestamp_column(df):
  df["time_stamp"]=df.index
  df.reset_index(drop=True, inplace=True)
  # Below lines make sure that time_stamp column is the first among other columns
  df.set_index(df.columns[-1], inplace=True)
  df.reset_index(inplace=True)
  return df

def generate_random_dataframe(rows,start_date,frequency, flag):
  np.random.seed(123)
  column_name_list=["Sensor{0}".format(i) for i in range(1, 501)]
  date_range=pd.date_range(start_date, periods=rows, freq=frequency)
  random_dataframe=pd.DataFrame(np.random.uniform(18, 21, (rows, 500),), 
                                  columns= column_name_list, index=date_range)
  random_dataframe=add_timestamp_column(random_dataframe)
  
  if (flag=='reading'):
    return random_dataframe
  else:
    # This block adds random NaN values into the prediction datafram
    for col in column_name_list:
      random_dataframe.loc[random_dataframe.sample(frac=0.6).index, col]=np.nan
    return random_dataframe

def generate_response_dataframe(input_list, flag="test"): 
  if flag=="main":
    input_list.sort(key=lambda val: val[0])
    resp_df=pd.DataFrame(input_list, columns=['time_stamp', 'Sensor', 'Temperature', 'Prediction'])
    return resp_df
  else:
    input_list_flat=[item for sublist in input_list for item in sublist]
    input_list_flat.sort(key=lambda val: val[0])
    resp_df=pd.DataFrame(input_list_flat, columns=['time_stamp', 'Sensor', 'Temperature', 'Prediction'])
    return resp_df
