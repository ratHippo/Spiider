# website-generator

## About:
Right now this python script is set up to generate my website. It takes a markdown file and converts it to html using a template and metadata from either the markdown itself or an external json file. It also copies over any other files, meaning you can add plain HTML or assets. It then uses templates for an index page and templates for previews to generate an index page. It does the same thing as the index page for rss using different templates.

## Configuration
The sample configuration file "config.py" defines a sample config. You can get this config in any way you want, all that matters is that you have a list of subconfigs named "folders".

|   Property  |   Details   |
|-------------|-------------|
| srcdir | The directory with the source articles |
| indexdir | The directory in which to place the index page |
| indexlinkdir | the link from the indexdir to the builddir |
| builddir | The directory in which to place the built articles |
| articletemplate | The template HTML for an article Use {title} and {text} to place the title and text |
| indextemplate | The template HTML for the index page. Use {previews} to place the article previews |
| previewtemplate | The template HTML for the article previews seen on the index page. Use {indexlinkdir} for the indexlinkdir (see above). Use {path} for the path of the article (if you use {indexlinkdir}+{path} then you get the link to the article). You can use {title}, {description}, and {date} for the title, description, and date.|
| dorss | Whether or not to generate an RSS feed. True or False |
| rsstemplate | RSS template, use {items to put in the rss items}|
| rssitemtemplate | use {title}, {path}, and {description} to get the title, path and description |

## Dependencies

```bash
pip install json markdown markdown-full-yaml-metadata
```
