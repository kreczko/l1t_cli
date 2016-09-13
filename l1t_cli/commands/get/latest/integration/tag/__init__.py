"""
    get latest integration branch: 
        Returns the latest integration branch for {0}
        
    Usage:
        get latest integration branch
"""
import logging
import pycurl
import json
from StringIO import StringIO
import re

from l1t_cli.commands.get import Command as C

LOG = logging.getLogger(__name__)
URL = 'https://api.github.com/repos/cms-l1t-offline/cmssw/tags?per_page=10000'
REPO = 'https://github.com/cms-l1t-offline/cmssw'


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        doc = doc.format(REPO)
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        str_buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, URL)
        c.setopt(c.WRITEDATA, str_buffer)
        c.perform()
        c.close()

        data = json.loads(str_buffer.getvalue())
        tags = [d['name'] for d in data]

        self.__run(tags)

        return True

    def __run(self, tags):
        intagration_tags = filter(lambda x: 'integration' in x, tags)
        # get versions
        versions = map(self.get_version, intagration_tags)
        versions_and_tags = zip(versions, intagration_tags)
        latest_tag = self.__get_latest_tag(versions_and_tags)

        self.__text = 'Latest integration tag for {0}: \n'.format(REPO)
        self.__text += latest_tag

    def __get_latest_tag(self, versions_and_tags):
        versions = [v for v, _ in versions_and_tags]
        latest_version = self.get_latest_version(versions)
        latest_tag = None
        for v, t in versions_and_tags:
            if v == latest_version:
                latest_tag = t
                break
        return latest_tag

    def get_version(self, branch_name):
        match = re.search('v(\d+\.\d\.?\d?)', branch_name)
        result = match.group()
        result = result.lstrip('v')
        return result

    def get_latest_version(self, versions):
        if versions:
            versions.sort(key=lambda s: map(int, s.split('.')), reverse=True)
            return versions[0]
        return None

