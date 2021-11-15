# rs_toolkit

This is my hobby project where I implement platform independent tools for RuneScape (similar to [Runescape Alt1 Toolkit](https://runeapps.org/alt1) which only supports Windows) like Croesus timer, clue scroll solver, etc.

The GUI is a ```Qt``` based transparent, frameless, click-through and always on top window:

![simplescreenrecorder-2021-11-16_00 20 19](https://user-images.githubusercontent.com/69594364/141868110-932efb12-7d3f-4a3e-977a-68351101e721.gif)

which can visualize defult drawables like ```Point```, ```Line```, ```Rect```, ```Image```, etc..

As this script draws on top of every window it is not possible to grab a screenshot of the full screen. For Linux I use ```Xlib``` and for Windows I use ```win32gui``` and ```win32con``` to grab image of the RuneScape window. It works even if the window minimized or off screen.

I implemented a ```Clock``` class which precisely ```sleep``` between algo and gui updates to match de desired (30) FPS.


(to be continued ..)
