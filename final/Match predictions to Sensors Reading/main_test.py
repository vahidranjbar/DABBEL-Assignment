from unittest import result
import pandas as pd
import numpy as np
from datetime import timedelta
from utils import generate_random_dataframe, generate_response_dataframe
from multiprocessing import Pool
import time
from operator import itemgetter
import warnings
warnings.filterwarnings("ignore")


# NEW get_result
def get_result(sensor):    
# For the sake of performance, instead of working with dataframe, all recoreds associated with each Sensor 
# will be converted into dictionary objects
  # NOte: Complexity: O(N)  
  sensor_reading_list=[{"time_stamp": record["time_stamp"], 
                        "Sensor": record[sensor], 
                        "flag": record["flag"]} 
                        for record in reading_dict_list]
  # NOte: Complexity: O(N)
  sensor_prediction_list=[{"time_stamp": record["time_stamp"], 
                          "Sensor": record[sensor], 
                          "flag": record["flag"]} 
                          for record in prediction_dict_list if not np.isnan(record[sensor])]
  # To reduce the computation cost Null values will be dropped from the prediction dataframe,  
  # sensor_prediction_df.dropna(inplace=True)
  records_in_sensor_prediction_list=len(sensor_prediction_list)
  temp_list=sensor_reading_list+sensor_prediction_list
  # Sort the combined list of both sensor_prediction_list and sensor_reading_list
  #  with respect to time_stamp
  # NOte: Complexity: O(NLogN)
  temp_list_sorted=sorted(temp_list, key=itemgetter('time_stamp'))
  dist_list=[]
  # NOte: Complexity: O(N)
  for i in range(0, len(temp_list_sorted)-1):
    current_record=temp_list_sorted[i]
    current_record_flag=current_record["flag"]
    next_record=temp_list_sorted[i+1]
    next_record_flag=next_record["flag"]
    # If current_record_flag and next_record_flag are the same it means both records are
    # from the same table and not required to calculate the distance between them, 
    # otherwise calculate the distance and add a new tuple into the distance list
    if(current_record_flag!=next_record_flag):
        # Create a tuple with this structure and add it to the list: 
        # ("reading_timestamp", "prediction_timestamp", "reading_value", "prediction_value", "distance")
      if(current_record_flag=="R"):
        dist_list.append((current_record["time_stamp"],sensor, 
                          current_record["Sensor"], 
                          next_record["Sensor"],
                          abs(next_record["time_stamp"]-current_record["time_stamp"])))
      else:
        dist_list.append((next_record["time_stamp"], sensor, 
                          next_record["Sensor"], 
                          current_record["Sensor"],                                   
                          abs(current_record["time_stamp"]-next_record["time_stamp"])))
  # Sort the dist_list with regards to distance in ASC order
  # NOte: Complexity: O(NLogN)
  dist_list.sort(key=lambda val: val[4])
  final_response_list=[]
  # this flag_obj makes sure no duplicate reading_time_stamp gets populated into the final_response_list
  flag_obj={"time_stamp":None}
  if(records_in_sensor_prediction_list <= len(dist_list)):
    for i in range(0, records_in_sensor_prediction_list):
      if (dist_list[i][0]!=flag_obj["time_stamp"]):
        flag_obj["time_stamp"]=dist_list[i][0]
        final_response_list.append(dist_list[i][0:4])
  else:
    for i in range(0, len(dist_list)):
      if (dist_list[i][0]!=flag_obj["time_stamp"]):
        flag_obj["time_stamp"]=dist_list[i][0]
        final_response_list.append(dist_list[i][0:4])
# In general, for each Sensor, the time complexity of this function is O(NLogN).
# Considering the number of sensors(M), the total time complexity will be O(MNLogN)
  return final_response_list
  

if __name__=="__main__":
  """
    Other than achieving the main GOAL of this assignment, there are two questions that I would
    like to answer here:
      Q1. Which data structure has been selected in this solution, Why?
        Answer: In this solution I prefered to work with dictionaries rather than dataframes. 
        Dictionaries are less structured and in case of large scale datasets they are more 
        favorable than dataframes and that is one of the reasons why in the big data realm 
        such database systems like MongoDb (with its building blocks components as Collections 
        and JSON objects(documents)) is widely used.

      Q2. What is the computational complexity of your solution?
        Answer: As it is highlighted in the context of the code, In general, for each Sensor, 
        the time complexity of the provided solution is O(NLogN). Considering the number of sensors(M),
        the total time complexity will be O(MNLogN)
  """
  prediction_df=generate_random_dataframe(15000, "2015-02-01 00:00:30","23S", "prediction")
  prediction_df["flag"]='P'
  reading_df=generate_random_dataframe(3000, "2015-02-01 00:00:00","17S", "reading")
  reading_df["flag"]='R'
  sensor_list=reading_df.columns[1:-1] 
  # convert Dataframe into a list of dictionaries 
  reading_dict_list=reading_df.to_dict(orient='records')
  prediction_dict_list=prediction_df.to_dict(orient='records')
      
  print("Process started!!")
  t1=time.time()
  # These lines of code implement some kind of Map-Reduce logic. In another word, the task is first distributed across
  # available core processes (Map) then after the result will get reverted back into the main process (Reduce).
  pool=Pool()
  result_list=pool.map(get_result, sensor_list)
  pool.close()
  pool.join()
  print(time.time()-t1)
  print("Process finished!!")  

  response_dataframe=generate_response_dataframe(result_list)
  print(response_dataframe.head(10))
    
    
    


