from selenium import webdriver
import os
import random
import urllib.request as ulib
from essential_generators import DocumentGenerator
from instabot import Bot

# set the instagram account username that you're uploading to
username = ''
# set the instagram account password that you're uploading to
password = ''

# function that gets a random word from either nouns.txt or people.txt
def getWord():
	index = random.randint(0, 1)
	print(index)
	if index == 1:
		file = open('nouns.txt', 'r')
	else:
		file = open('people.txt', 'r')
	lines = file.readlines()
	file.close()
	index = random.randint(0, len(lines))
	word = lines[index] + "\n"
	return word



# get the path of the chrome driver (this assume that the 
# chrome driver is located in this directory)
chrome_path=os.path.dirname(os.path.realpath(__file__))
chrome_path += '/chromedriver'

directory = "images"

# open the chrome driver to google images
driver = webdriver.Chrome(chrome_path)
driver.get("https://images.google.com/")

# generate a new word and search for it in the chrome driver
word = getWord()
search = driver.find_element_by_name("q")
search.send_keys(word)

# grab all of the image elements
images = driver.find_elements_by_class_name("rg_i")

# download one of the first 10 images
num = random.randint(0, 10)
img_url = images[num].get_attribute('src')
images_path = os.path.join(directory, "image.jpg")
ulib.urlretrieve(img_url,str(images_path))

# generate a sentence to be used in the caption
gen = DocumentGenerator()
sentence = gen.sentence()

# log in to instagram and post the image and caption
bot = Bot()
bot.login(username = username, password = password)
bot.upload_photo(str(images_path), caption = sentence)
