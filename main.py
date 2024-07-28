from typing import List
import handlers
import logging
import json
import os
from argparse import ArgumentParser

LINKS_FILE = "links.json"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def read_links_from_file(filename):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def write_links_to_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def parse_arguments():
    parser = ArgumentParser(description="Download series episodes")
    parser.add_argument("show_link", type=str, help="URL of the show")
    parser.add_argument(
        "--aria", action="store_true", help="Use aria2c for downloading"
    )
    parser.add_argument(
        "--bypass",
        action="store_true",
        help="Bypass the saved links file and rescrape all links manually",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Just fetches the file links, doesn't download anything",
    )
    return parser.parse_args()


def fetch_links(show_link, bypass):
    if os.path.isfile(LINKS_FILE) and not bypass:
        print(
            f"Found {LINKS_FILE} from a previous run. Skipping link scraping and moving directly to downloading"
        )
        return read_links_from_file(LINKS_FILE)
    else:
        season_links = handlers.extract_all_season_links_from_series(show_link)
        data = []
        for season in season_links:
            links = handlers.extract_all_downloadable_links_from_season_link(season)
            data.extend(links)
        write_links_to_file(LINKS_FILE, data)
        return data


def download_files(data: List[dict], use_aria):
    # check if to-be downloadded files exist in disk
    download_list = []
    for file in data:
        if not os.path.isfile(file["details"]["filename"]):
            download_list.append(file["url"])
        else:
            logging.info(
                f"Found {file['details']['filename']} in disk. Skipping download"
            )

    for link in download_list:
        if use_aria:
            handlers.download_with_aria2c(link)
        else:
            handlers.download_with_wget(link)


def main():
    args = parse_arguments()

    data = fetch_links(args.show_link, args.bypass)

    if not args.dry_run:
        download_files(data, args.aria)


if __name__ == "__main__":
    main()
