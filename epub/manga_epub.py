import numbers
import os

from ebooklib import epub
from ebooklib.utils import create_pagebreak

from utils.utils import create_directory


class MangaEpubCreator:

    def __init__(self, manga, output_path):
        self.manga = manga
        self.output_path = os.path.join(output_path, 'epub')

        create_directory(self.output_path)

    def create_volume(self, volume_name, volume_directory, manga_directory, language='en',
                      left_to_right=False, skip_halfs=False):

        print('Creating epub for volume: ' + volume_name)

        # Get the Title
        title = self.manga.title['en']

        for alt_title_dict in self.manga.altTitles:
            if 'en' in alt_title_dict:
                title = alt_title_dict['en']

        book_path = os.path.join(self.output_path, title + ' Vol ' + volume_name + '.epub')

        # If the epub already exists, skip it
        if os.path.isfile(book_path):
            print('Epub already exists, skipping...')
            return

        book = epub.EpubBook()

        # set metadata
        book.set_identifier(self.manga.manga_id + '_' + volume_name)

        book.add_author(self.manga.authorId[0])

        # Set the title
        book.set_title(title + ' Vol ' + volume_name)
        book.set_language(language)

        # Set the direction
        if not left_to_right:
            book.set_direction("rtl")

        # Add the cover.  If it doesn't exist, use the manga cover
        if os.path.isfile(os.path.join(volume_directory, 'cover.jpg')):
            book.set_cover("cover.jpg", open(os.path.join(volume_directory, 'cover.jpg'), "rb").read())
        else:
            book.set_cover("cover.jpg", open(os.path.join(manga_directory, 'cover.jpg'), "rb").read())

        page_count = 0
        chapter_count = 0
        chapters = []

        # Chapters are stored in directories named Chapter_1, Chapter_2, etc.
        # Because of this, we need to sort the directories by their number before we add them.
        # Otherwise, they'll be added out of order.
        volume_directory_contents = os.listdir(volume_directory)
        chapters_to_sort = []
        for chapter_dir in volume_directory_contents:
            chapter_directory = os.path.join(volume_directory, chapter_dir)
            if os.path.isdir(chapter_directory):
                chapter_number = chapter_dir.replace('Chapter_', '')
                chapters_to_sort.append((chapter_number, chapter_dir))

        chapters_to_sort.sort(key=lambda x: float(x[0]))

        # For every chapter in the volume directory, add it to the epub
        for chapter_dir in chapters_to_sort:
            chapter_directory = os.path.join(volume_directory, chapter_dir[1])

            # Skip half chapters
            if skip_halfs and '.' in chapter_dir[1]:
                continue

            if os.path.isdir(chapter_directory):
                chapter, chapter_name, pages_added = self.add_chapter(book, chapter_directory, chapter_count,
                                                                      page_count, language)
                chapters.append(chapter)
                page_count += pages_added
                chapter_count += 1

                # If the page count is 0, skip the chapter
                # Otherwise, you'll have errors writing the file out.
                if pages_added == 0:
                    print('Skipping chapter ' + chapter_name + ' because it has no pages')
                    continue
                else:
                    book.toc.append(chapter)

        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # define CSS style
        style = ('BODY {color: white;} img {display: block; margin: 0 auto;  max-width: 90%; height: auto;} '
                 '.chapter { text-align: left }  .page-number { text-align: right }')
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style,
        )

        # add CSS file
        book.add_item(nav_css)

        # create spine
        spine = ['cover', 'nav'] + chapters
        book.spine = spine

        # write to the file
        epub.write_epub(book_path + '', book, {})

    def add_chapter(self, book, chapter_directory, current_chapter_num, current_page_num, language='en'):
        # Get the chapter name
        chapter_name = os.path.basename(chapter_directory).replace('Chapter_', '')

        page_count = 0

        # chapter with image
        chapter = epub.EpubHtml(title='Chapter ' + chapter_name, file_name='Chapter_' + chapter_name + '.xhtml', lang=language)
        chapter.content = u'''<html><head></head><body>'''

        # Add every page in the chapter to the epub
        for page in os.listdir(chapter_directory):
            page_path = os.path.join(chapter_directory, page)

            if os.path.isfile(page_path):
                page_count += 1

                image_content = open(page_path, "rb").read()
                image_id = os.path.basename(chapter_directory) + '_' + os.path.basename(page_path)
                img = epub.EpubImage(
                    uid=image_id,
                    file_name=image_id,
                    media_type="image/jpg",
                    content=image_content,
                )

                # Add the image to the page
                chapter.content += u'''<img src="''' + image_id + u'''"/>'''

                # Add a page break
                chapter.content += create_pagebreak(current_page_num + page_count)

                # add image to epub
                book.add_item(img)

        chapter.content += u'''</body></html>'''

        # add chapter
        book.add_item(chapter)

        return chapter, chapter_name, page_count


