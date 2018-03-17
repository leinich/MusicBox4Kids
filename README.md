# MusicBox4Kids
## Description
TODO

## Hardware
For this project following hardware was used:
- 1x Raspberry Pi A
- 1x USB Wifi Stick
- 1x Hama PC Sonic Mobil 183 [Amazon.de](https://www.amazon.de/dp/B018VONYPY)
- 16x Jumper Wires 
- 1x IKEA Box (DRAGAN bamboo)
- 5x Push buttons
- 1x MIFARE RC522 RFID

## Hardware Wiring
TODO

## Software Installation
1. You need to setup the rasperry pi (in my case I used an old Raspberry Pi 1 A)
2. Enable SPI via `sudo raspi-config` -> Interfacing Options -> enable SPI
3. Login via SSH and install the needed `sudo apt-get install python-dev git mpd`
4. Clone this repository `cd ~ & git clone https://github.com/leinich/MusicBox4Kids.git`
5. Clone the MIFARE RC522 and copy MFRC522.py to MusicBox4Kids `cd ~ & git clone https://github.com/mxgxw/MFRC522-python.git & cp ./MFRC522-python/MFRC522.py ./MusicBox4Kids/MFRC522.py`
6. Test if the MIFARE RC522 is connected successfully by calling following You should see some information about the NFC chip once you place the chip to the reader `python ./MFRC522-python/Read.py`
7. Start the musicbox to check if the push buttons are attached correctly by pressing the buttons `python ./MusicBox4Kids/MusicBox4Kids.py`
   The results should be shown in the command line.

TODO Document Autorun
