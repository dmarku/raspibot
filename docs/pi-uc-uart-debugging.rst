Debugging UART-Kommunikation zwischen RPi3 und Attiny
=====================================================

Mögliche Quelle 1: UART1 unterstützt keine Parity-Bits
------------------------------------------------------

    The mini UART (ttyS0) does not support parity. I will create an overlay that uses ttyS0 for the BT modem, which may work for low baud rates and data volumes. Using it will also require the systemd script (/lib/systemd/system/hciuart.service) to be edited.
    
    https://www.raspberrypi.org/forums/viewtopic.php?f=107&t=138223#p921684
    
Mögliche Quelle 2: Baudraten
----------------------------

Mögliche Lösung 2a: Wechsel auf UART0

-   kein Bluetooth
-   evtl Remapping von BT auf UART1 mit niedrigen Baudraten:
    
    config.txt:
    
        dtoverlay=pi3-miniuart-bt
        
    Overlay, also Tausch GPIO- mit BT-UART, behebt Probleme mit Attiny-Kommunikation
    
    BT-Funktionalität nicht getestet

Mögliche Lösung 2b: Kerntakt fixieren

-   