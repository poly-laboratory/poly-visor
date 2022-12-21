from models.modelSupervisor import Supervisor
import sys
import os
import configparser
from flask import send_file

# Get PARENT path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
# insert into PYTHONPATH
sys.path.insert(1, parent)
# get Supervisor object from modelSupervisor


def get_supervisor():
    a = Supervisor()
    return a

# restart supervisor


def restart_supervisor_model():
    a = Supervisor()
    return a.restart

# shut down supervisor


def shutdown_supervisor_model():
    a = Supervisor()
    return a.shutdown

# clear log


def clear_log_model():
    a = Supervisor()
    return a.clear_log

# reload config supervisor, return array result [[added, changed, removed]]


def reload_config():
    a = Supervisor()
    return a.reload_config_model

# get all log of supervisor since it run


def all_log_supervisord():
    a = Supervisor()
    return a.all_log

# Clear all log of process when it running, return array result status info


def clear_all_log_of_processes():
    a = Supervisor()
    return a.clear_all_log_processes

# update the config file for a running process
def update_config(process_name):
    a = Supervisor()
    return a.update_config_model(process_name)

# reread and update by supervisorctl command
def reread_and_update():
    commandReread = 'supervisorctl reread'
    commandUpdate = 'supervisorctl update'
    os.system(commandReread)
    os.system(commandUpdate)

# Create config file for supervisor and check if file exist
def createConfig(process_name, command):
    if (os.path.isfile('/var/supervisor/conf.d/' + process_name + '.ini')):
        return False
    else:
        config = configparser.ConfigParser()
        config['program:' + process_name] = {
            'command': command,
            'autostart': 'true',
            'autorestart': 'true',
            'stdout_logfile': '/var/log/' + process_name + '.out.log',
            'stdout_logfile_maxbytes': '10MB',
            'stderr_logfile': '/var/log/' + process_name + '.err.log',
            'stderr_logfile_maxbytes': '10MB',
        }
        with open('/var/supervisor/conf.d/' + process_name + '.ini', 'w') as config_file:
            config.write(config_file)
        reread_and_update()
        return True


# create updateConfig function to update the config file based on the key
def modifyConfig(process_name,action, key , value = ''):
    if (os.path.isfile('/var/supervisor/conf.d/' + process_name + '.ini')):
        config = configparser.ConfigParser()
        config.read('/var/supervisor/conf.d/' + process_name + '.ini')
        if action == 'update':
            config['program:' + process_name][key] = value
        elif action == 'delete':
            del config['program:' + process_name][key]
        with open('/var/supervisor/conf.d/' + process_name + '.ini', 'w') as config_file:
            config.write(config_file)
        reread_and_update()    
        return True
    else:
        return False


# render config file
def renderConfig(process_name):
    if (os.path.isfile('/var/supervisor/conf.d/' + process_name + '.ini')):
        # with open('/var/supervisor/conf.d/' + process_name + '.ini', 'r') as f:
        #     # read each line and spilt each line after space
        #     config = f.read().splitlines()
        return send_file('/var/supervisor/conf.d/' + process_name + '.ini',mimetype='text/plain')
    else: 
        return 'File not found'