import os

from ebooklib import epub
from ebooklib.utils import create_pagebreak

from utils.utils import create_directory


class MangaEpubCreator:

    def __init__(self, manga, output_path):
        self.manga = manga
        self.output_path = os.path.join(output_path, 'epub')

        create_directory(self.output_path)

    def create_volume(self, volume_name, volume_directory):
        print('Creating epub for volume: ' + volume_name)
        book = epub.EpubBook()

        # set metadata
        book.set_identifier(self.manga.manga_id + '_' + volume_name)

        # Get the Title
        title = self.manga.title['en']

        for alt_title_dict in self.manga.altTitles:
            if 'en' in alt_title_dict:
                title = alt_title_dict['en']

        book.set_title(title + ' Vol ' + volume_name)
        book.set_language("en")

        book.add_author(self.manga.authorId[0])

        # Add the cover
        book.set_cover("cover.jpg", open(os.path.join(volume_directory, 'cover.jpg'), "rb").read())

        page_count = 0
        chapter_count = 0
        chapters = []

        # For every chapter in the volume directory, add it to the epub
        for chapter_dir in os.listdir(volume_directory):
            chapter_directory = os.path.join(volume_directory, chapter_dir)
            if os.path.isdir(chapter_directory):
                chapter, chapter_name, pages_added = self.add_chapter(book, chapter_directory, chapter_count, page_count)
                chapters.append(chapter)
                page_count += pages_added
                chapter_count += 1

                book.toc.append(chapter)

        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # define CSS style
        style = "BODY {color: white;}"
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

        # create book path
        book_path = os.path.join(self.output_path, title + ' Vol ' + volume_name + '.epub')

        # write to the file
        epub.write_epub(book_path + '', book, {})

    def add_chapter(self, book, chapter_directory, current_chapter_num, current_page_num):
        # Get the chapter name
        chapter_name = os.path.basename(chapter_directory).replace('Chapter_', '')

        page_count = 0

        # chapter with image
        chapter = epub.EpubHtml(title='Chapter ' + chapter_name, file_name='Chapter_' + chapter_name + '.xhtml', lang='en')
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

                chapter.content += u'''<img src="''' + image_id + u'''"/>'''
                chapter.content += create_pagebreak(current_page_num + page_count)

                # add image to epub
                book.add_item(img)

        chapter.content += u'''</body></html>'''

        # add chapter
        book.add_item(chapter)

        return chapter, chapter_name, page_count


