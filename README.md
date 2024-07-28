# Movie Downloader Script

This script is designed to scrape and download series episodes from a specified movie site. It supports downloading using either `wget` or `aria2c`.

## Features

- Scrape all season links from a given series URL.
- Extract all downloadable file links from each season.
- Download files using `wget` or `aria2c`.
- Bypass previously saved links for rescraping if needed.

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`

To install the required Python packages, run:
```sh
pip install requests beautifulsoup4
```

Usage
1. Clone this repository.
2. Ensure you have wget or aria2c installed on your system.
3. Run the script with the following command:

```sh
python downloader.py <show_link> [--aria] [--bypass]
```
- <show_link>: URL of the series.
- --aria: Use aria2c for downloading (optional).
- --bypass: Bypass the saved links file and rescrape all links manually (optional).

Example
To download episodes using aria2c:

```sh
python downloader.py https://example.com/show_link --aria
```

To download episodes using wget and rescrape all links:

```sh
python downloader.py https://example.com/show_link --bypass
```

## Disclaimer
This script is intended purely for educational purposes. The author is not responsible for any misuse of this script, including but not limited to piracy or any other illegal activities. Please ensure that you have the legal right to download the content before using this script.

