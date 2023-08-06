import os
from tapipy.tapis import Tapis
import json
import datetime
import logging

try:
    from ..utilities.logger import ServiceLogger
except:
    class ServiceLogger:
        def __init__(self, name, log_path):
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.INFO)
            file_handler = file_handler = logging.FileHandler(
                log_path, mode='a')
            file_handler.setLevel(logging.INFO)
            file_format = logging.Formatter(
                '%(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
            self.logger.disabled = False

        #def log(self, )


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(f"{__file__}")))
ROOT_USER_FILE_PATH = os.path.join(__location__, r'user_files')
    

class User:
    def __init__(self, parent_path, username):
        self.root_path = f"{parent_path}\\{username}"
        self.user_info_path = f"{self.root_path}\\{username}_info"
        self.cache_path = f"{self.root_path}\\cache"
        self.tenants_path = f"{self.root_path}\\tenants"
        

class Tenant:
    def __init__(self, parent_path, tenant_id):
        self.root_path = f"{parent_path}\\{tenant_id}"
        self.tenant_info_path = f"{self.root_path}\\{tenant_id}_info.json"
        self.services_path = f"{self.root_path}\\services"
    
    def write_tenant_info(self, tenant_info):
        with open(self.tenant_info_path, 'w') as f:
            try:
                json.dump(tenant_info)
                return True
            except:
                return False
            
    

class FileManager:
    user: User = None
    tenant: Tenant = None
    root_path = ROOT_USER_FILE_PATH

    def set_information(self, user, tenant):
        self.user = User(self.root_path, username=user)
        self.tenant = Tenant(self.root_path, tenant_id=tenant)

    

