Einrichtung eines frisch installierten Raspbian-Images
======================================================

Sprache und Tastaturlayout einstellen
-------------------------------------

TODO

Es gab mal/gibt das Problem, dass im Betrieb angesteckte Tastaturen mit englischem Layout eingerichtet werden.

Interfaces konfigurieren
------------------------

.. code-block:: shell
  
  sudo raspi-config
  
Folgende Optionen müssen eingestellt sein:

-  "5 Interfacing Options"
    -  "P1 Camera": enable
    -  "P4 SPI": enable
    -  "P5 I2C": enable
    -  "P6 Serial": no login shell, hardware enabled
    
dann "reboot now" mit "yes" bestätigen

GPIO-Avrdude einrichten
-----------------------

AVRdude ab Version 6.1 hat den linuxspi-Programmer schon dabei, der ist in den Raspbian-Repos

Test:

.. code-block:: shell
  
  avrdude --version
  avrdude -c list
  
das '-c list'-Kommando listet alle unterstützten Programmertypen auf, darunter sollte ein "linuxspi" sein

Reset an GPIO 4 (Board-version 1 & 2): Datei /etc/avrdude.conf bearbeiten, dort RESET und BAUDRATE setzen (bei mir war eine Baudrate von 400000 voreingestellt, da schlug die Programmierung fehl):

::
  
  programmer
    id = "linuxspi";
    desc = "Use Linux SPI device in /dev/spidev*";
    type = "linuxspi";
    reset = 4;
    baudrate = 200000;
  ;
  
PROBLEM beim überspielen: "unable to write /sys/class/gpio/gpio4/direction". Programmieren klappt nur jedes zweite mal, daher vielleicht ein Timing-Fehler?

Kann man mit "echo 'out' > /sys/class/gpio/gpio4/direction" manuell umgehen, dann gibts aber:

PROBLEM beim Überspielen: "AVR device not responding, initialization failed". Gelöst durch runtersetzen der Baudrate von 400000 auf 200000.

AVR-Compiler einrichten
-----------------------

.. code-block:: shell
  
  sudo apt install gcc-avr avr-libc avrdude
  
UART-Test
---------

.. code-block:: shell
  
  sudo apt install ipython3

.. code-block:: python
  
  from serial import Serial, PARITY_EVEN
  # Raspberry Pi 3 changes the GPIO UART device file from "ttyAMA0" to "ttyS0"
  u = Serial("/dev/ttyS0", baudrate=4800, stopbits=2, parity=PARITY_EVEN)
  
  ALIVE = 0x01.to_bytes(1, byteorder='little')
  ACK = 0x10.to_bytes(1, byteorder='little')
  
  u.write(ALIVE)
  response = u.read(1)
  if response == ACK:
    print("Yay!")
  else:
    print("Nay.")
    
