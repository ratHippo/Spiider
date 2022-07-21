import json, markdown, os
from shutil import copyfile, copytree

blog = {}
blog["srcdir"] = "src/articles/"
blog["indexdir"] = "blog/"
blog["indexlinkdir"] = "articles/"
blog["builddir"] = "blog/articles/"
blog["articletemplate"] = str("""
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
""")
blog["indextemplate"] = str("""
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
""")
blog["previewtemplate"] = str("""
<a class ="nocolor" href = {indexlinkdir}{path}>
    <card>
        <h3>{title}</h3>
        <p>{description}</p>
        <h5>{date}</h5>
      </card>
</a>""")
blog["dorss"] = True
blog["rsstemplate"] = str("""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>Blog</title>
  <link>https://rathippo.sh/blog</link>
  <description>ratHippo's blog</description>
  {items}
</channel>
</rss>
""")
blog["rssitemtemplate"] = str("""
<item>
    <title>{title}</title>
    <link>https://rathippo.sh/blog/articles/{path}</link>
    <description>{description}</description>
</item>
""")
games = {}
games["srcdir"] = "src/games/"
games["indexdir"] = "games/"
games["indexlinkdir"] = ""
games["builddir"] = "games/"
games["articletemplate"] = str("""
<!DOCTYPE html>
<html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <link rel="stylesheet" href="../../index.css">
    </head>
    <body class="font1">
        <div class="main-content">
            <div class="grid">
                <h1>{title}</h1>
                <card>
                    {article}
                </card>
                <card>
                    <img src = "play/preview.png"></img>
                </card>
                <card>
                    <a href = "play/">click here to play</a>
                </card>
                <h3><a href="../">Back</a></h3>
                </div>
            </div>
    </body>
 </html>
""")
games["indextemplate"] = str("""
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="../index.css">
    <title> Games </title>
  </head>
  <body class = "font1">
    <div class = "main-content">
      <div class="grid">
        <h1>Games</h1>
        <card>
            <p>
                These are the games I've made, and I've put them here for you to play. Try them out, but they might be a bit laggy.
            </p>
        </card>
        {previews}
        <h3><a href = "/">back</a></h3>
    </div>
    </div>
  </body>
</html>
""")
games["previewtemplate"] = str("""
<a class ="nocolor" href = {indexlinkdir}{path}>
    <card>
        <h3>{title}</h3>
        <p>{description}</p>
        <h5>{date}</h5>
      </card>
</a>""")
games["dorss"] = False
def get_article_list(folder):
    articles = []
    for article in os.listdir(folder["srcdir"]):
        if get_metadata(folder, article) and not get_metadata(folder, article)["testing"]:
            articles.append(article)
    return articles
def get_metadata(folder, article):
    if os.path.exists(folder["srcdir"]+article+"/article.md"):
        md = markdown.Markdown(extensions=['full_yaml_metadata'])
        md.convert(open(folder["srcdir"]+article+"/article.md","r").read())
        return(md.Meta)
    elif os.path.exists(folder["srcdir"]+article+"/metadata.json"):
        metadata = json.loads(open(folder["srcdir"]+article+"/metadata.json","r").read())
        return metadata
    else:
        return None
#generate articles
def generate_article(article, markdownpath, folder):
    #Generates HTML given json for metadata, md for text, and template"
    data = get_metadata(folder, article)
    article = markdown.markdown(open(markdownpath,"r").read(), extensions=['full_yaml_metadata'])

    return folder["articletemplate"].format(title = data["title"], data = data["date"], article = article)
def write_articles(articles, folder):
    #Writes Articles to folders
    for article in articles:
        if os.path.exists(folder["srcdir"] + article + "/article.md"):

            markdownpath = folder["srcdir"] + f"{article}/article.md"
            html = generate_article(article, markdownpath, folder)
            if not os.path.exists(folder["builddir"] + article): os.mkdir(folder["builddir"] + article)
            file = open(folder["builddir"] + f"{article}/index.html", "w")
            file.write(html)
            file.close()

        #Although this script is intended for use with .md, we should still be able to use folders and other filetypes
        for file in os.listdir(folder["srcdir"]+article):
            dir = article + "/" + file
            if not os.path.exists(folder["builddir"]+dir):
                if file.endswith(".html"):
                    if not os.path.exists(folder["builddir"] + article): os.mkdir(folder["builddir"] + article)
                    copyfile(folder["srcdir"]+dir, folder["builddir"]+dir)

                if os.path.isdir(folder["srcdir"]+dir):
                        copytree(folder["srcdir"]+dir, folder["builddir"]+dir)
#Generate index page
def generate_preview(metadata, folder, returndate = False):
    #Generates preview given metadata and template
    data = metadata

    preview = folder["previewtemplate"].format(
    path = data["path"], title = data["title"], description = data["description"], date = data["date"], indexlinkdir = folder["indexlinkdir"]
    )
    if returndate: return [data["date"], preview]
    else: return preview
def generate_index_page(articles, folder):
    #Generates index page

    #sorts list by reverse date
    preview_list = list(generate_preview(get_metadata(folder, article), folder, True) for article in articles)
    preview_list = list([list(reversed(i[0].split("-"))), i[1]] for i in preview_list)
    preview_list.sort()
    preview_list = list(reversed(preview_list))
    preview_list = list(i[1] for i in preview_list)

    previews = '\n'.join(preview_list)
    return folder["indextemplate"].format(previews = previews)
#Generate RSS
def generate_rss_item(metadata, folder, returndate = False):
    data = metadata

    item = folder["rssitemtemplate"].format(
    path = data["path"], title = data["title"], description = data["description"]
    )
    if returndate: return [data["date"], item]
    else: return item
def generate_rss_page(articles, folder):
    item_list = list(generate_rss_item(get_metadata(folder, article), folder, True) for article in articles)
    item_list = list([list(reversed(i[0].split("-"))), i[1]] for i in item_list)
    item_list.sort()
    item_list = list(reversed(item_list))
    item_list = list(i[1] for i in item_list)

    items = '\n'.join(item_list)
    return folder["rsstemplate"].format(items = items)
#run
def run(folder):
    if not os.path.exists(folder["indexdir"]): os.mkdir(folder["indexdir"])
    if not os.path.exists(folder["builddir"]): os.mkdir(folder["builddir"])
    articles = get_article_list(folder)
    write_articles(articles, folder)
    index = open(folder["indexdir"] + "index.html", "w")
    index.write(generate_index_page(articles, folder))
    index.close()
    if folder["dorss"]:
        index = open(folder["indexdir"] + "index.rss", "w")
        index.write(generate_rss_page(articles, folder))
        index.close()

run(blog)
run(games)
