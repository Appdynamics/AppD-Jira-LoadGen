from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import datetime
import random
import time
import string
import sys
import os

# Maintainer: David Ryder, david.ryder@appdynamics.com



def getEnvironmentConfig():
    return { "chromeDriverExe": os.environ.get('CHROME_DRIVER_EXE', '/usr/local/bin/chromedriver'),
             "chromeHeadLess": os.environ.get('CHROME_HEADLESS').lower() == "true",
             "jiraHost": os.environ.get('JIRA_HOST', 'REQUIRED'),
             "jiraPort": os.environ.get('JIRA_PORT', 'REQUIRED'),
             "jiraProtocol": os.environ.get('JIRA_PROTOCOL', 'http'),
             "jiraPassword": os.environ.get('JIRA_PASSWORD', "REQUIRED") }

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def randomID(stringLength=3):
    letters = [ "a", "b", "c" ]
    return ''.join(random.choice(letters) for i in range(stringLength))

def randomSentence(words=6, wordLength=8):
    return ' '.join(randomString() for i in range(words))

class Jira():
    config = { "user": "", "password": "" }

    def __init__(self):
        self.config["user"] = "REQUIRED"
        self.config["password"] = "REQUIRED"
        self.options = Options()


    def configure(self, config):
            self.config["user"] = config["jiraPassword"]
            self.config["password"] = ""
            self.config["jiraHost"] = config["jiraHost"]
            self.config["jiraPort"] = config["jiraPort"]
            self.config["jiraProtocol"] = config["jiraProtocol"]
            self.config["chromeDriverExe"] = config["chromeDriverExe"]
            self.config["chromeHeadLess"] = config["chromeHeadLess"]

    def startChrome(self):
        chromeOptions = Options()
        chromeOptions.add_argument("--window-size=640,320")
        if self.config["chromeHeadLess"]:
            chromeOptions.add_argument('--headless')
        print( "Loading Chrome webkit")
        self.driver = webdriver.Chrome(options=chromeOptions, executable_path=self.config["chromeDriverExe"] )

    def getURL(self, service):
        return "{protocol}://{host}:{port}/{service}".format(protocol=self.config["jiraProtocol"],
                host=self.config["jiraHost"], port=self.config["jiraPort"], service=service)

    def login(self, user, password):
        self.driver.get( self.getURL("login.jsp") )
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form-username")))
        id2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form-password")))
        id3 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form-submit")))
        id1.send_keys(user)
        id2.send_keys(password)
        id3.click()
        time.sleep(1)
        print( "Title: ", self.driver.title )

    def logout(self):
        self.driver.get( self.getURL("logout" ) )
        id4 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "confirm-logout-submit")))
        id4.click()

    def issuesSearch(self):
        self.driver.get( self.getURL("browse" ) )
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "quickSearchInput" )))
        s1 = "APPD-"+str(random.randint(1,20000))
        print( "Searching for ", s1 )
        id1.send_keys(s1)
        id1.send_keys(u'\ue007') # Enter

    def issuesSearchLatest(self):
        self.driver.get( self.getURL("browse" ) )
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "quickSearchInput" )))
        id1.send_keys(u'\ue007') # Enter

    def issuesCreate(self):
        self.driver.get( self.getURL("CreateIssue!default.jspa" ) )
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "summary" )))
        id1.send_keys("Summary_{}".format(randomSentence()))
        id2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "duedate" )))
        id2.send_keys("30/May/20")
        id3 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "issue-create-submit" )))
        id3.click()

    def issuesComment(self):
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
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "action_id_21" )))
        id1.click()

# Start time
startTime = datetime.datetime.now()
users =        [ "u1", "u2", "u3", "u4", "u5", "dryder", "nouser" ]
usersWeights = [ 1 ,    1,    1,    1,    1,    5,  1 ]
commands = ["search", "comment", "create", "done" ]
commandsWeights =  [1,1,1,5]

config = getEnvironmentConfig()

nArgs = len(sys.argv)
if nArgs > 1:
    cmd = sys.argv[1]

    if cmd == "test1":
        if nArgs > 3:
            iterations = int( sys.argv[2] )
            delaySec = int( sys.argv[3] )
        else:
            iterations = 1
            delaySec = 0

        j = Jira()
        j.configure(config)
        j.startChrome()
        for i in range(0, iterations):
            user = random.choices(population=users, weights=usersWeights)[0]
            password = config["jiraPassword"]
            jiraCmd = random.choices(population=commands, weights=commandsWeights)[0]
            print( "Iteration {} {} [{}]".format(i, user, jiraCmd))
            try:
                j.login(user, password)
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
    else:
        print("Unknown command ", cmd)
    # End time
    responseTime = int((datetime.datetime.now() - startTime).total_seconds() * 1000)

    print( "Response Time ", responseTime )


    print( "Complete")
