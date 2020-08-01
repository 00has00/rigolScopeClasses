# Rigol Scope by Etherenet
This is a collection of python classes and utilities to support very basic configuration actions on a Rigol MSO 5104. Feel free to use it how you will.

### Dependancies
The following additional PIP packages are requried:
* PyVISA
* PyVISA-py


###Scripts
The following shell scripts do a basic setup on a scope:
* _setup-4ch-5v.sh_ - this script will reset the scope, set the time and date, turn on all 4 channels, set the V/div to 5v and offset them all on the screen.

### Python Files:
* rigolChannel.py - provides a basic class to perform actions on channels and some command line processing to allow parametres to be passed in for ch #, scale, offset, etc.
* rigolTrigger.py - provides a basic class to perform trigger configuraiton, and command line processing ot allow the passing of parametres in.

Files are classes, but have a main() Function defined to provide example or direct access to basic functions from the command line.

Classes do not maintain state, state is queried from the device as required.
### TODO's:
* There is currently bugger all error checking and scrubbing of input data
* Implement a wider set of trigger functions
* Add ability to set up single shot capture, run/stop and change modes - YT/XY/Roll.
* Think about whether classes should directly print, or return a return string for printing elsewhere.
