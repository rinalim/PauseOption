#!/usr/bin/python

#PATH_PAUSEOPTION = '/opt/retropie/configs/all/VolumeJoy/'
PATH_PAUSEOPTION = '/home/csle/PauseOptionDev/'

print ' -(1)-----  -(2)-----  -(3)----- '
print ' | X Y L |  | Y X L |  | L Y X | '
print ' | A B R |  | B A R |  | R B A | '
print ' ---------  ---------  --------- '

es_conf = input('\nSelect your joystick layout: ')

if es_conf != 1 and es_conf != 2 and es_conf != 3:
    print 'input error!!'
else:
    f = open(PATH_PAUSEOPTION+"layout.cfg", 'w')
    f.write(str(es_conf))
