import sys
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# Get the URL of the page containing the images to be scraped from command-line argument
if len(sys.argv) < 2:
    print("Usage: python image-scraper.py <url>")
    sys.exit()
url = sys.argv[1]

# Set the local folder to which the images will be downloaded
folder_path = 'images/'

# Create the folder if it does not already exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Send a GET request to the URL and parse the HTML using BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all image tags in the HTML and download each image to the local folder
for img in soup.find_all('img'):
    img_url = img.get('src')
    if img_url.startswith('http'):
        # remove query parameters from the image URL
        parsed_url = urllib.parse.urlparse(img_url)
        img_url = urllib.parse.urlunparse(parsed_url._replace(query=''))
        img_data = requests.get(img_url).content
        with open(os.path.join(folder_path, os.path.basename(img_url)), 'wb') as handler:
            handler.write(img_data)