from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session
from jira.client import JIRA
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import requests
import datetime
import random
import time
import string
import sys
import os

# Jira Docs
# https://jira.readthedocs.io/en/master/api.html

# Jira OAuth
# https://developer.atlassian.com/server/jira/platform/oauth/?_ga=2.11854194.792712473.1589739280-239273911.1589739280

# Atlassian OAuth Examples
# https://bitbucket.org/atlassianlabs/atlassian-oauth-examples/src/master/

def getEnvironmentConfig():
    return { "JIRA_SERVER": os.environ.get('JIRA_SERVER', 'http://localhost:8080'),
             "JIRA_PRIVATE_PEM_FILE": os.environ.get('JIRA_PRIVATE_PEM_FILE', 'jira_privatekey.pem'),
             "JIRA_CONSUMER_KEY": os.environ.get('JIRA_CONSUMER_KEY', 'OauthKey'),
             "JIRA_CONSUMER_SECRET": os.environ.get('JIRA_CONSUMER_SECRET', 'ANYTHING'),
             "JIRA_VERIFIER": os.environ.get('JIRA_VERIFIER', 'jira_verifier'),
             "JIRA_OAUTH_TOKEN": os.environ.get('JIRA_OAUTH_TOKEN', 'REQURIED'),
             "JIRA_OAUTH_TOKEN_SECRET": os.environ.get('JIRA_OAUTH_TOKEN_SECRET', 'REQURIED'),
             "CHROMEDRIVER_EXE": os.environ.get('CHROMEDRIVER_EXE', '/usr/local/bin/chromedriver'),
             "CHROME_HEADLESS": os.environ.get('CHROME_HEADLESS', '/usr/local/bin/chromedriver'),
             "v1": int( os.environ.get('V1', 5)),
             "v2": int( os.environ.get('V2', 10)) }

def readFile(file_path):
    with open(file_path) as f:
        return f.read()

def randomWord(wordLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(wordLength))

def randomSentence(wordLength=8, words=6):
    return ' '.join(randomWord(wordLength) for i in range(words))


def read(file_path):
    """ Read a file and return it's contents. """
    with open(file_path) as f:
        return f.read()

def jiraCreateAccessToken():
    # The Consumer Key created while setting up the "Incoming Authentication" in
    # JIRA for the Application Link.
    CONSUMER_KEY = 'OauthKey'
    CONSUMER_SECRET = 'dont_care'
    VERIFIER = 'jira_verifier'

    # The contents of the rsa.pem file generated (the private RSA key)
    RSA_KEY = readFile('jira_privatekey.pem')

    # The URLs for the JIRA instance
    REQUEST_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/request-token'
    AUTHORIZE_URL = JIRA_SERVER + '/plugins/servlet/oauth/authorize'
    ACCESS_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/access-token'

    # Step 1: Get a request token
    oauth = OAuth1Session(CONSUMER_KEY, client_secret= CONSUMER_SECRET, signature_method=SIGNATURE_RSA, rsa_key=RSA_KEY)
    request_token = oauth.fetch_request_token(REQUEST_TOKEN_URL)

    resource_owner_key = request_token['oauth_token'];
    resource_owner_secret = request_token['oauth_token_secret'];

    print("STEP 1: GET REQUEST TOKEN")
    print("  oauth_token={}".format(resource_owner_key))
    print("  oauth_token_secret={}".format(resource_owner_secret))
    print("\n")

    # Step 2: Get the end-user's authorization
    print("STEP2: AUTHORIZATION")
    print("  Visit to the following URL to provide authorization:")
    print("  {}?oauth_token={}".format(AUTHORIZE_URL, request_token['oauth_token']))
    print("\n")

    input("Press any key to continue...")

    oauth = OAuth1Session(CONSUMER_KEY, client_secret= CONSUMER_SECRET,
                            resource_owner_key=resource_owner_key,
                            resource_owner_secret=resource_owner_secret,
                            verifier=VERIFIER,
                            signature_method=SIGNATURE_RSA, rsa_key=RSA_KEY)

    # Step 3: Get the access token
    access_token = oauth.fetch_access_token(ACCESS_TOKEN_URL)

    print("STEP2: GET ACCESS TOKEN")
    print("  oauth_token={}".format(access_token['oauth_token']))
    print("  oauth_token_secret={}".format(access_token['oauth_token_secret']))
    print("\n")

    # Now you can use the access tokens with the JIRA client. Hooray!
    jira = JIRA(options={'server': JIRA_SERVER}, oauth={
        'access_token': access_token['oauth_token'],
        'access_token_secret': access_token['oauth_token_secret'],
        'consumer_key': CONSUMER_KEY,
        'key_cert': RSA_KEY
    })

    # Test the Access
    for project in jira.projects():
        print(project.key)


