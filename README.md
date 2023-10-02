# Mangadex to Epub

## Description
This project is written to allow you to download manga from mangadex.org and convert it to an epub file.

I haven't tested this very well.  Or, at all.  Outside of running it on a couple manga.
Results were okay, but use at your own risk.

## Setup

Make sure you have python 3.6 or higher installed.

Install the required packages with `pip install -r requirements.txt`

## Usage

Run the script with `python main.py --manga <manga_id> --directory <directory>`

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

## Options for Downloading

lol, no.


But seriously, there's nothing.  No selecting specific chapters or volumes.
It's going to download everything.  Make sure you have space.  
Don't try on something like One Piece.

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