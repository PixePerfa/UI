#Update the Distro installation and remove previous install of xrdp
sudo apt-get update && sudo apt-get -y upgrade

#Install a desktop environment and a rdp server 
sudo apt-get purge xrdp
sudo apt install -y xrdp xfce4 xfce4-goodies

#Configure the xrdp server
sudo sed -i 's/3389/3390/g' /etc/xrdp/xrdp.ini
sudo sed -i 's/max_bpp=32/#max_bpp=32\nmax_bpp=128/g' /etc/xrdp/xrdp.ini
sudo sed -i 's/xserverbpp=24/#xserverbpp=24\nxserverbpp=128/g' /etc/xrdp/xrdp.ini
sudo sed -i 's/crypt_level=high/crypt_level=none/g' /etc/xrdp/xrdp.ini
echo xfce4-session > ~/.xsession

sudo sed -i 's/test -x/#test -x/g' /etc/xrdp/startwm.sh
sudo sed -i 's@exec /bin/sh@#exec /bin/sh@g' /etc/xrdp/startwm.sh
echo '#xfce4' >> /etc/xrdp/startwm.sh
echo 'startxfce4' >> /etc/xrdp/startwm.sh
sed -i 's@.*if test -r /etc/profile.*@unset DBUS_SESSION_BUS_ADDRESS\n&@' /etc/xrdp/startwm.sh
sed -i 's@.*if test -r /etc/profile.*@unset XDG_RUNTIME_DIR\n&@' /etc/xrdp/startwm.sh

#Enable services on boot
sudo systemctl enable xrdp
sudo systemctl enable dbus

#Fix Authentication Is Required to Create a Color Managed Device
echo "[Allow Colord all Users]" >> /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla
echo "Identity=unix-user:*" >> /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla
echo "Action=org.freedesktop.color-manager.create-device;org.freedesktop.color-manager.create-profile;org.freedesktop.color-manager.delete-device;org.freedesktop.color-manager.delete-profile;org.freedesktop.color-manager.modify-device;org.freedesktop.color-manager.modify-profile" >> /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla
echo "ResultAny=no" >> /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla
echo "ResultInactive=no" >> /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla
echo "ResultActive=yes" >> /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla

#Fix Failed to execute default web browser
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y

#Troubleshooting for Debian
if cat /etc/*release | grep ^NAME | grep Debian ; then
echo '[boot]' >> /etc/wsl.conf
echo 'systemd=true' >> /etc/wsl.conf
sudo apt install dbus-x11 -y
sudo apt install net-tools -y
fi

#Troubleshooting for Kali Linux
if cat /etc/*release | grep ^NAME | grep Kali ; then
echo '[boot]' >> /etc/wsl.conf
echo 'systemd=true' >> /etc/wsl.conf
sudo apt install dbus-x11 -y
sudo apt install net-tools -y
fi

#Start services
sudo systemctl start xrdp
sudo systemctl start dbus
sudo systemctl status xrdp
