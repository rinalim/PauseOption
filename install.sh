## install.sh
# Install      :
# cd /home/pi
# git clone https://github.com/rinalim/PauseOption
# cd PauseOption
# chmod 755 install.sh
# sudo ./install.sh

rm -rf /opt/retropie/configs/all/PauseOption/
mkdir /opt/retropie/configs/all/PauseOption/
cp -f -r ./PauseOption /opt/retropie/configs/all/
mkdir /opt/retropie/configs/all/PauseOption/result/

sudo sed -i '/rom_name/d' /opt/retropie/configs/all/runcommand-onstart.sh 
sudo sed -i '/PauseOption/d' /opt/retropie/configs/all/runcommand-onstart.sh 
echo 'rom_name=$3' >> /opt/retropie/configs/all/runcommand-onstart.sh 
echo 'rom_name="${rom_name##*/}"' >> /opt/retropie/configs/all/runcommand-onstart.sh 
echo 'rom_name="${rom_name%.*}"' >> /opt/retropie/configs/all/runcommand-onstart.sh 
echo 'echo "$1 $2 $rom_name" > /tmp/PauseOption.log' >> /opt/retropie/configs/all/runcommand-onstart.sh
echo '/usr/bin/python /opt/retropie/configs/all/PauseOption/PauseOption.py &' >> /opt/retropie/configs/all/runcommand-onstart.sh

#cd /home/pi/PauseOption/PauseOption/PauseMode
#sudo chmod 755 update.sh
#./update.sh

mkdir backup
cp /opt/retropie/configs/all/PauseMode/*png ./backup

chgrp -R -v pi /opt/retropie/configs/all/PauseOption/
chown -R -v pi /opt/retropie/configs/all/PauseOption/

python ./PauseOption/setup.py

echo
echo "Setup Completed"
