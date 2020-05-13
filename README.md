# AppD-Jira-LoadGen

Generate load for JIRA, performs: create, search, add comment, done operations across a range of users

Requires Chrome and Chromedriver installed

Clone this repository:

`git clone https://github.com/Appdynamics/AppD-Jira-LoadGen.git`

Update the OS, with Python, Selenium and Chrome using:

`./ubuntu-update.sh`

Configure the environment in `envvars.sh`

Generate load using the command:

`python3 jira1.py test1 10 1`
