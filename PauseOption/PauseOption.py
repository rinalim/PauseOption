import os, re
import xml.etree.ElementTree as ET

#CONFIG = '/opt/retropie/configs/'
CONFIG = '/home/csle/PauseOptionDev/configs/'

user_key = {}
btn_map = {}
es_conf = 1

def load_layout():

    #print ' -(1)-----  -(2)-----  -(3)----- '
    #print ' | X Y L |  | Y X L |  | L Y X | '
    #print ' | A B R |  | B A R |  | R B A | '
    #print ' ---------  ---------  --------- '

    if es_conf == 1:
        user_key['1'] = 'x'
        user_key['2'] = 'y'
        user_key['3'] = 'l'
        user_key['4'] = 'a'
        user_key['5'] = 'b'
        user_key['6'] = 'r'
    elif es_conf == 2:
        user_key['1'] = 'y'
        user_key['2'] = 'x'
        user_key['3'] = 'l'
        user_key['4'] = 'b'
        user_key['5'] = 'a'
        user_key['6'] = 'r'
    elif es_conf == 3:
        user_key['1'] = 'l'
        user_key['2'] = 'y'
        user_key['3'] = 'x'
        user_key['4'] = 'r'
        user_key['5'] = 'b'
        user_key['6'] = 'a'

            
def get_info(romname):

    #INPUT = './controls.xml'   
    if os.path.isfile('./xml/'+romname+'.xml') == False:
        print 'No Game Found'
        name = romname
        lever = '0'
        buttons = ['Button A', 'Button B', 'Button C', 'Button D']
    else:
        doc = ET.parse('./xml/'+romname+'.xml')
        game = doc.getroot()
    #game = root.find('./game[@romname=\"' + romname + '\"]')
    #if game == None:
    #   print 'No Game Found'
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


def get_btn_layout(emul, romname, buttons):

    f = open('/tmp/js.log', 'r')
    line = f.readline()
    line = f.readline() # goto 2nd line
    dev_name = re.search('Joystick \((.*?)\)', line).group(1)
    # print dev_name
    f.close()

    print 'Load global setting'
    '''
    f = open(CONFIG + 'all/retroarch/autoconfig/' + dev_name + '.cfg', 'r')
    #f = open("/home/csle/PauseOptionDev/configs/fba/FB Alpha/mslug.rmp", 'r')
    while True:
        line = f.readline()
        if not line: 
            break
        if 'btn' not in line:
            continue
        line = line.replace('\n','')
        line = line.replace('input_','')
        line = line.replace('_btn','')
        line = line.replace('=','')
        words = line.split()
        print words
        if len(words[0]) == 1:    # input_a_btn = "0"
            btn_map[words[0]] = words[1]   
    f.close()
    '''
    
    # FBA button sequence = [0, 8, 1, 9, 10, 11]   
    btn_map['a'] = '"0"'
    btn_map['b'] = '"8"'
    btn_map['x'] = '"1"'
    btn_map['y'] = '"9"'
    btn_map['l'] = '"10"'
    btn_map['r'] = '"11"'

    if os.path.isfile(CONFIG + 'fba/FB Alpha/FB Alpha.rmp') == True:
        print 'Override with emulator setting'
        f = open(CONFIG + 'fba/FB Alpha/FB Alpha.rmp', 'r')
        while True:
            line = f.readline()
            if not line: 
                break
            if 'btn' not in line:
                continue
            line = line.replace('\n','')
            line = line.replace('input_','')
            line = line.replace('_btn','')
            line = line.replace('=','')
            words = line.split()
            if 'player1' in words[0]:    # input_player1_btn_a = "1"
                btn_map[words[0][8]] = words[1]  
        f.close()

    if os.path.isfile(CONFIG + 'fba/FB Alpha/' + romname + '.rmp') == True:
        print 'Override with game specific setting'
        f = open(CONFIG + 'fba/FB Alpha/' + romname + '.rmp', 'r')
        while True:
            line = f.readline()
            if not line: 
                break
            if 'btn' not in line:
                continue
            line = line.replace('\n','')
            line = line.replace('input_','')
            line = line.replace('_btn','')
            line = line.replace('=','')
            words = line.split()
            if 'player1' in words[0]:    # input_player1_btn_a = "1"
                btn_map[words[0][8]] = words[1]  
        f.close()

    print btn_map
    # Convert from the FBA sequence to the normal sequence
    convert = {}
    convert['"0"'] = 0
    convert['"8"'] = 1
    convert['"1"'] = 2
    convert['"9"'] = 3
    convert['"10"'] = 4
    convert['"11"'] = 5
    btn_map['a'] = convert[btn_map['a']]
    btn_map['b'] = convert[btn_map['b']]
    btn_map['x'] = convert[btn_map['x']]
    btn_map['y'] = convert[btn_map['y']]
    btn_map['l'] = convert[btn_map['l']]
    btn_map['r'] = convert[btn_map['r']]   
    print btn_map

    # Do capcom patch here
    
