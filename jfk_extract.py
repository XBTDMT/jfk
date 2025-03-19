import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

# Configuration
base_url = 'https://www.archives.gov'
page_url = base_url + '/research/jfk/release-2025'
download_dir = 'JFK_Release_2025'
os.makedirs(download_dir, exist_ok=True)  # Create directory if it doesn’t exist
headers = {'User-Agent': 'PDF Downloader Script'}  # Identify the script to the server

# Step 1: Fetch the webpage
response = requests.get(page_url, headers=headers)
response.raise_for_status()  # Raise an error if the request fails
soup = BeautifulSoup(response.text, 'html.parser')

# Step 2: Extract all PDF links
pdf_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if href.endswith('.pdf'):  # Check if the link points to a PDF
        # Convert relative URLs to absolute URLs
        if href.startswith('/'):
            link = base_url + href
        else:
            link = href
        # Extract filename from the URL
        filename = os.path.basename(urlparse(link).path)
        pdf_links.append((link, filename))

# Remove duplicates, if any
pdf_links = list(set(pdf_links))
print(f"Found {len(pdf_links)} PDF links to download.")

# Step 3: Define the download function
def download_pdf(link, filename):
    try:
        filepath = os.path.join(download_dir, filename)
        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"Skipping {filename}, already exists")
            return
        # Download the PDF
        response = requests.get(link, headers=headers, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {link}: status code {response.status_code}")
    except Exception as e:
        print(f"Error downloading {link}: {e}")

# Step 4: Download PDFs concurrently with a thread pool
with ThreadPoolExecutor(max_workers=5) as executor:
    for link, filename in pdf_links:
        executor.submit(download_pdf, link, filename)

print("Download process completed.")
