INFILE_NAME = 'Infile.xml'
OUTFILE_NAME = 'Outfile.kml'

import xml.etree.ElementTree as et
et.register_namespace('', "http://www.opengis.net/kml/2.2")
tree = et.parse(INFILE_NAME)
kmlNamespace = '{http://www.opengis.net/kml/2.2}'
document = tree.find(kmlNamespace + 'Document')


# For each marker in the KML file
for map_pin in document.findall(kmlNamespace + 'Placemark'):
    # Get rid of all styleURL nodes
    for styleURL in map_pin.findall(kmlNamespace + 'styleUrl'):
        print(styleURL)
        map_pin.remove(styleURL)
    # Get well number from extended data and move it into parent 'name' node
    for attributes in map_pin.find(kmlNamespace + 'ExtendedData').findall(kmlNamespace + 'Data'):
        print(attributes.attrib)
        if attributes.attrib['name'] == 'wl_nbr':
            well_number = attributes.find(kmlNamespace + 'value').text
    name = et.SubElement(map_pin, 'name')
    name.text = well_number
    print(et.tostring(name))
# Write output to file
tree.write(
    OUTFILE_NAME,
    xml_declaration = True,
    encoding = 'utf-8',
    method = 'xml'
)

if __name__ == '__main__':
    pass
