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

# Maintainer: David Ryder, david.ryder@appdynamics.com

chromeDriverExe = "/usr/local/bin/chromedriver"

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
        #self.options.add_argument("--window-size=640,320")
        self.options.add_argument('--headless')
        print( "Loading webkit and selenium")
        self.driver = webdriver.Chrome(options=self.options, executable_path=chromeDriverExe)

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

    def issuesSearchLatest(self):
        self.driver.get( "http://jiralinuxtrialprep-jira-tynu5ggq.appd-sales.com:8080/browse" )
        id1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "quickSearchInput" )))
        id1.send_keys(u'\ue007') # Enter

    def issuesCreate(self):
        self.driver.get("http://jiralinuxtrialprep-jira-tynu5ggq.appd-sales.com:8080//secure/CreateIssue!default.jspa")
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
        for i in range(0, iterations):
            user = random.choices(population=users, weights=usersWeights)[0]
            password = "welcome1"
            jiraCmd = random.choices(population=commands, weights=commandsWeights)[0]
            print( "Iteration {} {} [{}]".format(i, user, jiraCmd))
            try:
                j.configure(user, password)
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
    else:
        print("Unknown command ", cmd)
    # End time
    responseTime = int((datetime.datetime.now() - startTime).total_seconds() * 1000)

    print( "Response Time ", responseTime )


    print( "Complete")
