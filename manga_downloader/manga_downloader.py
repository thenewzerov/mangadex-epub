import os
import time

import mangadex

from utils.utils import create_directory, print_progress_bar, download_file


class MangaDownloader:

    def __init__(self):
        self.api = mangadex.Api()

    def fetch_manga(self, manga_id: str, directory: str, ignore_limits=False, skip_download=False,
                    volumes_list=None, chapters_list=None, language='en', skip_halfs=False):
        errors = []

        # Get manga
        manga = self.api.view_manga_by_id(manga_id=manga_id)
        if not manga:
            errors.append('Manga not found')
            return '', errors

        # Create directory for manga

        # Get the title (whatever the first available one is)
        title = next(iter(manga.title.values()))

        for alt_title_dict in manga.altTitles:
            if language in alt_title_dict:
                title = alt_title_dict[language]
        safe_title = ''.join(letter for letter in title if letter.isalnum())
        manga_directory = os.path.join(directory, safe_title)

        create_directory(manga_directory)

        print('Manga Title: ' + title)

        # Get the Manga Cover
        cover_art = self.api.get_cover(coverId=manga.coverId)
        url = 'https://uploads.mangadex.org/covers/' + manga.manga_id + '/' + cover_art.fileName

        cover_ext = cover_art.fileName.split('.')[1]
        cover_path = os.path.join(manga_directory, 'cover.' + cover_ext)
        success = download_file(cover_path, url)

        if not success:
            errors.append(cover_path)

        # Get the covers for the volumes:
        covers = self.api.get_coverart_list(manga=manga.manga_id)

        # Get Volume and Chapter IDs
        volumes = self.api.get_manga_volumes_and_chapters(manga_id=manga_id)

        if skip_download:
            return {'manga': manga, 'volumes': volumes, 'directory': manga_directory}, errors

        for key, volume_dict in volumes.items():
            if volumes_list is not None and volume_dict['volume'] not in volumes_list:
                continue

            print('  Volume: ' + volume_dict['volume'])

            # Create directory for volume
            volume_number = volume_dict['volume']
            volume_directory = os.path.join(manga_directory, 'Volume_' + volume_number)

            create_directory(volume_directory)

            # Get the volume cover
            for cover in covers:
                if cover.volume == volume_dict['volume']:
                    url = 'https://uploads.mangadex.org/covers/' + manga.manga_id + '/' + cover.fileName
                    cover_ext = cover.fileName.split('.')[1]
                    cover_path = os.path.join(volume_directory, 'cover.' + cover_ext)
                    success = download_file(cover_path, url)

                    if not success:
                        errors.append(cover_path)

            for key, chapter_dict in volume_dict['chapters'].items():

                # If a chapter list was sent it, go through those only
                if chapters_list is not None and chapter_dict['chapter'] not in chapters_list:
                    continue

                # Skip .5 chapters
                if skip_halfs and '.' in chapter_dict['chapter']:
                    continue

                print('    Chapter: ' + chapter_dict['chapter'])
                # Create directory for chapter
                chapter_number = chapter_dict['chapter']
                chapter_directory = os.path.join(volume_directory, 'Chapter_' + chapter_number)

                create_directory(chapter_directory)

                # Get pages
                chapter = self.api.get_chapter(chapter_id=chapter_dict['id'])
                time.sleep(1)

                pages = chapter.fetch_chapter_images()

                if chapter.translatedLanguage != language or len(pages) == 0:
                    for chapter_id in chapter_dict['others']:
                        chapter = self.api.get_chapter(chapter_id=chapter_id)
                        pages = chapter.fetch_chapter_images()
                        time.sleep(1)
                        if chapter.translatedLanguage == language and len(pages) > 0:
                            break

                if chapter.translatedLanguage != language:
                    errors.append('  Chapter: ' + chapter_number + ' - Not available in ' + language)
                    continue
                elif len(pages) == 0:
                    errors.append('  Chapter: ' + chapter_number + ' - No pages found')
                    continue
                else:
                    download_needed = False
                    for index, page in enumerate(pages):
                        # Print progress
                        print_progress_bar(index + 1, len(pages), prefix='      Progress:', suffix='Complete',
                                           length=50)

                        # Download page if it doesn't exist
                        page_filename = os.path.join(chapter_directory, f'{index:03d}.jpg')

                        if not os.path.exists(page_filename):
                            # Be nice to the MangaDex servers.  But only sleep if we don't already have the page.
                            if not ignore_limits:
                                time.sleep(1)
                            download_needed = True

                            success = download_file(page_filename, page)
                            if not success:
                                print(
                                    'Volume: ' + volume_number + ' Chapter: ' + chapter_number + ' Page: ' + str(index))
                                errors.append('Page ' + str(page))

                    if download_needed:
                        # Sleep for 10 seconds because I want to be nice to the MangaDex servers
                        if not ignore_limits:
                            time.sleep(10)

        return {'manga': manga, 'volumes': volumes, 'directory': manga_directory}, errors
