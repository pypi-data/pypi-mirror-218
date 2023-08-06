import os
import sys
import dotenv 
dotenv.load_dotenv()
from getFromApi import getProfile
from LoggerLocalPythonPackage.LoggerServiceSingleton import locallgr
def main():
    locallgr.info("start running import prfoile from linkedin api..")
    access_token=os.getenv("LINKEDIN_API_TOKEN")
    getProfile1=getProfile()
    getProfile1.getProfileData(access_token)
    
if __name__ == "__main__":
    main()
