
## install.sh
# Install      :
# cd /home/pi
# git clone https://github.com/rinalim/PauseOption
# cd PauseOption
# chmod 755 install.sh
# sudo ./install.sh

sudo cp ./libraspidmx.so.1 /usr/lib

rm -rf /opt/retropie/configs/all/PauseOption/
mkdir /opt/retropie/configs/all/PauseOption/
cp -f -r ./PauseOption /opt/retropie/configs/all/

sudo sed -i '/PauseOption.py/d' /opt/retropie/configs/all/autostart.sh
sudo sed -i '1i\\/usr/bin/python /opt/retropie/configs/all/PauseOption/PauseOption.py &' /opt/retropie/configs/all/autostart.sh

echo
echo "Setup Completed. Reboot after 3 Seconds."
sleep 3
reboot
