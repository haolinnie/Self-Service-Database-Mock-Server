from configparser import ConfigParser


class Config(object):
    def __init__(self, path):
        self.path = path
        self.config = ConfigParser()
        self.config.read(path, encoding='utf-8')
    
    def get(self, *args): # pragma: no cover
        return self.config.get(args[0], args[1])

    def getint(self, *args): # pragma: no cover
        return self.config.getint(args[0], args[1])
    
    # def getfloat(self, *args):
    #     return self.config.getfloat(args[0], args[1])

    # def getboolean(self, *args):
    #     return self.config.getboolean(args[0], args[1])
