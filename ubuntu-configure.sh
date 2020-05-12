#!/bin/bash


# Install Chrome and Chromedriver

sudo apt-get update
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add
sudo add-apt-repository "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main"
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip -o chromedriver_linux64.zip
sudo cp chromedriver /usr/local/bin/
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver
chromedriver --version


# Install Python3 and Pip3
sudo apt-get install python3 python3-pip

# Install selenium
pip3 install Selenium
