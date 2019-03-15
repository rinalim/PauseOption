#!/usr/bin/python

import os, re, time
import xml.etree.ElementTree as ET

CONFIG = '/opt/retropie/configs/'
PATH_PAUSEOPTION = '/opt/retropie/configs/all/PauseOption/'
PATH_PAUSEMODE = '/opt/retropie/configs/all/PauseMode/'

user_key = {}
btn_map = {}
es_conf = 1

capcom_fight = ['mshvsf', 'vsav', 'sfa', 'sfa2', 'sfa3', 'sf2', 'sf2ce', 'ssf2']
capcom_dd = ['ddtod', 'ddsom']


def check_update(romname):
    RESUME = PATH_PAUSEOPTION+'result/' + romname + '_resume.png'
    XML = PATH_PAUSEOPTION+'xml/'+romname+'.xml'
    CORECFG = CONFIG + 'fba/FB Alpha/FB Alpha.rmp'
    GAMECFG = CONFIG + 'fba/FB Alpha/' + romname + '.rmp'
   
    if os.path.isfile(RESUME) == False:
        return True
    else:
        _time = os.path.getmtime(RESUME)
        if _time < os.path.getmtime(PATH_PAUSEOPTION+'layout.cfg'):
            return True
        if os.path.isfile(XML) == True:
            if _time < os.path.getmtime(XML):
                return True
        if os.path.isfile(CORECFG) == True:
            if _time < os.path.getmtime(CORECFG):
                return True
        if os.path.isfile(GAMECFG) == True:
            if _time < os.path.getmtime(GAMECFG):
                return True
        
    #print 'No need to update PNG'
    return False


def load_layout():

    global es_conf

    #' -(1)-----  -(2)-----  -(3)----- '
    #' | X Y L |  | Y X L |  | L Y X | '
    #' | A B R |  | B A R |  | R B A | '
    #' ---------  ---------  --------- '

    f = open(PATH_PAUSEOPTION+"layout.cfg", 'r')
    es_conf = int(f.readline())
    
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
    if os.path.isfile(PATH_PAUSEOPTION+'xml/'+romname+'.xml') == False:
        print 'No xml found'
        name = romname
        lever = '0'
        buttons = ['Button A', 'Button B', 'Button C', 'Button D', 'None', 'None']
    else:
        doc = ET.parse(PATH_PAUSEOPTION+'xml/'+romname+'.xml')
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
                btn = i.get('value')
                btn = btn.replace("Light", "L")
                btn = btn.replace("Jab", "L")
                btn = btn.replace("Short", "L")
                btn = btn.replace("Middle", "M")
                btn = btn.replace("Strong", "M")
                btn = btn.replace("Heavy", "H")
                btn = btn.replace("Fierce", "H")
                btn = btn.replace("Roundhouse", "H")
                btn = btn.replace(" - ", "-")
                btn = btn[:10]
                buttons.append(btn)
                print i.get('name'), btn
        for j in range(len(buttons), 6):
            buttons.append("None")
    
    return name, lever, buttons


def get_btn_layout(system, romname, buttons):
    '''
    f = open('/tmp/js.log', 'r')
    line = f.readline()
    line = f.readline() # goto 2nd line
    dev_name = re.search('Joystick \((.*?)\)', line).group(1)
    # print dev_name
    f.close()
    '''
    # FBA button sequence   
    btn_map['b'] = '"0"'
    btn_map['a'] = '"8"'
    btn_map['y'] = '"1"'
    btn_map['x'] = '"9"'
    btn_map['r'] = '"10"'
    btn_map['l'] = '"11"'

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
    # Convert from the FBA sequence to the normal sequence (0~5)
    convert = {}

    if romname in capcom_fight:
        convert['"0"'] = 3
        convert['"8"'] = 4
        convert['"1"'] = 0
        convert['"9"'] = 1
        convert['"10"'] = 2
        convert['"11"'] = 5
    elif romname in capcom_dd:
        convert['"0"'] = 0
        convert['"8"'] = 1
        convert['"1"'] = 3
        convert['"9"'] = 2
        convert['"10"'] = 4
        convert['"11"'] = 5
    else:
        convert['"0"'] = 0
        convert['"8"'] = 1
        convert['"1"'] = 2
        convert['"9"'] = 3
        convert['"10"'] = 4
        convert['"11"'] = 5 

    # Map the button sequnece and the button description   
    btn_map['a'] = buttons[convert[btn_map['a']]]
    btn_map['b'] = buttons[convert[btn_map['b']]]
    btn_map['x'] = buttons[convert[btn_map['x']]]
    btn_map['y'] = buttons[convert[btn_map['y']]]
    btn_map['l'] = buttons[convert[btn_map['l']]]
    btn_map['r'] = buttons[convert[btn_map['r']]]  
    print btn_map

    
