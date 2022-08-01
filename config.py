from spiider import Folder
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
    <a href = articles/{path}><h3>{title}</h3></a>
    <p>{description}</p>
    <h5>{date}</h5>
</div>
"""
folder.dorss = True
folder.rsstemplate = """<rss version="2.0">
  <channel>
    <title>Sample Title</title>
    <link>https://example.com</link>
    <description>This is a sample RSS feed</description>
    {items}
  </channel>
</rss>"""
folder.rssitemtemplate = """
<item>
    <title>{title}</title>
    <link>build/articles/{path}</link>
    <description>{description}</description>
</item>
"""
folders = {"folder":folder}