import os
from xml.etree import ElementTree as ET

MAIN_FILE = 'psf_test.xml'
TREE = ET.parse(MAIN_FILE)
ROOT_ELEMENT = TREE.getroot()
SPLIT_TAG = 'country'
ID_TAG = 'rank'
DATA_FOLDER = 'data'


def get_children_by_tag(element, tag):
    return [
        child_element
        for child_element in element
        if child_element.tag == tag]


def write_element_to_xml_file(element, filename):
    if len(filename.split('.')) > 2:
        raise Exception('only use one "."')
    if not filename.endswith('.xml'):
        raise Exception('filename must end with ".xml"')
    text = ET.tostring(element)
    with open(filename, 'w+') as xml_file:
        xml_file.write(text)


def filename_for_element_by_id(element, id_tag):
    identifiers = get_children_by_tag(element, id_tag)
    number_of_identifiers = len(identifiers)

    if number_of_identifiers is not 1:
        print 'Entry with malformed identifier: '
        ET.dump(element)

        if number_of_identifiers is 0:
            print 'entry has no identifier'
        elif number_of_identifiers > 1:
            print 'entry has too many identifiers'

        # attribute error is probably the wrong thing
        raise AttributeError('cannot parse element identifiers into file')

    file_prefix = identifiers[0].text

    return '{}.xml'.format(file_prefix)


if __name__ == '__main__':
    children_with_split_tag = get_children_by_tag(ROOT_ELEMENT, SPLIT_TAG)

    if DATA_FOLDER is not None and not os.path.exists(DATA_FOLDER):
        raise Exception('create folder "{}" before trying to write to it'.format(DATA_FOLDER))

    for element in children_with_split_tag:
        filename = filename_for_element_by_id(element, ID_TAG)

        if DATA_FOLDER is not None:
            filename = '{}/{}'.format(DATA_FOLDER, filename)

        if os.path.exists(filename):
            raise Exception('file with name {} already exists!'.format(filename))

        print 'writing file: "{}"...'.format(filename)

        write_element_to_xml_file(element, filename)