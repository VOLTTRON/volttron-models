# README #

This repository contains simple equipment and zone models that can be used by VOLTTRON agents. These models are not agents themselves an should be installed into the VOLTTRON virtual environment and extended or imported by agents requiring this functionality. This README contains instructions for installing these modules into the VOLTTRON virtual environments' site-packages directory.

## DEPENDENCIES ##

The following instructions assume you have already cloned this repository.

Make sure you have installed [VOLTTRON](https://github.com/VOLTTRON/volttron) and its dependencies.

## INSTALLATION ##

Enable the VOLTTRON virtual environment
~~~
$ . [VOLTTRON repository location]/env/bin/activate
~~~
Install the package.
~~~
$ cd [volttron-models repository location]
$ python setup.py install
~~~
