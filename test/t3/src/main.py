from os.path import dirname, join
from urban_journey import from_file


def main(args):
    """Entry point """
    ujml_path = join(dirname(__file__), "main.ujml")
    ujml = from_file(ujml_path)
