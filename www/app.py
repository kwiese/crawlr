"""
Authors: Sean Donohoe and Kyle Wiese

A class for generating the main index.html page
"""

from www.bounds import time_constraints
from www.html_text import *
import math
import os

class MyApp():
    def __init__(self):
        self.generateIndex()

    def generateIndex(self):
        fpath = os.getcwd() + '/www/static/index.html'
        f = open(fpath, 'w')
        keywordOptions = []
        keywords = [k for k in time_constraints]
        keywords.sort()
        for keyword in time_constraints:
            if keyword != "HOME":
                optionsTags = self.generateHourOptions(keyword)
                keyword = keyword.rstrip()
                kTag = keywordTag.format(
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                    optionsTags,
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                ).replace('\n', '').replace('\r', '')
                keywordOptions.append(kTag)
        indexString = indexBegin
        for ktag in keywordOptions:
            indexString += ktag
        indexString += indexEnd
        f.write(indexString)
        f.close()
    
    def generateHourOptions(self, keyword):
        lowerSeconds = time_constraints[keyword]
        hours = math.ceil(lowerSeconds / float(3600))
        options = []
        for x in range(hours, 13):
            hoursToSeconds = x * 3600
            if x == hours:
                optionTag = keywordHourOptionTagSelected.format(hoursToSeconds, x)
            else:
                optionTag = keywordHourOptionTag.format(hoursToSeconds, x)
            options.append(optionTag)

        return options
