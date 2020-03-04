Bluetooth button for controlling Signal K
=========================================

This repository is an example on how to control a [Signal K](https://signalk.org/) boat computer system using a cheap Bluetooth "camera shutter" button. Use case is starting the [anchor alarm](https://github.com/sbender9/signalk-anchoralarm-plugin) more conveniently:

* Single button click to set anchor and start watch
* Double click to stop anchor watch

![Camera button](https://live.staticflickr.com/65535/49608449938_e42a5b51e4.jpg)

## Hardware

* Raspberry Pi 3B+ running Signal K on Raspbian
* Bluetooth camera button ([I'm using this model](https://www.amazon.de/dp/B07C7YJS9M/ref=cm_sw_em_r_mt_dp_U_c74xEbBD2JAYD))

## Pairing the button

Set the camera button _On_.

SSH to your Raspberry Pi and discover the device:

```
$ hcitool scan
Scanning ...
XX:XX:XX:XX:XX:XX Camkix Shutter
```

Note down the Bluetooth ID shown for the button (the name and model may be different depending what button you bought).

Then pair and trust the button as a "Bluetooth keyboard":

```
$ sudo bluetoothctl
[bluetooth]# pair XX:XX:XX:XX:XX:XX
[bluetooth]# connect XX:XX:XX:XX:XX:XX
[Camkix Shutter]# trust XX:XX:XX:XX:XX:XX
```

Now you can run `udevadm` to see the device connection and disconnection events when turning it on and off:

```
$ udevadm monitor --environment
KERNEL[7000.708383] add      /devices/platform/soc/xxxxxxxx.serial/tty/ttyAMA0/hci0/hci0:11 (bluetooth)
ACTION=add
DEVPATH=/devices/platform/soc/xxxxxxxx.serial/tty/ttyAMA0/hci0/hci0:11
SUBSYSTEM=bluetooth
DEVTYPE=link
SEQNUM=1358

...
```

## Software setup

Please note that this repository _will not_ work for your hardware out of the box. You will need to adapt at least the udev and systemd files to match your hardware identifiers.
Clone this repository to `/home/pi/kbd` and adapt the files to your liking.

Install the dependencies with:

```
$ pip3 install -r requirements.pip
```

Copy the systemd service file in place and reload:

```
$ sudo cp systemd/signalk-bluetooth-button.service /etc/systemd/system
$ sudo systemctl daemon-reload
```

Copy the udev rules in place and reload udev:

```
$ sudo cp udev/99-camerabutton.rules /etc/udev/rules.d/
$ sudo service udev restart
$ sudo udevadm trigger
```

Now you should see the Python script starting and running whenever the Bluetooth button is turned on:

```
$ journalctl -u signalk-bluetooth-button -f
Mar 04 11:30:42 curiosity-pi systemd[1]: Starting Listen to Bluetooth camera button events...
Mar 04 11:30:43 curiosity-pi listener.py[827]: Running!
Mar 04 11:30:46 curiosity-pi listener.py[827]: Click
Mar 04 11:30:47 curiosity-pi listener.py[827]: Double click
Mar 04 11:31:08 curiosity-pi listener.py[827]: Disconnected
Mar 04 11:31:09 curiosity-pi systemd[1]: signalk-bluetooth-button.service: Succeeded.
```
