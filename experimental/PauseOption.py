#-*-coding: utf-8 -*-
#!/usr/bin/python

import os, re, time, sys
from subprocess import *
import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding('utf-8')

CONFIG = '/opt/retropie/configs/'
PATH_PAUSEOPTION = '/opt/retropie/configs/all/PauseOption/'
XML = PATH_PAUSEOPTION+'xml/'
PATH_PAUSEMODE = '/opt/retropie/configs/all/PauseMode/'
FONT = "'NanumBarunGothic'"

user_key = {}
btn_map = {}
es_conf = 1

show_pause = True
show_marquee = True

capcom_fight = ['mshvsf', 'vsav', 'sfa', 'sfa2', 'sfa3', 'sf2', 'sf2ce', 'ssf2']
capcom_dd = ['ddtod', 'ddsom']


def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen("LANG=en_US.UTF-8 " + cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
	

def check_update(romname):
    RESUME = PATH_PAUSEOPTION+'result/' + romname + '_resume.png'
    CORECFG = CONFIG + 'fba/FB Alpha/FB Alpha.rmp'
    GAMECFG = CONFIG + 'fba/FB Alpha/' + romname + '.rmp'
   
    if os.path.isfile(RESUME) == False:
        return True
    else:
        _time = os.path.getmtime(RESUME)
        if _time < os.path.getmtime(PATH_PAUSEOPTION+'layout.cfg'):
            return True
        if os.path.isfile(XML+romname+'.xml') == True:
            if _time < os.path.getmtime(XML+romname+'.xml'):
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
    if os.path.isfile(XML+romname+'.xml') == False:
        print 'No xml found'
        name = romname
        lever = '0'
        buttons = ['A 버튼', 'B 버튼', 'C 버튼', 'D 버튼', 'None', 'None']
    else:
        doc = ET.parse(XML+romname+'.xml')
        game = doc.getroot()
    #game = root.find('./game[@romname=\"' + romname + '\"]')
    #if game == None:
    #   print 'No Game Found'
        name = str(unicode(game.get('gamename')))
        print name
        player = game.find('player')
        controls = player.find('controls')
        lever = controls[0].get('name')
        print lever
        labels = player.findall('labels')
        buttons = []
        for i in labels[0]:
            if 'BUTTON' in i.get('name'):
                btn = str(unicode(i.get('value')))
                # Translate to Korean
                btn = btn.replace("Jab", "약")
                btn = btn.replace("Strong", "중")
                btn = btn.replace("Fierce", "강")
                btn = btn.replace("Short", "약")
                btn = btn.replace("Roundhouse", "강")
                btn = btn.replace("Light", "약")
                btn = btn.replace("Middle", "중")
                btn = btn.replace("Heavy", "강")
                btn = btn.replace("Punch", "펀치")
                btn = btn.replace("Kick", "킥")
                btn = btn.replace("Attack", "공격")
                btn = btn.replace("Jump", "점프")
                btn = btn.replace("Select", "선택")
                btn = btn.replace("Magic", "마법")
                btn = btn.replace("Fire", "총알")
                btn = btn.replace("Loop", "회전")
                btn = btn.replace("Bubble", "방울")
                btn = btn.replace("Left", "왼쪽")
                btn = btn.replace("Center", "가운데")
                btn = btn.replace("Right", "오른쪽")
                btn = btn.replace(" - ", "-")
                #btn = btn[:10]
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
    btn_map['l'] = '"10"'
    btn_map['r'] = '"11"'

    if os.path.isfile(CONFIG + 'fba/FB Alpha/' + romname + '.rmp') == True:
        print 'Use game specific setting'
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
	
    elif os.path.isfile(CONFIG + 'fba/FB Alpha/FB Alpha.rmp') == True:
        print 'Use FBA setting'
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

    if show_pause == True:
        # Title
        name = name.replace("'", "")
        cmd = "convert -background '#E8E8E8' -fill black -font " + FONT + "-Bold -pointsize 20 -size 360x50 -gravity Center caption:'" + name + "' /tmp/text.png"
        run_cmd(cmd)
        cmd = "composite -geometry 360x50+20+10 /tmp/text.png " + PATH_PAUSEOPTION + "img/bg_resume.png" + RESUME
        run_cmd(cmd)

        # Layout
        cmd = "composite -geometry 180x130+22+80 " + PATH_PAUSEOPTION + "img/layout" + str(es_conf) + ".png" + RESUME + RESUME
        run_cmd(cmd)

        # Button box
        cmd = "composite -geometry 180x130+212+80 " + PATH_PAUSEOPTION + "img/buttons.png" + RESUME + RESUME
        run_cmd(cmd)

        # Buttons
        pos = ["80x20+218+120", "80x20+298+120", "80x20+218+150", "80x20+298+150", "80x20+218+180", "80x20+298+180"]
        digits = [u'\u2460', u'\u2461', u'\u2462', u'\u2463', u'\u2464', u'\u2465']
        i = 0
        for btn in buttons:
            if btn == 'None':
                continue
            btn = digits[i].encode('utf-8') + ' ' + btn
            cmd = "convert -background '#E8E8E8' -fill black -font " + FONT + " -pointsize 20 label:'" + btn + "' /tmp/text.png"
            run_cmd(cmd)
            cmd = "composite -geometry " + pos[i] + " /tmp/text.png" + RESUME + RESUME
            run_cmd(cmd)
            i = i+1

        # Joystick Box
        cmd = "composite -geometry 358x120+23+248 " + PATH_PAUSEOPTION + "img/joystic.png" + RESUME + RESUME
        run_cmd(cmd)

    if show_marquee == True:
        # Title for Marquee
        #cmd = "convert -background white -fill black -font " + FONT + "-Bold -pointsize 20 -size 400x225 -gravity North caption:'" + name + "' /tmp/marquee.png"
        cmd = "convert -resize 250x70 -quality 100 '" + "/home/pi/RetroPie/roms/arcade/marquee/" + romname + ".png" + "' /tmp/marquee.png"
        run_cmd(cmd)
        cmd = "composite -gravity North /tmp/marquee.png " + "/home/pi/RemoteMarquee/background.jpg" + " /tmp/marquee.png"
        run_cmd(cmd)
        cmd = "convert /tmp/marquee.png -negate /tmp/marquee.png"
        run_cmd(cmd)

    # Lever
    if lever[0] != 'J': # Not 'Just Bottons'
	if show_pause == True:
            cmd = "composite -geometry 70x70+36+260 " + PATH_PAUSEOPTION + "img/" + lever[0] + "way.png" + RESUME + RESUME
            run_cmd(cmd)
	if show_marquee == True:
	    cmd = "composite -geometry 70x70+20+88 " + PATH_PAUSEOPTION + "img/" + lever[0] + "way.png" + " /tmp/marquee.png" + " /tmp/marquee.png"
            run_cmd(cmd)

    if system == "lr-fbalpha":
        get_btn_layout(system, romname, buttons)
    
        # Configured button layout
        pos = ["80x20+124+270", "80x20+207+270", "80x20+290+270", "80x20+124+300", "80x20+207+300", "80x20+290+300"]
        pos_marquee = ["80x20+124+100", "80x20+207+100", "80x20+290+100", "80x20+124+130", "80x20+207+130", "80x20+290+130"]
        for i in range(1,7):
	    btn = btn_map[user_key[str(i)]]
            if btn == 'None':
                btn = u'\u25cf'.encode('utf-8')
            else:
                btn = u'\u25cf'.encode('utf-8') + ' ' + btn
            if show_pause == True:
                cmd = "convert -background '#E8E8E8' -fill black -font " + FONT + " -pointsize 20 label:'" + btn + "' /tmp/text.png"
                run_cmd(cmd)
                cmd = "composite -geometry " + pos[i-1] + " /tmp/text.png" + RESUME + RESUME
                run_cmd(cmd)
	    # For marquee
	    if show_marquee == True:
                cmd = "convert -background white -fill black -font " + FONT + " -pointsize 20 label:'" + btn + "' /tmp/text.png"
                run_cmd(cmd)
                cmd = "composite -geometry " + pos_marquee[i-1] + " /tmp/text.png" + " /tmp/marquee.png" + " /tmp/marquee.png"
                run_cmd(cmd)
		cmd = "convert /tmp/marquee.png -negate /home/pi/RemoteMarquee/marquee/" + romname + "-ctrl.jpg"
                run_cmd(cmd)

    # Generate a STOP image
    if show_marquee == True:
        cmd = "composite " + PATH_PAUSEOPTION + "img/bg_stop.png " + RESUME + STOP
        run_cmd(cmd)


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
            run_cmd("cp " + RESUME + " " + PATH_PAUSEMODE + "pause_resume.png")
            run_cmd("cp " + STOP + " " + PATH_PAUSEMODE + "pause_stop.png")



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
