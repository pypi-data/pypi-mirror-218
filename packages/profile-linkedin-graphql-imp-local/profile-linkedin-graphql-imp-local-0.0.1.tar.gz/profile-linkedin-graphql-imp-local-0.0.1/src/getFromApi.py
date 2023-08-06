import os
from dotenv import load_dotenv
load_dotenv()
import requests
from insert import insertToDb
from dotenv import dotenv_values, set_key
from LoggerLocalPythonPackage.LoggerServiceSingleton import locallgr

# LinkedIn API credentials
class getProfile:
    def __init__(self):
        makefile_path = os.path.join(os.path.dirname(__file__), "..", ".env.play1")
        with open(makefile_path) as f:
                self.access_tokens = os.getenv("LINKEDIN_ACCESS_TOKENS").split(";")if os.getenv("LINKEDIN_ACCESS_TOKENS") else []
                self.api_url = os.getenv("LINKEDIN_API_URL")
        
    def getProfiles(self):
        res=[]
        for access_token in self.access_tokens:
            res.append(self.getProfile(access_token))
        return res   
        
    def getProfile(self,access_token):
        locallgr.info("retrive profile data")
        headers =  {"Authorization": f"Bearer {access_token}"}
        api_response = requests.get(self.api_url, headers=headers)
        if api_response.status_code == 200:
            user_data = api_response.json()
            locallgr.info("profile data retrieved")
            return user_data
        else:
            locallgr.error("Error occurred while fetching user data:", api_response.json())
    def addAccessToken(self,access_token):
        # Append the access token to the list
        locallgr.info("adding access token to environment")
        self.access_tokens.append(access_token)
        os.environ["LINKEDIN_ACCESS_TOKENS"] = ";".join(self.access_tokens)
        env_vars = dotenv_values(".env.play1")
        set_key(".env", "ACCESS_TOKENS", os.environ["LINKEDIN_ACCESS_TOKENS"])
        locallgr.info("access token added to environment")
        return access_token
    
    def getProfileData(self, access_token):
        locallgr.info("get profile data for access token: "+access_token)
        self.addAccessToken(access_token)
        result=self.getProfile(access_token)
        insertToDb1=insertToDb()
        insertToDb1.addOneLinkedProfile(result)
        locallgr.info("finished retrive profile data for access token: "+access_token)