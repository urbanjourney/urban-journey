from urban_journey.ujml import namespace as dtsml_namespace
import re


def get_qtag(tag):
    return "{{{}}}{}".format(dtsml_namespace, tag)


def parse_qtag(qtag):
    m = re.search(r'(?:{([\w\W]+)})?(\w*)', qtag)
    return m.group(1), m.group(2)


def is_dtsml_tag(qtag):
    return parse_qtag(qtag)[0] == dtsml_namespace


def is_default_namespace(qtag):
    return parse_qtag(qtag)[0] is None
