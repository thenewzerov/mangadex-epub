# Mangadex to Epub


## Description
This project is written to allow you to download manga from mangadex.org and convert it to an epub file.

I haven't tested this very well.  Or, at all.  Outside of running it on a couple manga.
Results were okay, but use at your own risk.

## Setup

Make sure you have python 3.6 or higher installed.

Install the required packages with `pip install -r requirements.txt`

## Usage

Basic usage is this: 
```
python main.py --manga <manga_id> --directory <directory>
```

`manga_id` is the id of the manga you want to download. 
You can find this in the url of the manga. 


For example, the manga id of https://mangadex.org/title/a1c7c817-4e59-43b7-9365-09675a149a6f/one-piece 
is `a1c7c817-4e59-43b7-9365-09675a149a6f`.

`directory` is the directory where you want to save the manga images.

Yes, this is going to download ALL the images for the manga.  
I did some really crappy rate-limiting using `time.sleep()` so you don't get banned.
Expect to wait a while for the downloads to finish.
I'm using a library for pulling the images, but NOT using their content servers like I should.

Sorry mangadex.org.

This also assumes you're downloading English. If you want a different language, for now just change the code.
Look for anywhere I have the string `en`

The downloader WILL check for already downloaded files.  So if you have to stop mid-download and re-run it later,
at least there's that.

## Options

You're lucky.  I very quickly ran into a problem and needed to implement these.

If you want to specify which volumes to download, use the `-v` option.

If you want to specify which chapters to download, use the `-c` option.

For example, if I only wanted to download Volume 1, chapter 3, I would run:

```
python main.py --manga a1c7c817-4e59-43b7-9365-09675a149a6f --directory ./manga -v 1 -c 3
```

If I only wanted to download Volumes 1 and 2, chapters 3, 4, 25, 30 I would run:

```
python main.py --manga a1c7c817-4e59-43b7-9365-09675a149a6f --directory ./manga -v 1,2 -c 3,4,25,30
```

If you already have the images downloaded, and just want to create the epub file, use the `-s` option.


If you want to change which language you use, use the `-l` option.

A complete list of options is available with `python main.py --help`

```commandline
usage: main.py [-h] [-m MANGA] [-d DIRECTORY] [-s] [-i] [-v VOLUMES]
               [-c CHAPTERS] [-l LANGUAGE] [-r] [-p]

MangaDexPy

options:
  -h, --help                            show this help message and exit
  -m MANGA, --manga MANGA               Manga ID
  -d DIRECTORY, --directory DIRECTORY   Directory to store files
  -s, --skip                            Skip downloading the manga, only create the epub
  -i, --ignore                          Ignore the rate limits
  -v VOLUMES, --volumes VOLUMES         Comma separated list of volumes to download
  -c CHAPTERS, --chapters CHAPTERS      Comma separated list of chapters to download
  -l LANGUAGE, --language LANGUAGE      Language to download
  -r, --ltr                             Set the read direction to left to right
  -p, --points                          Skip any ".x" chapters
```


## Warning

This is a very quick and dirty script.  I'm not responsible for anything that happens to your computer.
The rate limiting is very crude.
I'm not responsible for you getting banned from mangadex.org for abusing their servers.

I'm not responsible for you running out of space on your computer.

## Directory Structure

When you pass a directory, it's going to create a directory structure like this:

```
<directory>
    <manga_name>
        <epub>
            Manga-Name Vol X.epub
        <Volume_1>
            cover.jpg
            <Chapter_1>
                000.jpg
                001.jpg
                ...
            <Chapter_2>
                000.jpg
                001.jpg
                ...
            ...
        <Volume_2>
            cover.jpg
            <Chapter_5>
                000.jpg
                001.jpg
                ...
            <Chapter_6>
                000.jpg
                001.jpg
                ...
            ...
        ...
        cover.jpg
```

Sometimes there might be problems pulling the covers.
Honestly, easiest solution is to just copy the one from the manga directory and paste it where needed.
I should probably do that in code, but I'm lazy.  Make a PR if you want to fix it.


## Loading onto a Kindle

So, Amazon kinda sucks with their proprietary formats.
To convert these `.epub` files to something you can sideload onto your Kindle, use Kindle Previewer.

https://kdp.amazon.com/en_US/help/topic/G202131170

Drag and drop the `.epub` file into it, then export it.

I've tried this with Calibre, and the images didn't transfer correctly.

Best luck I've had is converting it to a .mobi file.