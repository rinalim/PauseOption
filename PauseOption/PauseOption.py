import xml.etree.ElementTree as ET

INPUT = './controls.xml'

doc = ET.parse(INPUT)
root = doc.getroot()

GAME = 'ddsom'

game = root.find('./game[@romname=\"' + GAME + '\"]')
if game == None:
    print 'No Game Found'
else:
    print game.get('gamename')
    player = game.find('player')
    controls = player.find('controls')
    print controls[0].get('name')
    labels = player.findall('labels')
    for i in labels[0]:
        print i.get('name'), i.get('value')
