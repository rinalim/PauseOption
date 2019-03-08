import os
import xml.etree.ElementTree as ET

INPUT = './controls.xml'
doc = ET.parse(INPUT)
root = doc.getroot()

def get_info(romname):

    game = root.find('./game[@romname=\"' + romname + '\"]')
    if game == None:
       print 'No Game Found'
    else:
       name = game.get('gamename') 
       print name
       player = game.find('player')
       controls = player.find('controls')
       lever = controls[0].get('name')
       print lever
       labels = player.findall('labels')
       buttons = []
       for i in labels[0]:
           if 'BUTTON' in i.get('name'):
               buttons.append(i.get('value'))
               print i.get('name'), i.get('value')
    
    return name, lever, buttons


def draw_picture(name, lever, buttons):
    
    #cmd = "composite -geometry 100x100+50+100 ./" + lever[0] + "way.png ./bg_resume.png ./pause.png"

    cmd = "convert -background '#E8E8E8' -fill black -font FreeSans -pointsize 20 -size 360x50 -gravity Center caption:'" + name + "' ./text.png"
    os.system(cmd)
    cmd = "composite -geometry 360x50+20+10 ./text.png ./pause.png ./pause.png"
    os.system(cmd)

    cmd = "composite -geometry 160x120+30+80 ./layout1.png ./bg_resume.png ./pause.png"
    os.system(cmd)

    #cmd = "composite -geometry 160x120+120+80 ./buttons.png ./bg_resume.png ./pause.png"
    #os.system(cmd)

    pos = ["400x30+240+100", "400x30+240+140", "400x30+240+180", "400x30+240+220", "400x30+240+260", "400x30+240+300"]
    i = 0
    for btn in buttons:
        cmd = "convert -background '#E8E8E8' -fill black -font FreeSans -pointsize 50 label:'" + btn + "' ./text.png"
        os.system(cmd)
        cmd = "composite -geometry " + pos[i] + " ./text.png ./pause.png ./pause.png"
        os.system(cmd)
        i = i+1

def main():

    try:
        f = open('/tmp/PauseOption.log', 'r')
        # except FileNotFoundError:
    except IOError:
        print "IOError"
    else:
        line = f.readline()
        words = line.split()
        f.close()
        if words[0] != "maintitle":
            name, lever, buttons = get_info(words[1])
            #print name, lever, buttons
        
        draw_picture(name, lever, buttons)


if __name__ == "__main__":
    import sys

    try:
        main()

    # Catch all other non-exit errors
    except Exception as e:
        sys.stderr.write("Unexpected exception: %s" % e)
        sys.exit(1)

    # Catch the remaining exit errors
    except:
        sys.exit(0)