class JiraUI():
    config = { }

    def __init__(self, config):
        self.config =  config
        chromeOptions = Options()
        if self.config["CHROME_HEADLESS"]:
            chromeOptions.add_argument('--headless')
            chromeOptions.add_argument("--window-size=640,320")
        print( "Loading webkit and selenium")
        self.driver = webdriver.Chrome(options=chromeOptions, executable_path=config['CHROMEDRIVER_EXE'])

    def configure(self, user, password):
            self.config["user"] = user
            self.config["password"] = password

    def login(self):
        self.driver.get( "http://jiralinuxtrialprep-jira-tynu5ggq.appd-sales.com:8080/login.jsp" )
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form-username")))
        id2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form-password")))
        id3 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form-submit")))
        id1.send_keys(self.config["user"] )
        id2.send_keys(self.config["password"])
        id3.click()
        time.sleep(1)
        print( "Title: ", self.driver.title )

    def logout(self):
        self.driver.get( "http://jiralinuxtrialprep-jira-tynu5ggq.appd-sales.com:8080/logout" )
        id4 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "confirm-logout-submit")))
        id4.click()

    def issuesSearch(self):
        self.driver.get( "http://jiralinuxtrialprep-jira-tynu5ggq.appd-sales.com:8080/browse" )
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "quickSearchInput" )))
        s1 = "APPD-"+str(random.randint(1,20000))
        print( "Searching for ", s1 )
        id1.send_keys(s1)
        id1.send_keys(u'\ue007') # Enter
        #id1.click()

    def issuesSearchLatest(self):
        self.driver.get( "http://jiralinuxtrialprep-jira-tynu5ggq.appd-sales.com:8080/browse" )
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "quickSearchInput" )))
        #s1 = randomString(3)
        #s1 = "APPD-"+str(random.randint(1,200))
        #print( "Searching for ", s1 )
        #id1.send_keys(s1)
        id1.send_keys(u'\ue007') # Enter
        #id1.click()

    def issuesCreate(self):
        self.driver.get("http://jiralinuxtrialprep-jira-tynu5ggq.appd-sales.com:8080//secure/CreateIssue!default.jspa")
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "summary" )))
        id1.send_keys("Summary_{}".format(randomSentence()))
        id2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "duedate" )))
        id2.send_keys("30/May/20")
        id3 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "issue-create-submit" )))
        id3.click()

    def issuesComment(self):
        # Should be on an Issue Page
        #self.driver.get("http://jiralinuxtrialprep-jira-tynu5ggq.appd-sales.com:8080//secure/CreateIssue!default.jspa")
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "footer-comment-button" )))
        id1.click()

        if1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe" )))
        self.driver.switch_to.frame(if1)

        #id2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "comment-wiki-edit" ))) # "tinymce"
        id3 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "tinymce" ))) # "tinymce"
        s1 = "Comment from {} - {}".format(self.config["user"],randomSentence())
        print( s1)
        id3.send_keys(s1)

        self.driver.switch_to.default_content()
        id4 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "issue-comment-add-submit" )))
        id4.click()

    def issuesDone(self):
        # Should be on an Issue Page
        #self.driver.get("http://jiralinuxtrialprep-jira-tynu5ggq.appd-sales.com:8080//secure/CreateIssue!default.jspa")
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "action_id_21" )))
        id1.click()

    def configBasicAuth(self, userList):
        self.userList = userList

    def run(self, iterations, delaySec):
        commands = ["search", "comment", "create", "done" ]
        commandsWeights =  [1,1,1,1]
        j = JiraUI(config)
        for i in range(0, iterations):
            user = random.choice(self.userList)
            jiraCmd = random.choices(population=commands, weights=commandsWeights)[0]
            print( "Iteration {} {} [{}]".format(i, user, jiraCmd))
            try:
                j.configure(user[0], user[1])
                j.login()
                if jiraCmd == 'search':
                    j.issuesSearch()
                elif jiraCmd == 'comment':
                    j.issuesSearchLatest()
                    j.issuesComment()
                elif jiraCmd == 'create':
                    j.issuesCreate()
                elif jiraCmd == 'done':
                    j.issuesSearch()
                    j.issuesDone()
                else:
                    print( "unknown command ", jiraCmd)
                j.logout()
                time.sleep(delaySec)
            except Exception as e:
                print( e )


