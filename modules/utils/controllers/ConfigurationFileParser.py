import os
import configparser as cp

class ConfigurationFileData:

    def __init__(self,configFilePath:str,section:str) -> None:
        self.configFilePath =configFilePath
        self.section =section
        configuration =self.get_credentials()
        if not configuration:
            raise "Invalid File path"
        else:
            if self.section not in configuration:
                raise "Invalid properties section"
            else:
                self.config = dict(configuration.items(self.section))

    def get_credentials(self):
        """
        Get the configuration parsed as an array.
        """
        if os.path.exists(self.configFilePath):
            credentials = cp.RawConfigParser()
            credentials.read(self.configFilePath,'utf-8')
            return credentials
        else:
            print("[Error] Credentials file {} is not defined!".format(self.configFilePath))
            return None


    def getconfkey(self,key:str):
        return self.config.get(key)