Anmerkungen
'''''''''''

-  ``raspibot.AttinyUart``-API-Calls geben Fehler: ``'str' does not support the buffer interface``

- Befehle haben sich in neuer uC-Firmware teilweise geändert

============== =========== =================== =============================
Befehl         Kommando    Gesendet            Empfangen
============== =========== =================== =============================
Alive?         0x01        -                   1B: ACK
Enc_Right      0x02        -                   2B: MSB LSB
Enc_Left       0x03        -                   2B: MSB LSB
Enc_Both       0x04        -                   4B: L_MSB L_LSB R_MSB R_LSB
Reset_Left     0x05        -                   1B: ACK
Reset_Right    0x06        -                   1B: ACK
Reset_Both     0x07        -                   1B: ACK
Buzzer         0x40        5B: MSB LSB ...     1B: ACK
============== =========== =================== =============================


Encoder
-------

Hersteller-Link: https://www.pololu.com/product/3081

Pinout, Draufsicht, Magnetscheibe oben, Pins oben:

Betrieb mit 3.3V


Buttons
-------

Button-LEDs und -Taster liegen auf GPIO-Pins. LED-Outputs müssen auf LOW gesetzt werden, um die LEDs leuchten zu lassen. Die Taster sind High-Aktiv, d.h. sie verbinden den Pin mit VCC, wenn sie gedrückt werden und werden sonst über einen Pull-Down-Widerstand an Masse angelegt.

======== === ==== ======
\          LED    
-------- -------- ------
Position rot grün Taster
======== === ==== ======
Links    26  23   13
Mitte    20  24   19
Rechts   21  25   16
======== === ==== ======

.. code-block:: python
  
  import RPi.GPIO as GPIO
  GPIO.setmode(GPIO.BCM)
  
  GPIO.setup([20, 21, 23, 24, 25, 26], direction=GPIO.OUT, initial=1)
  
  # Ampel
  GPIO.output(26, 0)
  GPIO.output([20, 24], 0)
  GPIO.output(25, 0)
  
  GPIO.setup([13, 16, 19], direction=GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  
LCD
---

-  HD44780-kompatibler LCD-Controller
-  Leitungen:
   
   ===================== ================================== ================
   Kategorie             Pinout                             RasPi-GPIO
   --------------------- ---------------------------------- ----------------
   Spannungsquelle       Ground                             
   \                     VCC
                         
   Display               Contrast adjust
   \                     Backlight anode
   \                     Backlight Cathode
                         
   Datenleitungen        Register Select                    GPIO 17
   \                     Read/~Write                         GPIO 18
   \                     Clock bzw. Enable (falling edge)   GPIO 27
   \                     Bit 0-3 (für 8-Bit-Modus)          nicht verbunden
   \                     Bit 4-7 (8-Bit- und 4-Bit-Modus)   GPIO 8, 7, 5, 6
   ===================== ================================== ================
   
-  Befehle haben maximale Ausführungszeiten
-  Controller hat Busy Flag (BF), kann über Read=1

- MERKE: Beim Initialisieren ALLE Steuerfunktionen explizit setzen (und einmal clearen)
    - 4-Bit-Modus initialisieren
    - entry mode: cursor LTR, no shift
    - display control: display on, cursor whatever
    - function: 2 lines, 4-bit data, 5x8 character size

I2C-Bus
-------

Im Paket *i2c-tools* gibt es einige nützliche Kommandozeilenprogramme, darunter ``i2cdetect``, das erreichbare Adressen auf einem Bus scant.

Um auf dem Bus ``i2c-1`` nach Geräten zu scannen: (Die Option ``-y`` unterdrückt die Warnung, dass die Suche den i2c-Bus verwirren kann)

::
  i2cdetect -y 1

Python 3 SMbus kennt kein read/write_word_data mehr -> nur noch r/w_byte_data

read_byte_data() liefert negative Werte? Sind das Fehlercodes?

cffi-smbus
''''''''''

erfordert 'apt install libffi-dev' und 'pip3 install --user cffi-smbus'

scheint zu funktionieren, ebenfalls mit 'import smbus', exportiert '\*_word_data()'

ADC
'''

ADC hat vier Register. Die Register sind 16 bit breit

-  Conversion Register: Ergebnis der letzten Analog-Digital-Wandlung (Adresse 0), cleared to 0
-  Konfig-Register: Betriebsparameter (Adresse 1)
-  Low & High Threshold Register (Adressen 2, 3)

Der Controller überträgt die 16 Bit-Werte in Big Endian (MSB first), im Gegensatz
zur SMBus-Konvention, Werte aus mehreren Bytes in Little Endian zu serialisieren.
Daher ist ein manuelles Tauschen der Bits beim Senden und Empfangen notwendig,
um die in der Doku erwähnten Bits auch so ansprechen zu können.

Die Adresse wird über den ADDR-Pin festgelegt. Man kann zwischen vier Adressen
auswählen, indem man den Pin wahlweise mit Ground, VDD, SDA oder SCL verbindet.
Auf der Platine ist der Pin mit VDD verbunden; der ADC ist über die Adresse 0x49 erreichbar.

Zusätzlich zum I2C-Bus gibt es noch eine Alert-Leitung, die 

config-register
***************

===== =========================================================================== =========================
Bits  Bedeutung                                                                   Default
----- --------------------------------------------------------------------------- -------------------------
15    OS; Operational Status (read), conversion start in power-down modus (write) 1 (no conv)
14:12 MUX; Input multiplexer                                                      000 (In0 zu In1)
11:9  PGA; Eingabeverstärker                                                      010 (+/-2.048 V)
8     Mode; Betriebsmodus                                                         1 (single-shot)
7:5   Datenrate                                                                   100 (1600 Samples/s)
4     Comparator mode                                                             0 (trad. with hysteresis)
3     Comparator polarity                                                         0 (active low)
2     Comparator latch                                                            0 (non-latching)
1:0   Comparator queue & disable                                                  11 (disable)
===== =========================================================================== =========================