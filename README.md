# Spiider

## About
Spiider is a python script for generating websites (Spiider makes webs). It takes a markdown file and converts it to html using a template and metadata from either the markdown itself or an external json file. It also copies over any other files, meaning you can add plain HTML or assets. It then uses templates for an index page and templates for previews to generate an index page. It does the same thing as the index page for feeds (atom or RSS), just using different templates.

## Quickstart
First of all, you'll need to clone the repository. Run 
```bash
git clone https://github.com/rathippo/spiider {your website name here}
```
To use the script, you're going to need to install some packages. To make sure you have everything you need, just use
```bash
pip3 install json markdown markdown-full-yaml-metadata
```
Now that you have all the necessary things installed, navigate into the directory where you cloned the repo and remove the sample article. 
```bash
python3 spiider.py remove folder sample
```
Now, you don't want to stick with the default config. Open up config.py using your favorite text editor. Before you edit, it should look like this:
```python
from spiider import Folder
folder = Folder()
folder.srcdir = "src/articles/"
folder.indexdir = "build/"
folder.builddir = "build/articles/"
folder.articletemplate = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
    ...
 </html>
"""
folder.indextemplate = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
  ...
</html>
"""
folder.previewtemplate = """
<div>
   ...
</div>
"""
folder.dofeed = True
folder.feedtemplate = """<rss version="2.0">
  ...
</rss>"""
folder.feeditemtemplate = """
<item>
    ...
</item>
"""
folders = {"folder":folder}
```
This config file defines a basic folder. What spiider does is takes the folders defined in the dictionary named 'folders' and converts them into index pages, articles, and feeds. Although this config only defines one, it is entirely possible to use more. Anyway, you probably don't want to keep refering to your folder as 
'folder' (This is what you did when you removed the sample article). For this example, we'll use the name blog. Anyway, all you need to do to change the name is edit the dictionary at the bottom of the file to be:
```python
folders = {"blog":folder}
```
, but for the sake of consistency and readability, you might as well update the entire file to use a variable called 'blog' instead of 'folder'. 
```python
from spiider import Folder
blog = Folder()
blog.srcdir = "src/articles/"
blog.indexdir = "build/"
blog.builddir = "build/articles/"
blog.articletemplate = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
    ...
 </html>
"""
blog.indextemplate = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
  ...
</html>
"""
blog.previewtemplate = """
<div>
   ...
</div>
"""
blog.dofeed = True
blog.feedtemplate = """<rss version="2.0">
  ...
</rss>"""
blog.feeditemtemplate = """
<item>
    ...
</item>
"""
folders = {"folder":blog}
```
For more advanced configuration, such as changing the source and build directories or the templates, you can check out the [configuration section](##configuration"), but we'll leave it here for now.

Now that you've modified the configuration file to your liking, you can begin writing an article. Simply run
```bash
python3 spiider.py new blog myfirstarticle
```
or something similar to create your article. Assuming you haven't already changed the source directories, you should find your article at src/articles/myfirstarticle/. In that directory there will be a file named 'article.md'. You should go to the [writing section](###writing) for more detail, but after changing the default metadata, your article should look something like this:
```
---
title: My First Article
description: This is my first article I wrote with spiider!
date: 22-08-01
path: myfirstarticle
testing: false
---
```
add some markdown underneath the metadata, and you've got yourself an article, which'll probably look something like this:
```
---
title: My First Article
description: This is my first article I wrote using spiider!
date: 22-08-01
path: myfirstarticle
testing: false
---
## Why I Made my first article
a 'quick' start guide forced me to
```
Now finally comes the time to build your website. 
```bash
python3 spiider.py build
```
Assuming you did everything correctly, there should be no errors. As long as you haven't changed the directories in the config yet, your build and source directories should look like this:
```
websitename
|
|  build
| | articles
| | | myfirstarticle
| | | | index.html
| | | |
| | index.html
| | feed.xml
|
| src
| | articles
| | | myfirstarticle
| | | | article.md
| | | |
| | | | 
```
To test out your website, go into the build directory and run:
```bash
python3 -m http.server
```
go to [http://localhost:8000](http://localhost:8000) in your browser, and if all went well, your website should look pretty basic, but once you configure your templates and add in some CSS, your website will be looking great.
  


## Configuration
The sample configuration file "config.py" defines a sample config. You can get this config in any way you want, all that matters is that you have a dictionary of subconfigs named "folders" with the keys being the names of the folders you want to use in the CLI and the value being the folders themselves. Each subconfig is a "Folder" object which uses the following properties:

|   Property  |   Details   |
|-------------|-------------|
| srcdir | The directory with the source articles |
| indexdir | The directory in which to place the index page |
| builddir | The directory in which to place the built articles |
| articletemplate | The template HTML for an article Use {title} and {text} to place the title and text |
| indextemplate | The template HTML for the index page. Use {items} to place the article previews |
| previewtemplate | The template HTML for the article previews seen on the index page. Use {path} for the path of the article. then you get the link to the article). You can use {title}, {path} {description}, {date}, and {fulldate} for the title, path, description, date in your own format, and date in 'Mon, 01 Jan 2000' format.|
| dofeed | Whether or not to generate a feed (RSS, atom, etc.). True or False |
| feedtemplate | Feed template, use {items} to put in the feed items|
| feeditemtemplate | Template for feed items. You can use {title}, {path} {description}, {date}, and {fulldate} for the title, path, description, date in your own format, and date in 'Mon, 01 Jan 2000' format. (use this for pubDate) |

The main config also has one property: the datetimeformat property. This is just a format string, see [strftime.org](https://strftime.org)
## Writing
To write an article, navigate to the directory which has spiider.py in it. Then run `python3 spiider.py new {foldername} {articlename}`. A directory with the article name you put should be located in your source directory. There should be a file in this folder called 'article.md' The file should contain metadata that looks like this:
```
---
title:{insert title}
description: {insert description}
date: "{insert date}" (remember to put quotes around it to garuntee it is interpreted as a string, rather than a datetime.date)
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