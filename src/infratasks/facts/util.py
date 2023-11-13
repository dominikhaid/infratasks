from pyinfra.api import FactBase


class RawCommandOutput(FactBase):
    '''
    Returns the raw output of a command.
    '''

    def command(self, command):
        return command

    def process(self, output):
        return '\n'.join(output)  # re-join and return the output lines
