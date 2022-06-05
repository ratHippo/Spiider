import json, markdown, os

srcdir = "src/articles/"
indexdir = "build/"
indexlinkdir = "articles/"
builddir = "build/articles/"

#Generate articles
if not os.path.exists(builddir): os.mkdir(builddir)

def generate_article(jsonpath, md):
    #Generates HTML given a json for metadata, and an md file for articles"
    data = json.loads(open(jsonpath, "r").read())
    title, date = data["title"], data["date"]
    article = markdown.markdown(open(md,"r").read())

    html = f"""
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

    return html

jsonfiles = []
for article in os.listdir(srcdir):
    if os.path.isdir(srcdir+article):
        jsonpath = srcdir + f"{article}/{article}.json"
        jsonfiles.append(jsonpath)
        md = srcdir + f"{article}/{article}.md"
        html = generate_article(jsonpath, md)
        if not os.path.exists(builddir + article): os.mkdir(builddir + article)
        file = open(builddir + f"{article}/{article}.html", "w")
        file.write(html)
        file.close()

#Generate index page
def generate_preview(jsonpath):
    data = json.loads(open(jsonpath, "r").read())
    return f"""<a class ="nocolor" href = {indexlinkdir}{data["path"]}>
        <card>
            <h3>{data["title"]}</h3>
            <p>{data["description"]}</p>
            <h5>{data["date"]}</h5>
          </card>
    </a>"""
def generate_index_page(jsonfiles):
    preview_list = list(generate_preview(i) for i in jsonfiles)
    previews = '\n'.join(preview_list)
    return (
        f"""
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
    )
index = open(indexdir + "index.html", "w")
index.write(generate_index_page(jsonfiles))
