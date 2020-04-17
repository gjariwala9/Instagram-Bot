import sys
from selenium import webdriver
from getpass import getpass
from time import sleep

class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome("C://Windows//chromedriver_win32//chromedriver.exe")
        self.username = username
        self.driver.get("https://www.instagram.com/")
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(pw)
        
        try:
        	self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button').click()
        	sleep(4)
	        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()
	        sleep(4)
        except Exception as e:
        	print(f'Loggin failed. Please check your username and password.')
        	self.close_browser()
        	sys.exit(1)
        
    def get_unfollowers(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a').click()
        sleep(4)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        following = self._getnames()
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        followers = self._getnames()
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)
        self._store_to_text_file(not_following_back)
        
        
    def _getnames(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_ht, ht=0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        return names

    def _store_to_text_file(self, unfollowers):
    	with open('unfollowers.txt', 'w') as f:
		    for unfollower in unfollowers:
		        f.write("%s\n" % unfollower)


    def close_browser(self):
    	self.driver.quit()
    
    
username = input("Enter Username: ")
password = getpass()    
my_bot = InstaBot(username, password)       
my_bot.get_unfollowers()
my_bot.close_browser()
