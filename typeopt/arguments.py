'''
This module constains classes and methods used for intelligent arguments
parsing
'''
import logging
import re
import sys
import yaml

from docopt import docopt

from typeopt.parsing import DictParser

CONFIG_KEY = '--config'


class Arguments:
    '''
    Helper class used to call arguments
    '''

    def __init__(self, doc, **kwargs):
        args = docopt(doc, **kwargs)

        # load config from file
        if CONFIG_KEY in args and args[CONFIG_KEY]:
            with open(args[CONFIG_KEY]) as cfg_file:
                conf_args = yaml.load(cfg_file)
        else:
            conf_args = {}

        args = self.update_args(conf_args, args)

        # parse dictionary
        typed = self.get_typed_arguments(doc)

        parser = DictParser(typed)
        parsed = [parser(k, v) for k, v in args.items()]

        # for ease of use
        self.__dict__.update(parsed)

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def get_typed_arguments(doc):
        '''
        Gets type annotation form docsting
        '''

        # Type annotation should be between <,> brackets
        regex_text = r'\<(.*?)\>'
        pattern = re.compile(regex_text, re.IGNORECASE)

        # Find type annotations in docs
        typed = []
        for line in doc.split("\n"):
            is_typed = re.search(pattern, line)
            if is_typed:
                cast_type = is_typed.group()[1:-1]
                typed.append((line, cast_type))

        return typed

    @staticmethod
    def update_args(conf_args, deafult_args):
        '''
        Returns new dictionary with values read from the config file

        Arguments:
        conf_args       - values read from configuration file
        defaulr_args    - values parsed by docopt
        '''
        logger = logging.getLogger(__name__)
        for k in conf_args:
            if k not in deafult_args:
                logger.error("Configuration file has unknown option %s", k)
                sys.exit(-1)

        deafult_args.update(conf_args)

        return deafult_args
