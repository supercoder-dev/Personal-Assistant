# Household Intelligent Assistant #

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

The web application on the port 80 can be launched by typing following command inside the virtual machine:
```
./webapp.py
```

### Docker container ###
You can build you own Docker image by
```
docker build --tag phoenix Personal-Assistant/deploy/docker/
```
and then run the container
```
docker run -d -p 80:80 --name phoenix phoenix
```
which will run the web application at the port 80.

Due to problems with audio transfering into Docker containers, the web application is available only in Docker containers.

## Developers ##
  - [Jiří Burant](https://github.com/JBurant)
  - [Jakub Drápela](https://github.com/drapejak)
  - [Martin Klučka](https://github.com/Kluckmar)
  - [Petr Kovář](https://github.com/kovarp15)
  - [Jakub Konrád](https://github.com/konrajak)
  - [Pavel Trutman](https://github.com/PavelTrutman)

Special thanks to [Petr Baudiš](https://github.com/pasky) and Jan Šedivý for indroducing us into the problem and for their help.
