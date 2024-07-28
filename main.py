import handlers
import sys
import logging
import os
from argparse import ArgumentParser

LINKS_FILE = "all_links.txt"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_links_from_file(filename):
    logging.info(f"Reading links from {filename}")
    with open(filename, 'r') as file:
        return file.read().splitlines()

def write_links_to_file(filename, links):
    logging.info(f'Writing {len(links)} links to {filename}')
    with open(filename, 'w') as file:
        file.write('\n'.join(links))

def parse_arguments():
    parser = ArgumentParser(description="Download series episodes")
    parser.add_argument('show_link', type=str, help="URL of the show")
    parser.add_argument('--aria', action='store_true', help="Use aria2c for downloading")
    parser.add_argument('--bypass', action='store_true', help="Bypass the saved links file and rescrape all links manually")
    parser.add_argument('--dry-run', action='store_true', help="Just fetches the file links, doesn't download anything")
    return parser.parse_args()

def fetch_links(show_link, bypass):
    if os.path.isfile(LINKS_FILE) and not bypass:
        print("Found link files from a previous run. Skipping link scraping and moving directly to downloading")
        return read_links_from_file(LINKS_FILE)
    else:
        season_links = handlers.extract_all_season_links_from_series(show_link)
        file_links = []
        for season in season_links:
            links = handlers.extract_all_downloadable_links_from_season_link(season)
            file_links.extend(links)
        write_links_to_file(LINKS_FILE, file_links)
        return file_links

def download_files(file_links, use_aria):
    if use_aria:
        handlers.download_file_with_aria2c(LINKS_FILE)
    else:
        for file in file_links:
            handlers.download_with_wget(file)

def main():
    args = parse_arguments()

    file_links = fetch_links(args.show_link, args.bypass)

    if not args.dry_run:
        download_files(file_links, args.aria)

if __name__ == "__main__":
    main()
