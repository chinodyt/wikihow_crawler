import os
import json

class Settings() :
    def __init__(self, path = './') :
        self.path = path
        self.loadSettings()

    def loadSettings(self):
        SETTINGS_JSON = os.path.join(self.path, 'settings.json')
        print(SETTINGS_JSON)
        jsonFile = open(SETTINGS_JSON, 'r')
        self.settings = json.load(jsonFile)
        jsonFile.close()

        LOCAL_SETTINGS = os.path.join(self.path, 'local_settings.json')
        if os.path.isfile(LOCAL_SETTINGS) :
            jsonFile = open(LOCAL_SETTINGS, 'r')
            localSettings = json.load(jsonFile)
            jsonFile.close()
            self.settings = dict(self.mergedicts(self.settings, localSettings))

    def mergedicts(self, dict1, dict2):
        '''
        Copied from here:
        http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge
        '''
        for k in set(dict1.keys()).union(dict2.keys()):
            if k in dict1 and k in dict2:
                if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                    yield (k, dict(self.mergedicts(dict1[k], dict2[k])))
                else:
                    # If one of the values is not a dict, you can't continue merging it.
                    # Value from second dict **overrides** one in first and we move on.
                    yield (k, dict2[k])
                    # Alternatively, replace this with exception raiser to alert you of value conflicts
            elif k in dict1:
                yield (k, dict1[k])
            else:
                yield (k, dict2[k])