import re
import pdb
#Weight, height, age classifier

# Regex to get
# http://www.regexr.com/
# re_restring = "\/*[mfMF]\/*\d+.\/\d\'*\d+\"*"
# ex:
# M/18/6'1
# M/27/5'10"
# M/21/5'4"
# F/34/5'4"


# Regex format handlers: gender,age,height
# Moved out of class definition since it cannot be called within it.
# ex: F/20/5'3"
# ex: M/21/5'10
regex_format = [
    (r"\/*[mfMF]\/*\d+.\/\d\'*\d+\"*", 'format1'),
    (r"[mfMF]\/*\d+.\/\d\'*\d+?\s", 'format1')
]
class RedditAnalyzer:
    """Analyzes the title text of the posts to retrieve information"""
    attrDict = {}
    def __init__(self, title):
        self.title = title
        self.gender = None
        self.height = None
        self.weight = None
        self.age = None

    #
    # M/21/5'7"
    # M/21/6'
    #
    def format1(self, str):
        x = str.split('/')
        #print x
        self.attrDict['title'] = self.title
        self.attrDict['gender'] = x[0]
        self.attrDict['age'] = x[1]
        self.attrDict['height'] = x[2]
        return self.attrDict


    #loops through regex functions to
    def get_attrs(self):
        for regex, fun in regex_format:
            match = re.match(regex, self.title)
            if match:
                return getattr(self, fun)(match.group(0))
            return None







