import requests
from bs4 import BeautifulSoup
import redis
import os
import hashlib
import re
from urllib.parse import urljoin

# Connect to Redis
try:
    redis_client = redis.StrictRedis(host='192.168.1.78', port=6379, db=0)
except redis.ConnectionError:
    print("Error: Failed to connect to Redis.")
    exit()

def sanitize_title(title):
    # Remove special characters and spaces
    return re.sub(r'[^\w\s]', '', title).replace(' ', '_')

def crawl_and_store_links(url):
    # Send a GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.ok:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all anchor tags (links) on the page
        links = soup.find_all('a', href=True)
        
        # Limit the number of links to crawl to 10
        links_to_crawl = links[:10]
        
        # List to store crawled content
        crawled_content = []
        
        # Iterate through the links
        for link in links_to_crawl:
            # Get the href attribute of the link
            href = link.get('href')
            
            # Check if the link is valid (not None and not empty)
            if href and href.strip():
                # If the link is a relative URL, construct the absolute URL
                absolute_link = urljoin(url, href)
                
                # Call the crawl_and_store_wikipedia function for each link
                content = crawl_and_store_wikipedia(absolute_link)
                if content:
                    crawled_content.append(content)
        
        # Transfer all crawled content to the Storage Node - FS
        transfer_content_to_storage_node(crawled_content)
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

def crawl_and_store_wikipedia(url):
    # Send a GET request to the Wikipedia page
    response = requests.get(url)

    # Check if the request was successful
    if response.ok:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the title of the page
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text()
        else:
            title = "Title_not_available"

        # Find all paragraphs in the page content and join them into a single string
        paragraphs = soup.find_all('p')
        if paragraphs:
            content = '\n'.join(paragraph.get_text() for paragraph in paragraphs)
        else:
            content = "Content_not_available"

        # Store title and content in Redis
        title_key = f"{url}_title"
        content_key = f"{url}_content"
        redis_client.set(title_key, title)
        redis_client.set(content_key, content)

        # Sanitize the title for file naming
        sanitized_title = sanitize_title(title)

        # Save title and content to a text file with sanitized title
        filename = f"{sanitized_title}.txt"
        with open(filename, 'w') as file:
            file.write(f"Title: {title}\n")
            file.write(f"Content: {content}\n")

        # Return the filename and content
        return {
            'filename': filename,
            'content': content
        }
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)
        return None

def transfer_content_to_storage_node(crawled_content):
    # Create a directory to store crawled files
    os.makedirs("crawled_files", exist_ok=True)

    # Transfer all crawled content to the local directory
    for content in crawled_content:
        filename = content['filename']
        content_text = content['content']
        with open(f"crawled_files/{filename}", 'w') as file:
            file.write(content_text)

    # Transfer the entire directory to the Storage Node - FS using SCP
    os.system("scp -r crawled_files/* vmadmin@192.168.1.198:/home/vmadmin")
    print("Files transferred to Storage Node - FS.")

# Ask the user for the website URL
website_url = input("Enter the URL of the website you want to crawl: ")

# Call the crawl_and_store_links function with the provided URL
crawl_and_store_links(website_url)
