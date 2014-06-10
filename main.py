__author__ = 'kurtisjungersen'

from re import sub
from os import listdir, mkdir
from shutil import rmtree

class convert_camel_case():

    '''A very simple tool to convert CamelCase to_underscore.
    The class can handle a file (or any number of files) and
    can also simply take a users input and convert it.

    The directories that the tool reads from/ writes to can
    be customized in __init__.

    For usage elsewhere, the 'convert' method is what actually
     does the CamelCase conversion.'''

    #TODO (kmjungersen): More detailed documentation

    def __init__(self):

        self.converted_dir = 'converted/'
        self.convert_dir = 'to_be_converted/'

        self.file_list = []

        for file in listdir(self.convert_dir):

            if file != '.gitignore':

                self.file_list.append(file)

        if len(self.file_list) > 0:

            self.file_convert()

        else:

            self.manual_phrase = ''
            self.manual_convert()


    def convert(self, var_name):
        '''This method of converting CamelCase to_underscore
        is borrowed from the StackOverflow post at:
        http://stackoverflow.com/questions/1175208/
        elegant-python-function-to-convert-camelcase-to-camel-case

        The only borrowed things are the regex substitutions
        described in this post.
        '''

        s1 = sub('(.)([A-Z][a-z]+)', r'\1_\2', var_name)
        s2 = sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        return s2

    def manual_convert(self):

        finished = False

        while finished == False:

            print '=================================='
            print 'Please enter phrase you would like to convert from'
            print 'CamelCase to_underscores! \n'

            self.manual_phrase = raw_input()

            output = self.convert(self.manual_phrase)

            print 'Your converted phrase:\n'
            print '=================================='
            print output
            print '==================================\n'
            print 'Go again (y/n)?'

            response = raw_input()

            if response != 'y' and response != 'Y':
                finished = True

    def file_convert(self):

        for item in self.file_list:

            with open(self.convert_dir + item, 'r+') as infile, \
                 open(self.converted_dir + item, 'w+') as outfile:

                f = infile.read()

                f = self.convert(f)

                outfile.write(f)

        rmtree(self.convert_dir)
        mkdir(self.convert_dir)

        with open(self.converted_dir + '.gitignore', 'r') as infile, \
             open(self.convert_dir + '.gitignore', 'w+') as outfile:

            f = infile.read()
            outfile.write(f)

        print '==================================\n'
        print str(len(self.file_list)) + ' file(s) was/were converted succesfully.\n'
        print 'Be sure to check for any strange underscore behavior'
        print 'before using your converted files.\n'


if __name__ == '__main__':
    convert_camel_case()
