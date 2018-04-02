#!/bin/sh

#Install Packages
PACKAGES="python3-PyQt5.QtMultimedia python3-serial nano python3-setuptools python-dev python3-dev python3-pyqt5  python3-pyqt4 python3-pyqtgraph python3-smbus python3-numpy libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev libjpeg-dev libfreetype6-dev"
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install $PACKAGES -y

#install GPIO
wget http://dlcdnet.asus.com/pub/ASUS/mb/Linux/Tinker_Board_2GB/GPIO_API_for_Python.zip
unzip GPIO_API_for_Python.zip -d GPIO
cd GPIO/
sudo python3 setup.py install

#install pygame
cd ~
sudo apt-get install mercurial
hg clone https://bitbucket.org/pygame/pygame
cd pygame
python3 setup.py build
sudo python3 setup.py install

FILE=/home/linaro/.config/autostart/tightvnc.desktop
mkdir -p "$(dirname "$FILE")" && touch "$FILE"
text= "[Desktop Entry]\nType=Application\nName=TightVNC\nExec=vncserver :1\nStartupNotify=false"
printf "[Desktop Entry]\nType=Application\nName=TightVNC\nExec=vncserver :1\nStartupNotify=false" > $FILE
