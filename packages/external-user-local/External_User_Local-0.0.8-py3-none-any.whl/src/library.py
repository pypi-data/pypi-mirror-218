import os
from LoggerLocalPythonPackage.LoggerServiceSingleton import LoggerServiceSingleton
import sys
import dotenv 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db')))
from library_DB import library_DB

dotenv.load_dotenv()
logger_serv=LoggerServiceSingleton()
Local_Logger=logger_serv.get_instance()
class Accsess_Token_Library:
    
    def insert_user_external(self,user_name,profile_id,access_token):
        Local_Logger.info("START insert access token for "+access_token)
        insert_user_ext=library_DB()
        insert_user_ext.insert_User_Access_Token(user_name,profile_id,access_token)
        Local_Logger.info("END insert access token "+access_token )
        
    def update_user_external(self,profile_id,access_token):
        Local_Logger.info("START update access token")
        insert_user_ext=library_DB()
        insert_user_ext.update_by_profile_id(profile_id,access_token)
        Local_Logger.info("END update access token "+access_token )
    def get_access_token(self,profile_id):
        Local_Logger.info("START get access token")
        insert_user_ext=library_DB()
        return insert_user_ext.select_by_profile_id(profile_id)
    def get_access_token_by_user_name(self,user_name):
        Local_Logger.info("START get access token")
        insert_user_ext=library_DB()
        res=insert_user_ext.get(user_name)
        Local_Logger.info("END get access token")
        return res
        
    def delete_access_token_by_profile_id(self,profile_id):
        Local_Logger.info("START get access token")
        insert_user_ext=library_DB()
        Local_Logger.info("END get access token")
        insert_user_ext.delete_by_profile_id(profile_id)
        Local_Logger.info("END delete access token")
        
    def update_user_external_by_username(self,user_name,access_token):
       Local_Logger.info("START update access token")
       insert_user_ext=library_DB()
       insert_user_ext.update_by_user_name(user_name,access_token)
       Local_Logger.info("END update access token "+access_token ) 