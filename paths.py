import os
from dotenv import load_dotenv
load_dotenv()

paths = {
    2016: os.getenv("DATA_PATH_2016"),
    2014: os.getenv("DATA_PATH_2014"),
    2012: os.getenv("DATA_PATH_2012"),
    2010: os.getenv("DATA_PATH_2010"),
    2008: os.getenv("DATA_PATH_2008")
}