def draw_picture(romname, name, lever, buttons):

    RESUME = " ./result/" + romname + "_resume.png"

    if os.path.isfile(RESUME[1:]) == True:
        print 'File aleady exists'
        return

    # Title
    cmd = "convert -background '#E8E8E8' -fill black -font FreeSans -pointsize 22 -size 360x50 -gravity Center caption:'" + name + "' /tmp/text.png"
    os.system(cmd)
    cmd = "composite -geometry 360x50+20+10 /tmp/text.png ./img/bg_resume.png" + RESUME
    os.system(cmd)

    # Layout
    cmd = "composite -geometry 180x130+22+80 ./img/layout1.png" + RESUME + RESUME
    os.system(cmd)

    # Button box
    cmd = "composite -geometry 180x130+212+80 ./img/buttons.png" + RESUME + RESUME
    os.system(cmd)

    # Buttons
    pos = ["80x18+218+120", "80x18+298+120", "80x18+218+150", "80x18+298+150", "80x18+218+180", "80x18+298+180"]
    digits = [u'\u2460', u'\u2461', u'\u2462', u'\u2463', u'\u2464', u'\u2465']
    i = 0
    for btn in buttons:
        btn1 = btn.replace("Light", "L")
        btn1 = btn1.replace("Middle", "M")
        btn1 = btn1.replace("Heavy", "H")
        btn1 = digits[i].encode('utf-8') + ' ' + btn1
        cmd = "convert -background '#E8E8E8' -fill black -font FreeSans -pointsize 20 label:'" + btn1 + "' /tmp/text.png"
        os.system(cmd)
        cmd = "composite -geometry " + pos[i] + " /tmp/text.png" + RESUME + RESUME
        os.system(cmd)
        i = i+1

    # Joystick Box
    cmd = "composite -geometry 360x120+22+248 ./img/joystic.png" + RESUME + RESUME
    os.system(cmd)

    # Lever
    if lever[0] != 'J': # Not 'Just Bottons'
        cmd = "composite -geometry 70x70+36+260 ./img/" + lever[0] + "way.png" + RESUME + RESUME
        os.system(cmd)

    get_btn_layout('fba', romname, buttons)
    
    # Configured button layout
    pos = ["80x18+124+270", "80x18+207+270", "80x18+290+270", "80x18+124+300", "80x18+207+300", "80x18+290+300"]
    i = 0
    for btn in buttons:
        btn2 = btn.replace("Light", "L")
        btn2 = btn2.replace("Middle", "M")
        btn2 = btn2.replace("Heavy", "H")
        btn2 = u'\u25cf'.encode('utf-8') + ' ' + btn2
        cmd = "convert -background '#E8E8E8' -fill black -font FreeSans -pointsize 20 label:'" + btn2 + "' /tmp/text.png"
        os.system(cmd)
        cmd = "composite -geometry " + pos[i] + " /tmp/text.png" + RESUME + RESUME
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
        if len(words) >= 2:
            name, lever, buttons = get_info(words[1])
            #print name, lever, buttons
            draw_picture(words[1], name, lever, buttons)


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
