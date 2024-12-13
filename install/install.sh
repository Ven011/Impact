# Update the raspberry pi
sudo apt-get update 
sudo apt-get upgrade -y

# Install software packages
sudo apt-get install -y python3-tk
pip3 install pyserial
pip3 install pillow
#pip3 install functools


sudo cp Impact.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable Impact.service

