import os, markdown, config, sys, shutil
from datetime import datetime

class Folder:
    def __init__(self, srcdir = "",indexdir = "", builddir = "", articletemplate = "", indextemplate = "", previewtemplate = "", dofeed = False, feedtemplate = "", feeditemtemplate = ""):
        self.srcdir, self.indexdir, self.builddir, self.articletemplate, self.indextemplate, self.previewtemplate, self.dofeed, self.feedtemplate, self.feeditemtemplate = srcdir, indexdir, builddir, articletemplate, indextemplate, previewtemplate, dofeed, feedtemplate, feeditemtemplate

def get_article_list(folder):
    articles = []
    for article in os.listdir(folder.srcdir):
        if get_metadata(folder, article) and not get_metadata(folder, article)["testing"]:
            articles.append(article)
    return articles
def get_metadata(folder, article):
    if os.path.exists(folder.srcdir+article+"/article.md"):
        md = markdown.Markdown(extensions=['full_yaml_metadata'])
        md.convert(open(folder.srcdir+article+"/article.md","r").read())
        md.Meta["content"] = markdown.markdown(open(folder.srcdir+article+"/article.md","r").read(), extensions = ['full_yaml_metadata'])
        return(md.Meta)
    #none
    else:
        return None
#Generate articles
def generate_article(article, folder):
    #Generates HTML given md for metadata, md for text, and template"
    metadata = get_metadata(folder, article)
    return folder.articletemplate.format(title = metadata["title"], date = metadata["date"], article = metadata["content"])
def write_articles(articles, folder):
    #Writes Articles to folders
    for article in articles:
        if os.path.exists(folder.srcdir + article + "/article.md"):

            html = generate_article(article, folder)
            if not os.path.exists(folder.builddir + article): os.mkdir(folder.builddir + article)
            file = open(folder.builddir + f"{article}/index.html", "w")
            file.write(html)
            file.close()

        #Copy other files such as an assets folder
        for file in os.listdir(folder.srcdir+article):
            dir = article + "/" + file
            if not os.path.exists(folder.builddir+dir):
                if os.path.isdir(folder.srcdir+dir):
                        shutil.copytree(folder.srcdir+dir, folder.builddir+dir)

#Generate index
def generate_item(metadata, itemtemplate, returndate = False):
    #Generates item given metadata and template
    item = itemtemplate.format(
    path = metadata["path"], title = metadata["title"], description = metadata["description"], date = metadata["date"], fulldate = datetime.strptime(metadata["date"], config.datetimeformat).strftime(config.fulldateformat))
    if returndate: return [datetime.strptime(metadata["date"], config.datetimeformat), item]
    else: return item
def generate_page(articles, folder, itemtemplate, pagetemplate):
    #Generates an feed file using a list of items
    item_list = list(generate_item(get_metadata(folder, article), itemtemplate, True) for article in articles)
    item_list = list([item[0].strftime("%Y%m%d%H%M%S"), item[1]] for item in item_list)
    item_list.sort(reverse=True)
    item_list = list(i[1] for i in item_list)

    return pagetemplate.format(items = '\n'.join(item_list))

#Build
def build(folder):
    #Builds a folder using the functions above
    print(folder.indexdir[:-1]+": setting up directories...")
    for d in (folder.indexdir, folder.builddir): 
        if not os.path.exists(d): os.mkdir(d)
    articles = get_article_list(folder)
    print(folder.indexdir[:-1]+": writing articles...")
    write_articles(articles, folder)
    print(folder.indexdir[:-1]+": writing index page...")
    index = open(folder.indexdir + "index.html", "w")
    index.write(generate_page(articles, folder, folder.previewtemplate, folder.indextemplate))
    index.close()
    if folder.dofeed:
        print(folder.indexdir[:-1]+": generating feed...")
        feed = open(folder.indexdir + "feed.xml", "w")
        feed.write(generate_page(articles, folder, folder.feeditemtemplate, folder.feedtemplate))
        feed.close()
def cli(args):
    if args[0] == "build":
        if len(args) == 1:
            for folder in config.folders:
                build(config.folders[folder])
        elif len(args) == 2:
            build(config.folders[args[1]])
        elif len(args) == 3:
            write_articles([args[2]], config.folders[args[1]])
    elif args[0] == "new":
        folder = config.folders[args[1]]
        name = args[2]
        if not os.path.exists(folder.srcdir + name): os.mkdir(folder.srcdir + name)
        file = open(folder.srcdir + f"{name}/article.md", "w")
        file.write(f"""---\ntitle: Sample\ndescription: This is a Sample Article\ndate: \"{datetime.now().strftime(config.datetimeformat)}\"\npath: {name}\ntesting: false\n---""")
        file.close()      
    elif args[0] == "remove":
        input("This will remove the article and all files in the article's directory. Exit the program if you want to prevent this. Press enter to continue.")
        folder = config.folders[args[1]]
        name = args[2]
        if os.path.exists(folder.srcdir + name): shutil.rmtree(folder.srcdir + name)
    elif args[0] == "rename":
        folder = config.folders[args[1]]
        name = args[2]
        new_name = args[3]
        shutil.move(folder.srcdir + name, folder.srcdir + new_name)   
    else:
         print("No such thing as argument \'"+args[0]+"\'.")

if __name__ == '__main__':
    os.chdir(os.getcwd())  
    cli(sys.argv[1:])