from spiider import Folder

datetimeformat = "%Y-%m-%d"
fulldateformat = "%a, %d %b %Y"
folder = Folder()
folder.srcdir = "src/articles/"
folder.indexdir = "build/"
folder.builddir = "build/articles/"
folder.articletemplate = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        {article}
    </body>
 </html>
"""
folder.indextemplate = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    {items}
  </body>
</html>
"""
folder.previewtemplate = """
<div>
    <a href = /articles/{path}><h3>{title}</h3></a>
    <p>{description}</p>
    <h5>{date}</h5>
    <div>{tags}<div>
</div>
"""
folder.dofeed = True
folder.feedtemplate = """<rss version="2.0">
  <channel>
    <title>Sample Title</title>
    <link>https://example.com</link>
    <description>This is a sample RSS feed</description>
    {items}
  </channel>
</rss>"""
folder.feeditemtemplate = """
<item>
    <title>{title}</title>
    <link>build/articles/{path}</link>
    <description>{description}</description>
    <pubDate>{fulldate}</pubDate>
</item>
"""
folder.dotags = True
folder.tagdir = "build/tags/"
folder.tagtemplate = "<a href = '/tags/{name}' class = 'tag tag_{name}'>{name}</a>"
folders = {"folder":folder}