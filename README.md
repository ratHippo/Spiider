# website-generator

## About:
Right now this python script is set up to generate my website. It takes a markdown file and converts it to html using a template and metadata from either the markdown itself or an external json file. It also copies over any other files, meaning you can add plain HTML or assets. It then uses templates for an index page and templates for previews to generate an index page. It does the same thing as the index page for rss using different templates.

## Configuration
The sample configuration file "config.py" imports from blog.py and games.py, which act as subconfigs, but the only important thing is that your config contains a variable called "folders" and that that variable is a list of the configs
## Dependencies

```bash
pip install json markdown markdown-full-yaml-metadata
```