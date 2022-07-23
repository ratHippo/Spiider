blog = {}
blog["srcdir"] = "src/articles/"
blog["indexdir"] = "blog/"
blog["indexlinkdir"] = "articles/"
blog["builddir"] = "blog/articles/"
blog["articletemplate"] = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <link rel="stylesheet" href="../../../index.css">
    </head>
    <body class="font1">
        <div class="main-content">
            <div class="grid">
                <h1>{title}</h1>
                <card>
                    {article}
                </card>
                <h3><a href="../../">Back</a></h3>
                </div>
            </div>
    </body>
 </html>
"""
blog["indextemplate"] = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="../index.css">
    <title></title>
  </head>
  <body class = "font1">
    <div class = "main-content">
      <div class="grid">
        <h1>Blog</h1>
        {previews}
        <h3><a href = "/">back</a></h3>
    </div>
    </div>
  </body>
</html>
"""
blog["previewtemplate"] = """
<a class ="nocolor" href = {indexlinkdir}{path}>
    <card>
        <h3>{title}</h3>
        <p>{description}</p>
        <h5>{date}</h5>
      </card>
</a>"""
blog["dorss"] = True
blog["rsstemplate"] = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Blog</title>
    <link>https://rathippo.sh/blog</link>
    <description>ratHippo's blog</description>
    {items}
  </channel>
</rss>
"""
blog["rssitemtemplate"] = """
<item>
    <title>{title}</title>
    <link>https://rathippo.sh/blog/articles/{path}</link>
    <description>{description}</description>
</item>
"""