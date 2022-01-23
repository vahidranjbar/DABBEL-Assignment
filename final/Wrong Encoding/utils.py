import re
import json

def process_json_file():
  """[summary]
    This function loads the provided JSON file and goes through all the
    KEYs and their respected VALUEs and pretifies the string values.
    The list of KEYs upon which this function iterates is as below:
     -objects: The value associated to this key holdes all the required data
       -"Vendor Proprietary Value"
       -"analog-input"
       -"analog-output"
       -"analog-value"
       -"binary-input"
       -"binary-output"
       -"binary-value"
       -"multi-state-value"
       -"notification-class"
       -"pulse-converter"
       -"schedule"
       -"device"
    Note: 
      The string VALUEs associated with each one of these keys have the same properties EXCEPT for "device". 
      For example, this is one sample object under "Vendor Proprietary Value":
         "properties": {
            "active-text": null,
            "cov-increment": null,
            "description": "\"\"",
            "inactive-text": null,
            "number-of-states": null,
            "object-identifier": "Vendor Proprietary Value:1",
            "object-name": "\".H.E.I.Z.G.R.U.P.P.E\"",
            "object-type": 130,
            "out-of-service": null,
            "present-value": null,
            "priority-array": null,
            "resolution": null,
            "state-text": null,
            "status-flags": null,
            "units": null
        }
      while the object under "device" looks like this:
        "properties": {
            "apdu-timeout": 3000,
            "description": "\".H.e.i.z.b.e.r.t.e.i.l.u.n.g. .T.r.a.k.t. .C\"",
            "location": "\".R.C.Z./.A./.U.G.1./.A.U.2.2./.0.1.4.2\"",
            "max-apdu-length-accepted": 480,
            "model-name": "\".X.L.W.e.b.2\"",
            "number-of-APDU-retries": 4,
            "object-identifier": "device:2000",
            "object-name": "\".B.A.C.n._.2.0.0.0\"",
            "object-type": 8,
            "protocol-conformance-class": null,
            "protocol-object-types-supported": [
                127,   
            ],
            "protocol-services-supported": [
                -5
            ],
            "segmentation-supported": 0,
            "vendor-identifier": 17,
            "vendor-name": "\".H.o.n.e.y.w.e.l.l. .I.n.t.e.r.n.a.t.i.o.n.a.l. .I.n.c..\""
        }

      As it is obvious the KEYs are not the same in above mentioned objects. The current function examines 
      such a case and debug accordingly. 

  """
  with open("2000.json") as file:
    data=json.load(file)["objects"]
    for key, value in data.items():
      objects_data_list=data[key]
      # For key: "device" different properties get manipulated
      if(key=='device'):
        for object_info in objects_data_list:
          object_info["properties"]["description"]=manipulate_string(object_info["properties"]["description"])
          object_info["properties"]["location"]=manipulate_string(object_info["properties"]["location"])
          object_info["properties"]["model-name"]=manipulate_string(object_info["properties"]["model-name"])
          object_info["properties"]["object-name"]=manipulate_string(object_info["properties"]["object-name"])
          object_info["properties"]["vendor-name"]=manipulate_string(object_info["properties"]["vendor-name"])
      else:
        for object_info in objects_data_list:
          if("out-of-service" in object_info["properties"].keys()):
            del object_info["properties"]["out-of-service"]

          description_str=object_info["properties"]["description"]
          object_name_str=object_info["properties"]["object-name"]
          active_text_str=object_info["properties"]["active-text"]
          inactive_text_str=object_info["properties"]["inactive-text"]          
          if(description_str!=None):
            object_info["properties"]["description"]=manipulate_string(description_str)
          if(object_name_str!=None):
            object_info["properties"]["object-name"]=manipulate_string(object_name_str)
          if(active_text_str!=None):
            object_info["properties"]["active-text"]=manipulate_string(active_text_str)
          if(inactive_text_str!=None):
            object_info["properties"]["inactive-text"]=manipulate_string(inactive_text_str)       
  with open("edited_2000.json", "w") as file:
    json.dump(data, file, indent=4)

def manipulate_string(input_string):
  if(len(list(re.finditer("\.{3}", input_string)))!=0):
    if(len(list(re.finditer("\.{3}", input_string))) > 3):
      return "........"
    else:
      return re.sub(pattern= '(\.{3})', repl="-",string= input_string).replace(".", "")\
                  .replace("-",".").replace("\"", "")
  elif(len(list(re.finditer('(^\"+|\"+$|\.+)', input_string)))!=0):
    if(len(list(re.finditer('^T.h.i.s', input_string)))!=0):
      return input_string
    elif(len(list(re.finditer('This', input_string)))!=0):
      return re.sub(pattern= '(^\"+|\"+$)', repl="",string= input_string) 
    else:
      return re.sub(pattern= '(^\"+|\"+$|\.+)', repl="",string= input_string)
  elif(input_string==""):
    return ""

