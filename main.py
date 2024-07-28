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

def main():
    parser = ArgumentParser(description="Download series episodes")
    parser.add_argument('show_link', type=str, help="URL of the show")
    parser.add_argument('--aria', action='store_true', help="Use aria2c for downloading")
    parser.add_argument('--bypass', action='store_true', help="Bypass the saved links file and rescrape all links manually")
    parser.add_argument('--dry-run', action='store_true', help="Just fetches the file links, doesn't download anything")
    args = parser.parse_args()

    show_link = args.show_link
    file_links = []

    if os.path.isfile(LINKS_FILE) and not args.bypass:
        print("Found link files from a previous run. Skipping link scraping and moving directly to downloading")
        file_links = read_links_from_file(LINKS_FILE)
    else:
        season_links = handlers.extract_all_season_links_from_series(show_link)
        for season in season_links:
            links = handlers.extract_all_downloadable_links_from_season_link(season)
            file_links.extend(links)
        write_links_to_file(LINKS_FILE, file_links)

    if args.dry_run:
        return

    if args.aria:
        handlers.download_file_with_aria2c(LINKS_FILE)
    else:
        for file in file_links:
            handlers.download_with_wget(file)

if __name__ == "__main__":
    main()
