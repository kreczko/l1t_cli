"""
    get latest integration branch: 
        Returns the latest integration branch for {0}
        
    Usage:
        get latest integration branch
"""
import logging
#import pycurl
import json
from StringIO import StringIO
import re

import hepshell

LOG = logging.getLogger(__name__)
URL = 'https://api.github.com/repos/cms-l1t-offline/cmssw/tags?per_page=10000'
REPO = 'https://github.com/cms-l1t-offline/cmssw'


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        doc = doc.format(REPO)
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)

        versions_and_tags = Command.get_versions_and_tags()
        latest_tag = Command.get_latest_tag(versions_and_tags)

        self.__text = 'Latest integration tag for {0}: \n'.format(REPO)
        self.__text += latest_tag

        return True

    @staticmethod
    def get_versions_and_tags():
        tags = Command.__get_tags()
        intagration_tags = filter(lambda x: 'integration' in x, tags)
        # get versions
        versions = map(Command.get_version, intagration_tags)
        versions_and_tags = zip(versions, intagration_tags)

        return versions_and_tags

    @staticmethod
    def __get_tags():
        str_buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, URL)
        c.setopt(c.WRITEDATA, str_buffer)
        c.perform()
        c.close()

        data = json.loads(str_buffer.getvalue())
        tags = [d['name'] for d in data]
        return tags

    @staticmethod
    def get_latest_tag(versions_and_tags):
        versions = [v for v, _ in versions_and_tags]
        latest_version = Command.get_latest_version(versions)
        latest_tag = None
        for v, t in versions_and_tags:
            if v == latest_version:
                latest_tag = t
                break
        return latest_tag

    @staticmethod
    def get_version(branch_name):
        match = re.search('v(\d+\.\d\.?\d?)', branch_name)
        result = match.group()
        result = result.lstrip('v')
        return result

    @staticmethod
    def get_latest_version(versions):
        if versions:
            versions.sort(key=lambda s: map(int, s.split('.')), reverse=True)
            return versions[0]
        return None
