
import argparse
from argparse import RawTextHelpFormatter
import os

# Argument parser.
class parser(object):


    def __init__(self):
        """
        Defines the command-line arguments. Check the help [-h] to learn more.
        """

        # Set-up the parser object.
        self.parser = argparse.ArgumentParser(description='Boolean query documents using inverted index', formatter_class=RawTextHelpFormatter)

        # Option to load the desired documents from a CSV file.
        self.parser.add_argument('documents', type=str, help='''Constructs an inverted index from a CSV file. Required format: One document per line. First line is discarded.
<id>\\t<url>\\t<pub_date>\\t<title>\\t<document_content>\\n
        ''')

        self.parser.add_argument('-q',metavar='query', type=str, help='Boolean query', action='append')

    def parse_args(self):
        """
        parses the program arguments.
        :return: dictionary with key-value pairs.
        """

        # Parse the arguments themselves.
        args = vars( self.parser.parse_args() )

        return args