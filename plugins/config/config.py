from DevPlugin import DevopsAppPlugin
import os
import re
import configparser

class Config(DevopsAppPlugin):
    def __init__(self, app):
        super().__init__(app)
        self.name = 'config'
        self.config = {}

    def get_data(self):
        file_name = "~/wp_vars"
        if self.get_config(file_name):
            #self.get_default_data()
            for each_section in self.config_parser.sections():
                self.config[each_section] = {}
                for key in self.config_parser[each_section]:
                    self.config[each_section][key] = self.get_value(each_section,key)
        return self.config


    def get_config(self, config_file="~/wp_vars"):
        """ this is used to get config file information wp_vars """
        self.config_parser = configparser.ConfigParser()
        try:
            self.config_parser.read( os.path.expanduser(config_file) )
        except Exception as e:
            self.log('Error finding config file %s' % config_file, level='error')
            return False
        return True


    def get_value(self, section, name=None, default=None):
        """ gets a value from config file"""
        output = default
        try:
            if name == None:
                output = self.config_parser[section]
            else:
                output = self.config_parser[section][name].strip('"').strip()
        except Exception as e:
            self.log('Error reading config options %s in section %s' %(name, section), level='debug')
        output = self.convert_value(output)
        return output

    def set_value(self, section, name, value=""):
        pass

    def convert_value(self, value):
        try:
            list = re.sub(r'\s', '', value).split(',');
            if len(list) > 1:
                value = list
            else:
                if value == 'True':
                    value = True
                if value == 'False':
                    value = False
        except TypeError:
            pass
        return value
