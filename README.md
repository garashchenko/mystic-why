# Mystic Why

This application allows to apply user developed RGB effects for newer MSI motherboards. 

**CAUTION!** The application is not stable and may harm your hardware. It interacts with motherboard's RGB controller HID device and there were cases of [bricked RGB controllers](https://gitlab.com/CalcProgrammer1/OpenRGB/-/issues/389). This has been only tested for MSI Z490 Gaming Plus (MS-7C75). Please refer to the list of motherboards with the same RGB controller. I am not responsible for any damage to your hardware so proceed with caution.
There is a **known issue**: if something goes wrong, the application is closed and lightning gets 'stuck' you can use Mystic Light tool to reset it by applying any lightning effect. It may not react to Apply button for a while but should work in the end. It happens when a per led lightning effect had been used but the application was closed incorrectly. A 185-byte packed should be sent to a controller for it to return to a full lightning mode which can be done by Mystic Light.  

This project is more of a proof-of-concept of controlling newer motherboards and creating effects with per LED lightning.

## Compatible motherboards
| Model | Tested  |
|--|--|
|MS_7C67|no
|MS_7B10|no
|MS_7C87|no
|MS_7B93|no
|MS_7C34|no
|MS_7C35|no
|MS_7C36|no
|MS_7C37|no
|MS_7C42|no
|MS_7C84|no
|MS_7B94|no
|MS_7B96|no
|MS_7C59|no
|MS_7C60|no
|MS_7C70|no
|MS_7C71|no
|MS_7C73|no
|MS_7C75|**yes**
|MS_7C76|no
|MS_7C77|no
|MS_7C79|no
|MS_7C80|no
|MS_7C98|no
|MS_7C99|no
|MS_7C81|no
|MS_7C82|no
|MS_7C83|no
|MS_7C85|no
|MS_7C86|no
|MS_7C88|no
|MS_7C89|no
|MS_7D03|no
|MS_7D04|no
|MS_7D05|no
|MS_7D06|no
|MS_7D07|no
|MS_7D08|no
|MS_7D09|no
|MS_7D10|no
|MS_7D11|no
|MS_7D12|no
|MS_7D15|no
|MS_7D17|no
|MS_7D18|no
|MS_7D19|no
|MS_7D20|no
|MS_7D22|no
|MS_4459|no
|MS_3EA4|no
|MS_905D|no
|MS_7C90|no
|MS_7C91|no
|MS_7C92|no
|MS_7C94|no
|MS_7C95|no
|MS_7C96|no
|MS_7C56|no
|MS_7D13|no
|MS_7D14|no

## Effects
Currently there are three types of effects implemented:
 - Police lights which I implemented mainly for testing
 - Hue wheel which allows you to cycle between selected colors
 - Sweep which runs a single LED of a selected color through all the LEDs of background color

Here is a short video of these effects: [video](https://www.youtube.com/watch?v=I_q0ZEQXTls)
 
There is a base class created both for full area lightning effects and per led lightning effects. The first one sends a 185 byte message and affects all the RGB in the selected area. The second one allows you to control every single LED in the selected area individually by sending a 725 byte message. 

Every effect added  to the effects directory is automatically imported and displayed in the GUI. 

## Credits
I would like to mention a few projects and ideas I found online which helped me a lot:

 - [MSIRGB](https://github.com/ixjf/MSIRGB) - a projects which allows you to do things Mystic Why does but better. Unfortunately it doesn't support newer motherboards.
 - [OpenRGB](https://gitlab.com/CalcProgrammer1/OpenRGB) - a project aimed at controlling all the RGB using one piece of software. There were some problems with newer MSI motherboards but they were [solved recently](https://gitlab.com/CalcProgrammer1/OpenRGB/-/issues/389) . This issue helped me a lot avoiding bricking my own motherboard.
 - [This issue](https://github.com/nagisa/msi-rgb/issues/54) helped a lot with finding tools for researching Mystic Light's behavior
