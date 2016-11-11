"""
    list twikis:
        List all L1 Trigger Offline Twikis
        
    Usage:
        list twikis [check=1]

    Parameters:
        check: force a check of the twiki URL before printing.
               Useful when adding new entries. Default: 0
        
"""
import logging
import urllib
import hepshell

LOG = logging.getLogger(__name__)

URL_PREFIX = 'https://twiki.cern.ch/twiki/bin/view/'
TWIKIS = {
    'L1T offline DEV': {
        'url': 'https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TOfflineDev',
        'description': 'Instructions for L1 offline software development',
    },
    'L1T Calo Upgrade Offline Analysis': {
        'url': 'https://twiki.cern.ch/twiki/bin/view/CMS/L1CaloUpgradeOfflineAnalysis',
        'description': 'Some CaloL2 analysis workflows are detailed here',
    },
    'L1T phase 2': {
        'url': 'https://twiki.cern.ch/twiki/bin/view/CMS/L1TriggerPhase2',
        'description': 'In preparation ! ',
    },
    'L1T phase 2 interface specs': {
        'url': 'https://twiki.cern.ch/twiki/bin/view/CMS/L1TriggerPhase2InterfaceSpecifications',
        'description': 'Working definitions of Trigger Primitive inputs',
    },
    'CSC trigger emulator timing': {
        'url': 'https://twiki.cern.ch/twiki/bin/view/CMS/CSCDigitizationTiming',
        'description': 'Simulation of signal times for CSC',
    },
    'L1 Trigger Emulator Stage 2 Upgrade Instructions': {
        'url': 'https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TStage2Instructions',
        'description': 'L1 Trigger Emulator Stage 2 Upgrade Instructions',
    },
    'Offline DQM': {
        'url': 'https://twiki.cern.ch/twiki/bin/view/CMS/DQMOffline',
        'description': 'Twiki meant to give you a basic understanding of Offline DQM',
    },
}


def does_url_exist(url):
    exists = False
    try:
        qry = urllib.urlopen(url)
        if qry.getcode() == 200:
            exists = True
    except Exception as e:
        print(e)
    return exists


def get_text_lenghts(twikis):
    names = twikis.keys()
    urls = []
    descriptions = []

    for _, twiki in twikis.items():
        urls.append(twiki['url'])
        descriptions.append(twiki['description'])

    len_names = [len(n) for n in names]
    len_urls = [len(u) for u in urls]
    len_descriptions = [len(d) for d in descriptions]

    return max(len_names), max(len_urls), max(len_descriptions)


class Command(hepshell.Command):

    DEFAULTS = {
        'check': False
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        # parse arguments and parameters
        self.__prepare(args, variables)
        self.__create_table(TWIKIS)

        return True

    def __create_table(self, twikis):
        headers = ['Name', 'URL', 'Description']
        # get maximum lenghts of our columns
        max_len_n, max_len_u, max_len_d = get_text_lenghts(twikis)
        # add some space
        max_len_n = max([max_len_n, len(headers[0])])

        row_format = "{:<" + str(max_len_n) + "}\t"
        row_format += "{:<" + str(max_len_u) + "}\t"
        row_format += "{:<" + str(max_len_d) + "}\n"

        self.__text = row_format.format(*headers)
        self.__text += '-' * (max_len_n + max_len_u + max_len_d)
        self.__text += '\n'

        for name, twiki in sorted(twikis.items()):
            #             url = twiki['url'].replace(URL_PREFIX, '')
            url = twiki['url']
            desc = twiki['description']
            if not self.__variables['check'] or does_url_exist(url):
                self.__text += row_format.format(*[name, url, desc])
            else:
                LOG.warn('Twiki "{0}" does not exist!'.format(url))
        self.__text += '\n'
