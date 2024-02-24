import os

from epub.manga_epub import MangaEpubCreator
from manga_downloader.manga_downloader import MangaDownloader
from utils.utils import create_directory, get_args

if __name__ == '__main__':
    args = get_args()

    # Create root directory if it doesn't exist
    create_directory(args.directory)

    # Create API object
    downloader = MangaDownloader()

    manga_id = args.manga

    # If volumes is specified, split into list and pass to downloader
    volumes_list = None
    if args.volumes:
        volumes_list = args.volumes.split(',')

    # If chapters is specified, split into list and pass to downloader
    chapters_list = None
    if args.chapters:
        chapters_list = args.chapters.split(',')

    la = args.language

    # Get the pages
    details, errors = downloader.fetch_manga(manga_id, args.directory, ignore_limits=args.ignore,
                                             skip_download=args.skip, volumes_list=volumes_list,
                                             chapters_list=chapters_list, skip_halfs=args.points, language=la)

    # Print errors
    if len(errors) > 0:
        print('Errors:')
        for error in errors:
            print(error)
        exit()

    # Create the Epub Generator
    manga = details['manga']

    title = next(iter(manga.title.values()))

    for alt_title_dict in manga.altTitles:
        if 'en' in alt_title_dict:
            title = alt_title_dict['en']
    safe_title = ''.join(letter for letter in title if letter.isalnum())
    manga_directory = os.path.join(args.directory, safe_title)

    epub_generator = MangaEpubCreator(details['manga'], manga_directory)

    volumes = details['volumes']

    # For every volume in volumes, create an epub
    for key, volume_dict in volumes.items():
        # Create directory for volume
        volume_number = volume_dict['volume']
        volume_directory = os.path.join(manga_directory, 'Volume_' + volume_number)

        # Skip if the volume directory isn't in the volumes list
        if volumes_list is not None and volume_number not in volumes_list:
            continue

        # Create epub
        epub_generator.create_volume(volume_name=volume_dict['volume'], volume_directory=volume_directory,
                                     manga_directory=manga_directory, language=la, left_to_right=args.ltr,
                                     skip_halfs=args.points)