def draw_picture(system, romname, name, lever, buttons):

    RESUME = " " + PATH_PAUSEOPTION+'result/' + romname + '_resume.png'
    STOP = " " + PATH_PAUSEOPTION+'result/' + romname + '_stop.png'

    # Title
    cmd = "convert -background '#E8E8E8' -fill black -font FreeSans -pointsize 20 -size 360x50 -gravity Center caption:'" + name + "' /tmp/text.png"
    os.system(cmd)
    cmd = "composite -geometry 360x50+20+10 /tmp/text.png " + PATH_PAUSEOPTION + "img/bg_resume.png" + RESUME
    os.system(cmd)

    # Layout
    cmd = "composite -geometry 180x130+22+80 " + PATH_PAUSEOPTION + "img/layout" + str(es_conf) + ".png" + RESUME + RESUME
    os.system(cmd)

    # Button box
    cmd = "composite -geometry 180x130+212+80 " + PATH_PAUSEOPTION + "img/buttons.png" + RESUME + RESUME
    os.system(cmd)

    # Buttons
    pos = ["80x17+218+120", "80x17+298+120", "80x17+218+150", "80x17+298+150", "80x17+218+180", "80x17+298+180"]
    digits = [u'\u2460', u'\u2461', u'\u2462', u'\u2463', u'\u2464', u'\u2465']
    i = 0
    for btn in buttons:
        if btn == 'None':
            continue
        btn = digits[i].encode('utf-8') + ' ' + btn
        cmd = "convert -background '#E8E8E8' -fill black -font FreeSans -pointsize 20 label:'" + btn + "' /tmp/text.png"
        os.system(cmd)
        cmd = "composite -geometry " + pos[i] + " /tmp/text.png" + RESUME + RESUME
        os.system(cmd)
        i = i+1

    # Joystick Box
    cmd = "composite -geometry 358x120+23+248 " + PATH_PAUSEOPTION + "img/joystic.png" + RESUME + RESUME
    os.system(cmd)

    # Lever
    if lever[0] != 'J': # Not 'Just Bottons'
        cmd = "composite -geometry 70x70+36+260 " + PATH_PAUSEOPTION + "img/" + lever[0] + "way.png" + RESUME + RESUME
        os.system(cmd)

    if system == "lr-fbalpha":
        get_btn_layout(system, romname, buttons)
    
        # Configured button layout
        pos = ["80x17+124+270", "80x17+207+270", "80x17+290+270", "80x17+124+300", "80x17+207+300", "80x17+290+300"]
        for i in range(1,7):
            btn = btn_map[user_key[str(i)]]
            if btn == 'None':
                btn = u'\u25cf'.encode('utf-8')
            else:
                btn = u'\u25cf'.encode('utf-8') + ' ' + btn
            cmd = "convert -background '#E8E8E8' -fill black -font FreeSans -pointsize 20 label:'" + btn + "' /tmp/text.png"
            os.system(cmd)
            cmd = "composite -geometry " + pos[i-1] + " /tmp/text.png" + RESUME + RESUME
            os.system(cmd)

    # Generate a STOP image
    cmd = "composite " + PATH_PAUSEOPTION + "img/bg_stop.png " + RESUME + STOP
    os.system(cmd)


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
        if len(words) == 3:    # path, romname
            system = words[1]
            romname = words[2]
            if check_update(romname) == True:
                load_layout()
                name, lever, buttons = get_info(romname)
                #print name, lever, buttons
                draw_picture(system, romname, name, lever, buttons)

            RESUME = " " + PATH_PAUSEOPTION+'result/' + romname + '_resume.png'
            STOP = " " + PATH_PAUSEOPTION+'result/' + romname + '_stop.png'
            # Copy images to PauseMode 
            os.system("cp " + RESUME + " " + PATH_PAUSEMODE + "pause_resume.png")
            os.system("cp " + STOP + " " + PATH_PAUSEMODE + "pause_stop.png")



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
