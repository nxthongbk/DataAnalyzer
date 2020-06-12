# DataAnalyzer
Update

sudo nano .config/lxsession/LXDE-pi/autostart    

```@lxpanel --profile LXDE-pi   
@pcmanfm --desktop --profile LXDE-pi   
@lxterminal -e python3 /home/pi/Desktop/DataAnalyzer/lab_monitor.py   
@xscreensaver -no-splash   
@point-rpi
