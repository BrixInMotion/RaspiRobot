# RaspiRobot
Software for a Robot, controlled by a Raspberry Pi and an Infineon XMC. <br/>
Watch it here: https://www.youtube.com/watch?v=HGzMH6Q6lPc <br/>


Download the code to your Raspberry Pi: <br/>
$git clone https://github.com/BrixInMotion/RaspiRobot.git  <br/>
Copy the XMC1100_H-Bridge-ok.zip to your Computer (you don't need it on the Pi) and extract the zip-file. <br/>
Then download the DAVE-Development Plattform for XMC-microcontrollers: <br/> http://www.infineon.com/cms/en/product/channel.html?channel=db3a30433580b37101359f8ee6963814 <br/>
<br/>
After installing it, copy the extracted Project to C:Workspaces and open the Project in DAVE. <br/>
Then connect your XMC 1100 Boot kit via usb and flash it. After you've done this, connect your Hardware like shown in the <br/> schematics in the Video and open a Remote Desktop Protocoll on your computer and connect to your Raspberry Pi. <br/>
There open a terminal and run: <br/>

$sudo python /home/pi/RaspiRobot/DrivebyXMC.py <br/>
