# Jira Access Token and Load Gen config
#
export JIRA_SERVER="http://localhost:8080"
export JIRA_PRIVATE_PEM_FILE="jira_privatekey.pem"
export JIRA_CONSUMER_KEY="OauthKey"
export JIRA_CONSUMER_SECRET="Anything"
export JIRA_VERIFIER="jira_verifier"

# Selenium
export CHROMEDRIVER_EXE="/usr/local/bin/chromedriver"
export CHROME_HEADLESS="true"

# Approved OAuth Token
# Use jira-create-token - jiraCreateAccessToken() to generate these
export JIRA_OAUTH_TOKEN="REQUIRED_FOR_OAUTH"
export JIRA_OAUTH_TOKEN_SECRET="REQUIRED_FOR_OAUTH"
