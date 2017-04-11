# Setup of the Mindstorms for ev3dev

For each mindstorms brick we have
* 32 GB MicroSD card
* ugreen usb2.0 Ethernet adapter
* Edimax Wifi Nano USB Adapter N 150

## Download Image and flash card

1. Go to the ev3dev homepage and download the latest image
http://www.ev3dev.org/downloads/

2. Use etcher https://etcher.io/ to burn the image onto the MicroSD card

## Setup
Setup is most easily done via the usb ethernet connection.
Connect the brick to a network and boot. 

If you have mDNS enabled, you should be able to login to it via
```
ssh robot@ev3dev.local
```
The standard password is `maker`.


### Hostname
Change the hostname to `pepbot<N>`, where `<N>` is a running number for the bots.

To do this, open `/etc/hostname` and edit it to contain the desired hostname, e.g. using

```
sudo echo pepbot<N> | sudo tee /etc/hostname
```

We should also append a line to the `/etc/hosts` file for the hostname:
```
sudo echo '127.0.0.1 pepbot<N>' | sudo tee -a /etc/hostname
```
Be sure to use `tee -a` here, otherwise we will overwrite the file instead of append.

### Install packages

Install some usefull packages.
```
sudo apt update
sudo apt upgrade
sudo apt install python3-msgpack python3-zmq python3-numpy ipython3 python3-pip
```

### Add pep user, remove standard user

```
sudo useradd -G users,sudo,tty,dialout,cdrom,floppy,audio,video,plugdev,input,bluetooth,i2c,ev3dev -m  pep
sudo passwd pep
```

Log out and log back in as the `pep` user, then run
```
sudo deluser --remove-home robot
```
