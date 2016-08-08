# RaspiRobot
Software for a Robot, controlled by a Raspberry Pi and an Infineon XMC
Watch it here: https://www.youtube.com/watch?v=HGzMH6Q6lPc


Download the code to your Raspberry Pi and copy the XMC1100_H-Bridge-ok.zip to your Computer
(you don't need it on the Pi) and extract the zip-file.
Then download the DAVE-Development Plattform for XMC-microcontrollers: http://www.infineon.com/cms/en/product/channel.html?channel=db3a30433580b37101359f8ee6963814
After installing it, copy the extracted Project to C:Workspaces and open the Project in DAVE.
Then connect your XMC 1100 Boot kit via usb and flash it. After you've done this, connect your Hardware like shown in the schematics in the Video and open a Remote Desktop Protocoll on your computer and connect to your Raspberry Pi.
There open a terminal and run:
$sudo Python /home/pi/RaspiRobot/DrivebyXMC-kbhit.py
