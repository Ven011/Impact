# Update the raspberry pi
sudo apt-get update 
sudo apt-get upgrade -y

# Install software packages
sudo apt-get install -y python3-tk
pip3 install pyserial
pip3 install pillow
sudo apt-get install python3-pil.imagetk
#pip3 install functools


sudo cp Impact.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable Impact.service

# setup silent boot
sudo systemctl mask plymouth-start.service

sudo rm /boot/cmdline.txt
sudo cp cmdline.txt /boot

sudo rm /boot/config.txt
sudo cp config.txt /boot

sudo rm /etc/xdg/lxsession/LXDE-pi/autostart
sudo cp autostart /etc/xdg/lxsession/LXDE-pi/

# reboot pi
sudo reboot
