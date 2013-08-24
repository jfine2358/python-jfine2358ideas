'''Tools for helping to test
'''
import lxml.etree

__metaclass__ = object

def pp_elt(elt):

    xml= elt.xml
    s = lxml.etree.tostring(elt.xml, pretty_print=True)
    print(s[:-1])               # Strip trailing '\n'.
