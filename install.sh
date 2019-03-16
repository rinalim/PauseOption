## install.sh
# Install      :
# cd /home/pi
# git clone https://github.com/rinalim/PauseOption
# cd PauseOption
# chmod 755 install.sh
# sudo ./install.sh

#sudo apt-get install fonts-nanum -y
#sudo apt-get install fonts-nanum-extra -y

sudo rm -rf /opt/retropie/configs/all/PauseOption/
mkdir /opt/retropie/configs/all/PauseOption/
cp -f -r ./PauseOption /opt/retropie/configs/all/
mkdir /opt/retropie/configs/all/PauseOption/result/
# cp ./experimental/PauseOption.py /opt/retropie/configs/all/PauseOption/

sudo sed -i '/PauseOption/d' /opt/retropie/configs/all/runcommand-onstart.sh 
echo 'rom_PauseOption=$3' >> /opt/retropie/configs/all/runcommand-onstart.sh 
echo 'rom_PauseOption="${rom_PauseOption##*/}"' >> /opt/retropie/configs/all/runcommand-onstart.sh 
echo 'rom_PauseOption="${rom_PauseOption%.*}"' >> /opt/retropie/configs/all/runcommand-onstart.sh 
echo 'echo "$1 $2 $rom_PauseOption" > /tmp/PauseOption.log' >> /opt/retropie/configs/all/runcommand-onstart.sh
echo '/usr/bin/python /opt/retropie/configs/all/PauseOption/PauseOption.py &' >> /opt/retropie/configs/all/runcommand-onstart.sh

#cd /home/pi/PauseOption/PauseOption/PauseMode
#sudo chmod 755 update.sh
#./update.sh

chgrp -R -v pi /opt/retropie/configs/all/PauseOption/
chown -R -v pi /opt/retropie/configs/all/PauseOption/

python ./PauseOption/setup.py

echo
echo "Setup Completed"
