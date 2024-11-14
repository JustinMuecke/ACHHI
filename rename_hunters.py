import os
from user import Hunter
import pickle

registered_hunter = {}
for file in os.listdir("Hunters"):
    filename = os.fsdecode(file)
    if(filename.endswith(".hunt")):
        with open("Hunters/" + filename, "rb") as f:
            hunter : Hunter = pickle.load(f)
            with open("Hunters_new/" + filename.lower(), "wb") as file:
                pickle.dump(hunter, file)
