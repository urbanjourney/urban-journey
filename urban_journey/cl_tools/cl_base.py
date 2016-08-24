class ClBase:
    @staticmethod
    def description():
        raise Exception("This function must be overridden")

    @staticmethod
    def usage():
        raise Exception("This function must be overridden")

    @staticmethod
    def main(args):
        raise Exception("This function must be overridden.")
