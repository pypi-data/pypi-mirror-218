import os
from ctypes.wintypes import POINT
import sys
import dotenv 
dotenv.load_dotenv()
import mysql.connector
import requests
from LoggerLocalPythonPackage.LoggerServiceSingleton import locallgr
import config



class insertToDb:
    def __init__(self):
        self.conn = config.db_connection()
        self.cursor = self.conn.cursor()
        


    def __del__(self):
        self.cursor.close()
        self.conn.close()

    # def insertLinkedProfile(self, results):
    #     try:
    #         for result in results:
    #             query_max_id = "SELECT MAX(id) FROM user.user_table"
    #             self.cursor.execute(query_max_id)
    #             res = self.cursor.fetchone()
    #             max_id = res[0] + 1
    #             name = result.get("name")
    #             firstName = result.get("given_name")
    #             lastName = result.get("family_name")
    #             email = result.get("email")
    #             local = result.get("locale")
    #             country = local.get("country")
    #             location = self.getLocationByCountryId(country)
    #             values = (max_id, name, email, firstName, lastName, location)
    #             query = "INSERT INTO user.user_table (id, username, main_email, first_name, last_name, active_location_id) VALUES (%s, %s, %s, %s, %s, %s)"
    #             self.cursor.execute(query, values)
    #             self.conn.commit()
    #             self.cursor.fetchall()  # Fetch and discard any remaining result sets
    #     except mysql.connector.Error as error:
    #         # self.logger.error("Error executing SQL statement: {}".format(error))
    #         print(error.msg)

    def getLocationByCountryId(self, country):
        locallgr.info("get country location id for "+country)
        query = "SELECT l.id FROM location.location_table AS l JOIN location.country_table AS c ON l.country_id = c.id WHERE c.iso = %s"
        self.cursor.execute(query, (country,))
        result = self.cursor.fetchone()
        self.cursor.fetchall()  # Fetch and discard any remaining result sets
        self.cursor.close()
        if result:

            location_id = result[0]
            locallgr.info("return location id for " +country)
            return location_id
        else:
            locallgr.info("insert location_id for " +country)
            query_max_id = "SELECT MAX(id) FROM location.location_table"
            self.cursor.execute(query_max_id)
            result = self.cursor.fetchone()
            max_id = result[0] + 1
            query_country_cor_id = "SELECT id, coordinate FROM location.country_table WHERE iso = %s"
            self.cursor.execute(query_country_cor_id, (country,))
            result = self.cursor.fetchone()
            country_id = result[0]
            country_cor = result[1]
            values = (max_id, country_cor, country_id)
            query = "INSERT INTO location.location_table (id, coordinate, country_id) VALUES (%s, %s, %s)"
            self.cursor.execute(query, values)
            self.conn.commit()
            self.cursor.fetchall()
            return self.getLocationByCountryId(country=country)

    def addOneLinkedProfile(self, result):
        try:
            locallgr.info("insert profile " +result.get("email"))
            cursor = self.conn.cursor()
            query_max_id = "SELECT MAX(id) FROM user.user_table"
            cursor.execute(query_max_id)
            res = cursor.fetchone()
            max_id = res[0] + 1
            name = result.get("name")
            firstName = result.get("given_name")
            lastName = result.get("family_name")
            email = result.get("email")
            local = result.get("locale")
            country = local.get("country")
            location = self.getLocationByCountryId(country)
            isExist=self.getUserid(email)
            if(isExist):
                self.InsertProfile(isExist)
            else:
                locallgr.info("insert user " +result.get("email"))
                values = (max_id, name, email, firstName, lastName, location)
                query = "INSERT INTO user.user_table (id, username, main_email, first_name, last_name, active_location_id) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, values)
                self.conn.commit()
                cursor.close()
                isExist=self.getUserid(email)
                
                self.InsertProfile(isExist)
                locallgr.info("profile inserted "+max_id)
        except mysql.connector.Error as error:
            locallgr.error(error.msg)
            
    def getUserid(self,email):
        locallgr.info("check if user already exits in user table " +email)
        cursor = self.conn.cursor()
        query_get_id = "SELECT id FROM user.user_table where main_email= %s"
        cursor.execute(query_get_id,(email,))
        res = cursor.fetchone()
        if(res):
            locallgr.info("user "+email+ " already exits in data base with id ")
            return res[0]  
        else:
            locallgr.info("user "+email+ " doesnt exits in data base")
            return None
        
    def InsertProfile(self,user_id):
        cursor = self.conn.cursor()
        query_max_id = "SELECT MAX(id) FROM profile.profile_table"
        cursor.execute(query_max_id)
        res = cursor.fetchone()
        max_id = res[0] + 1
        profile_type=self.getType()
        query = "INSERT INTO profile.profile_table (id,number, user_id,profile_type_id) VALUES (%s,%s, %s, %s)"
        cursor = self.conn.cursor()
        values=(max_id,max_id,user_id,profile_type)
        cursor.execute(query, values)
        self.conn.commit()
        cursor.fetchall()
        
        
    def getType(self):
       locallgr.info("getting profile type for LinkedIn profile")
       cursor = self.conn.cursor()
       query = "SELECT id FROM profile.profile_type_ml_table Where title='LinkedIn profile' "
       cursor.execute(query, )
       result = cursor.fetchone()
       cursor.fetchall()  
       cursor.close() 
       if result:
            type_id = result[0]
            locallgr.info("returned  type")
            return type_id
       else:
           cursor = self.conn.cursor()
           query_max_id = "SELECT MAX(id) FROM profile.profile_type_table"
           cursor.execute(query_max_id)
           res = cursor.fetchone()
           cursor.close()
           cursor=self.conn.cursor()
           max_id = res[0] + 1
           query = "INSERT INTO profile.profile_type_table (id) VALUES (%s)"
           cursor.execute(query, (max_id,))
           self.conn.commit()
           cursor.fetchall()
           cursor.close()
           locallgr.info("insert profile type for linkedin profile")
           query = "INSERT INTO profile.profile_type_ml_table (profile_type_id,title) VALUES (%s,'LinkedIn profile')"
           cursor=self.conn.cursor()
           cursor.execute(query, (max_id,))
           self.conn.commit()
           cursor.fetchall()
           locallgr.info("inserted profile type for linkedin profile")
           return self.getType()