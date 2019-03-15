rm -rf /opt/retropie/configs/all/PauseOption/

sudo sed -i '/PauseOption/d' /opt/retropie/configs/all/runcommand-onstart.sh 

cp /home/pi/PauseMode/PauseMode/*png /opt/retropie/configs/all/PauseMode/

echo
echo "Uninstall Completed"
