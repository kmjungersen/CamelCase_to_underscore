__author__ = 'kurtisjungersen'

from re import sub
from os import listdir, mkdir
from shutil import rmtree


class ConvertCamelCase():

    """A very simple tool to convert CamelCase to_underscore.
    The class can handle a file (or any number of files) and
    can also simply take a users input and convert it.

    The directories that the tool reads from/ writes to can
    be customized in __init__.

    For usage elsewhere, the 'convert' method is what actually
     does the CamelCase conversion."""

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

    def convert(self, file_to_convert):
        """This method of converting CamelCase to_underscore
        is borrowed from the StackOverflow post at:
        http://stackoverflow.com/questions/1175208/
        elegant-python-function-to-convert-CamelCase-to-camel-case

        The only borrowed things are the regex substitutions
        described in this post.
        """

        s1 = sub('(.)([A-Z][a-z]+)', r'\1_\2', file_to_convert)
        s2 = sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        return s2

    def manual_convert(self):
        """This method will only be called if nothing exists in
        the 'to_be_converted' directory.  It prompts the user
        for a phrase that it can convert from CamelCase_to_underscore.
        """

        finished = False

        while not finished:

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
        """This method gets called when the are files in the
        'to_be_converted' directory.  It will open each file in
        the list, read it and convert it, then write it to a file
        of the same name in the 'converted' directory.

        After doing so, it deletes and recreates the 'to_be_converted'
        directory and then recreates the '.gitignore' file in said
        directory.

        Finally, a summary is displayed in the console.
        """

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
        print str(len(self.file_list)) + ' file(s) was/were converted successfully.\n'
        print 'Be sure to check for any strange underscore behavior'
        print 'before using your converted files.\n'


if __name__ == '__main__':
    ConvertCamelCase()