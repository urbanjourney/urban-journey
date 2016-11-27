

class ClBase:
    """
    Base class for command line commands.
    """

    @staticmethod
    def description():
        """
        :return: A short one line description of the command.
        :rtype: string
        """
        raise Exception("This function must be overridden")

    @staticmethod
    def usage():
        """
        :return: A short usage description of the command.
        :rtype: string
        """
        raise Exception("This function must be overridden")

    @staticmethod
    def main(args):
        """
        Main entry point of the command.
        :param args: List of command line arguments passed to the command.
        """
        raise Exception("This function must be overridden.")


