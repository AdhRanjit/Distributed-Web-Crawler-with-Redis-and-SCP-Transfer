## Distributed-Web-Crawler-with-Redis-and-SCP-Transfer

This project implements a distributed web crawling system that interacts with multiple nodes (virtualized using Oracle VirtualBox) for crawling, storage, and file management. The system is designed to retrieve web pages, extract content, store it in Redis, and then transfer that data to a file system node for persistent storage.
The project was developed by Group 10: Large Scale Data Management (CS 4243-001), led by Ranjit Adhikari.

### Team Members
- Ranjit Adhikari (Team Lead)
- Cristopher Serrano
- Caleb Lee Pierce
- Annalisa Vuong

### Project Overview:

This distributed system consists of:
- Crawling Node: Retrieves web pages, extracts their content and links, and sends this information to the Redis node.
- Redis Node: Acts as the centralized data store for all crawled web pages.
- File System Node: Receives data from the crawling node and stores it in text files, which are later transferred via SCP to a remote server.

#### The system limits crawling to 10 links per page to conserve resources and maintain performance efficiency

### Components
- Crawling Node: Fetches and processes web pages.
- Redis Node: Stores web page titles and content.
- File System Node: Receives the crawled content and stores it as text files, transferring the files via SCP to a remote storage node.

### Distributed Nodes Setup
1. Each node (Crawling, Redis, File System) is deployed as a separate virtual machine using Oracle VirtualBox to simulate a distributed architecture.
2. The Crawling Node interacts with the Redis Node for storing retrieved content and the File System Node for transferring the stored files.

### Features
- Distributed Architecture: Simulates a multi-node web crawling system using Oracle VirtualBox.
- Web Crawling: Fetches the first 10 links from a given website.
- Content Storage: Stores the extracted titles and content in a Redis data store.
- File Management: Saves the web page content to text files and transfers them to a remote file system node via SCP.
- Resource Efficiency: Crawling is limited to 10 links per webpage to avoid resource exhaustion.

### Prerequisites
1. Software Requirements
2. Python 3.x
3. Redis Server (set up on a separate node)
4. Oracle VirtualBox for creating the distributed system
5. SCP Access to a remote server for transferring files

### Redis Setup
Ensure you have a Redis server running on a separate virtual machine. By default, the crawler connects to a Redis node at 192.168.1.78. Modify the IP in the script if your Redis node is running elsewhere.

### File System Node Setup
Set up SCP access to a remote node where the text files will be transferred. Update the script with the correct IP address, username, and destination path for SCP transfer.

### How It Works
- The user provides a URL for the crawler to start with.
- The crawler fetches the webpage, extracts the first 10 links, and sends the content to the Redis node.
- The titles and content are stored in Redis.
- The crawler then stores this content in local text files and transfers the files to a remote file system node using SCP.

### Program Flow
- Start: The user inputs a URL.
- Crawl: The system fetches the content of the web page and crawls up to 10 links.
- Store in Redis: The titles and content are stored in the Redis database.
- Store in Files: The content is saved as .txt files.
- Transfer Files: The saved files are transferred via SCP to a remote storage node.

  [Watch full Execution video here](https://www.youtube.com/watch?v=yYcdqZNV5Lk)