class JiraAPI():
    def __init__(self, config):
        self.config = config

    def configBasicAuth(self, userList):
        self.jiraAccess = [ JIRA(options={'server': self.config['JIRA_SERVER']}, basic_auth=user) for user in userList ]

    def configOAuth(self):
        oauth_token = self.config['JIRA_OAUTH_TOKEN']
        oauth_token_secret = self.config['JIRA_OAUTH_TOKEN_SECRET']
        CONSUMER_KEY = self.config['JIRA_CONSUMER_KEY']
        RSA_KEY = read(self.config['JIRA_PRIVATE_PEM_FILE'])
        JIRA_SERVER = self.config['JIRA_SERVER']
        self.jiraAccess = [ JIRA(options={'server': JIRA_SERVER}, oauth={
            'access_token': oauth_token,
            'access_token_secret': oauth_token_secret,
            'consumer_key': CONSUMER_KEY,
            'key_cert': RSA_KEY
        }) ]

    def createIssue(self, jira):
        fields = { 'project': {'key': 'APPD'},
                   'summary': randomSentence(8, 2), 'description': randomSentence(8, 6),
                   'issuetype': {'name': random.choice(['Bug','Story'])} }
        jira.create_issue( fields )

    def run(self, iterations, delaySec):
        loadCommands = [("search",100), ("comment",1), ("create",100), ("done",1),
                        ("projects",100), ("searchUsers",100), ("jqlToDo",100) ]
        loadPopulation = [i[0] for i in loadCommands]
        loadWeights = [i[1] for i in loadCommands]
        for i in range(0, iterations):
            jira = random.choice(self.jiraAccess)
            jiraCmd = random.choices(population=loadPopulation, weights=loadWeights)[0]
            print( "Iteration {} {} [{}]".format(i, jira, jiraCmd))
            if jiraCmd == 'search':
                pass
            elif jiraCmd == 'comment':
                pass
            elif jiraCmd == 'create':
                self.createIssue(jira)
            elif jiraCmd == 'projects':
                for project in jira.projects():
                    print(project.key)
            elif jiraCmd == 'done':
                pass
            elif jiraCmd == 'searchUsers':
                print( jira.search_users('.') )
            elif jiraCmd == "jqlToDo":
                print( jira.search_issues('Project = APPD AND status = "To Do"') )
            else:
                print( "unknown command ", jiraCmd)
            time.sleep(delaySec)

def getArgs1():
    if nArgs > 3:
        iterations = int( sys.argv[2] )
        delaySec = int( sys.argv[3] )
    else:
        iterations = 1
        delaySec = 0
    return iterations, delaySec

config = getEnvironmentConfig()

userListBasic = [ ("u1", "welcome1"), ("dryder", "welcome1") ]

cmd = "help"
nArgs = len(sys.argv)
if nArgs > 1:
    cmd = sys.argv[1]

if cmd == "load-api-basic":
    iterations, delaySec = getArgs1()
    j = JiraAPI(config)
    j.configBasicAuth( userListBasic )
    j.run(iterations, delaySec)

elif cmd == "load-api-oauth":
    iterations, delaySec = getArgs1()
    j = JiraAPI(config)
    j.configOAuth()
    j.run(iterations, delaySec)

elif cmd == "load-ui":
    iterations, delaySec = getArgs1()
    j = JiraUI(config)
    j.configBasicAuth( userListBasic )
    j.run(iterations, delaySec)

elif cmd == "jira-create-token":
    jiraCreateAccessToken()

elif cmd == "test-config":
    config = getEnvironmentConfig()
    for i in config.keys():
        print( "{} : {}".format(i, config[i]))


elif cmd == "help":
    print( "load-api-basic")
    print( "load-api-oauth")
    print( "load-ui")
    print( "jira-create-token" )
    print( "test-config" )

else:
    print("Unknown cmd: ", cmd )
