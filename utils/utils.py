import argparse
import os

import requests


# Print iterations progress
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def create_directory(directory):
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_args():
    # Read command line arguments
    parser = argparse.ArgumentParser(description='MangaDexPy')

    # Read manga id
    parser.add_argument('-m', '--manga', type=str, help='Manga ID')

    # Read directory to store files
    parser.add_argument('-d', '--directory', type=str, help='Directory to store files')

    # Skip Download
    parser.add_argument('-s', '--skip', action='store_true', help='Skip downloading the manga, only create the epub')

    # Ignore Limits
    parser.add_argument('-i', '--ignore-limits', action='store_true', help='Ignore the rate limits')

    # Volumes
    parser.add_argument('-v', '--volumes', type=str, help='Comma separated list of volumes to download')

    # Chapters
    parser.add_argument('-c', '--chapters', type=str, help='Comma separated list of chapters to download')

    # Languages
    parser.add_argument('-l', '--language', type=str, help='Language to download', default='en')

    # Parse arguments
    args = parser.parse_args()

    if not args.manga:
        print('Manga ID is required')
        exit()

    if not args.directory:
        print('Directory is required')
        exit()

    print('Manga ID: ' + args.manga)
    print('Directory: ' + args.directory)

    return args


def download_file(path, url):
    if not os.path.exists(path):
        try:
            data = requests.get(url).content

            with open(path, 'wb') as handler:
                handler.write(data)
                handler.close()
        except Exception as e:
            print('Error: ' + str(e))
            return False
    return True
