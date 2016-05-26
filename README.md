# Household Intelligent Assistant #

This is a prototype of a speech-controlled personal assistant - easy to deploy
(on Linux), can talk about the weather, tell you (very dry) jokes, the time and
The Guardian news summary.  Attention word scanning using PocketSphinx (locally,
no background streaming to the cloud), speech reco powered by Google, intent
detection by wit.ai.  It responds to the name **Phoenix** /ˈfiːnɪks/.  Enjoy!

Quick demo: https://www.youtube.com/watch?v=xOZluGa_lwc

## Installation Instructions ##
To install the application, please follow these steps:
```
git clone https://github.com/brmson/Personal-Assistant.git
```
Due to many other libraries dependencies and audio configuration problems, we do not recommend to install it on your personal laptop. We recommned to use virtual machine handled by Vagrant or to run Docker container. If still local installation is required, please follow Ansible playbooks in the folder `deploy/ansible/`.

### Virtual Machine by Vagrant ###
To create clear virtual machine, Vagrant with provisioning tool Ansible is used. Follow these commands:
```
cd Personal-Assistant/deploy/vagrant/
vagrant up
```
To enter the virtual machine and run the application, please type:
```
vagrant ssh
sudo -i
./run.py
```
The virtual machine has to have access to you microphone and speakers. You can check it in you VirtualBox GUI application.

For testing of intent detection and development of new domains, aside of
the speech interface there is also a web-based text interface available.
The web application on port 80 can be launched by typing following
command inside the virtual machine:
```
./webapp.py
```

### Docker container ###

**Deprecated for now.**
Due to problems with audio transfering into Docker containers, *only
the web application* is available in Docker containers, no speech reco.

You can build you own Docker image by
```
docker build --tag phoenix Personal-Assistant/deploy/docker/
```
and then run the container
```
docker run -d -p 80:80 --name phoenix phoenix
```
which will run the web application at the port 80.

## Tuning Instructions ##

A major tunable of the assistant are thresholds for attention word recognition
and silence after speech input.  Tune these in /root/config.yml (inside the
virtual machine) by changing threshold in attword: (larger is less sensitive)
and speechToText: section (larger is more noise resistant, requires louder
speech input).

Errors and other debug information is logged to the /root/logs directory.

## Intent recognition database ##

Our system uses wit.ai for parsing questions. It is possible to create a fork of our wit.ai application and extend its scope to your custom intents. You need to sign up with wit.ai and than use the link below.

https://wit.ai/drapejak/Household2

## Developers ##
  - [Jiří Burant](https://github.com/JBurant)
  - [Jakub Drápela](https://github.com/drapejak)
  - [Martin Klučka](https://github.com/Kluckmar)
  - [Petr Kovář](https://github.com/kovarp15)
  - [Jakub Konrád](https://github.com/konrajak)
  - [Pavel Trutman](https://github.com/PavelTrutman)

Special thanks to [Petr Baudiš](https://github.com/pasky) and Jan Šedivý for indroducing us into the problem and for their help.

This is a student project, so discretion re code quality is welcome. ;-)
