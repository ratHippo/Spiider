# Spiider

## About
Spiider is a python script for generating websites (Spiider makes webs). It takes a markdown file and converts it to html using a template and metadata from either the markdown itself or an external json file. It also copies over any other files, meaning you can add plain HTML or assets. It then uses templates for an index page and templates for previews to generate an index page. It does the same thing as the index page for rss using different templates.

## Configuration
The sample configuration file "config.py" defines a sample config. You can get this config in any way you want, all that matters is that you have a dictionary of subconfigs named "folders" with the keys being the names of the folders you want to use in the CLI and the value being the folders themselves. Each subconfig is a "Folder" object which uses the following properties:

|   Property  |   Details   |
|-------------|-------------|
| srcdir | The directory with the source articles |
| indexdir | The directory in which to place the index page |
| builddir | The directory in which to place the built articles |
| articletemplate | The template HTML for an article Use {title} and {text} to place the title and text |
| indextemplate | The template HTML for the index page. Use {items} to place the article previews |
| previewtemplate | The template HTML for the article previews seen on the index page. Use {path} for the path of the article. then you get the link to the article). You can use {title}, {description}, and {date} for the title, description, and date.|
| dorss | Whether or not to generate an RSS feed. True or False |
| rsstemplate | RSS template, use {items to put in the rss items}|
| rssitemtemplate | use {title}, {path}, and {description} to get the title, path and description |

## Writing
To write an article, navigate to the directory which has spiider.py in it. Then run `python3 spiider.py new {foldername} {articlename}`. A directory with the article name you put should be located in your source directory. There should be a file in this folder called 'article.md' The file should contain metadata that looks like this:
```
---
title:{insert title}
description: {insert description}
date: {insert date}
path: {insert path}
testing: {insert testing (bool)}
---
```
See the table below for what each point of data means
| Property | Details |
|-|-|
| title | The title of the article |
| description | A short description of the article |
| date | The date the article was written |
| path | The name of the folder that you created for the article
| testing | True or false: if false the article will be ignored by the builder|

Edit this metadata in your article to change how it will be displayed.
To add text to your article, simply write markdown in the resto of the file

## Building

To build everything, run:

`python3 spiider.py build`

To build a single folder run:

`python3 spiider.py build foldername`

To build a single article run:

`python3 spiider.py build foldername articlename`
(keep in mind that this won't update the index page)
## Dependencies

`
pip3 install json markdown markdown-full-yaml-metadata
`