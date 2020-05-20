# AppD-Jira-LoadGen

Generate load for JIRA, performs: create, search, add comment, done operations across a range of users

Requires Chrome and Chromedriver installed

Clone this repository:

`git clone https://github.com/Appdynamics/AppD-Jira-LoadGen.git`

Update the OS, with Python, Selenium and Chrome using:

`./ubuntu-update.sh`

Configure the environment in `envvars.sh`

Generate UI load using the command:

`python3 jira-api-load-gen.py load-ui 10 2`

Generate API load with basic auth using the command:

`python3 jira-api-load-gen.py load-api-basic 10 2`

To generate a load using OAuth, a private/public key is needed along with a Jira Application Link

The following scripts will help with this:

`jira-key-gen.sh`

Generate the OAuth token configure `envvars.sh`

`python3 jira-api-load-gen.py jira-create-token`

API load with OAuth  using the command:

`python3 jira-api-load-gen.py load-api-oauth 10 2`
