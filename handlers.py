import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import subprocess

BASE_URL = "https://vadapav.mov"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_all_season_links_from_series(series_link: str):
    """
    Extracts all season links from the given series link.
    
    :param series_link: URL of the series
    :return: List of season URLs
    :raises: requests.HTTPError if the request fails
    """
    response = requests.get(series_link)
    logging.info(f"Extracting season links for: {series_link}")
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    season_links = soup.find_all('a', class_='directory-entry')
    logging.info(f"Found {len(season_links)} season links")
    return [urljoin(BASE_URL, link.get('href')) for link in season_links]

def extract_all_downloadable_links_from_season_link(season_link: str):
    """
    Extracts all downloadable file links from the given season link.
    
    :param season_link: URL of the season
    :return: List of file URLs
    :raises: requests.HTTPError if the request fails
    """
    response = requests.get(season_link)
    logging.info(f"Extracting download links for: {season_link}")
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    file_links = soup.find_all('a', class_='file-entry')
    logging.info(f"Found {len(file_links)} file links")
    return [urljoin(BASE_URL, link.get('href')) for link in file_links]

def download_with_wget(link):
    """
    Downloads a file using wget.
    
    :param link: URL of the file to download
    """
    logging.info(f"Downloading with wget: {link}")
    subprocess.run(['wget', '--content-disposition', '--trust-server-names', link])

def download_with_aria2c(link):
    """
    Downloads a file using aria2c.
    
    :param link: URL of the file to download
    """
    logging.info(f"Downloading with aria2c: {link}")
    subprocess.run(['aria2c', '-x4', link, '--file-allocation=none', '-c', '--auto-file-renaming=false'])
