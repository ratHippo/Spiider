import json, os, markdown, config, sys, shutil

class Folder:
    def __init__(self, srcdir = "",indexdir = "", builddir = "", articletemplate = "", indextemplate = "", previewtemplate = "", dorss = False, rsstemplate = "", rssitemtemplate = ""):
        self.srcdir, self.indexdir, self.builddir, self.articletemplate, self.indextemplate, self.previewtemplate, self.dorss, self.rsstemplate, self.rssitemtemplate = srcdir, indexdir, builddir, articletemplate, indextemplate, previewtemplate, dorss, rsstemplate, rssitemtemplate
def get_article_list(folder):
    articles = []
    for article in os.listdir(folder.srcdir):
        if get_metadata(folder, article) and not get_metadata(folder, article)["testing"]:
            articles.append(article)
    return articles
def get_metadata(folder, article):
    #markdown
    
    if os.path.exists(folder.srcdir+article+"/article.md"):
        md = markdown.Markdown(extensions=['full_yaml_metadata'])
        md.convert(open(folder.srcdir+article+"/article.md","r").read())
        return(md.Meta)
    #json
    elif os.path.exists(folder.srcdir+article+"/metadata.json"):
        metadata = json.loads(open(folder.srcdir+article+"/metadata.json","r").read())
        return metadata
    #none
    else:
        return None
#Generate articles
def generate_article(article, markdownpath, folder):
    #Generates HTML given json for metadata, md for text, and template"
    data = get_metadata(folder, article)
    article = markdown.markdown(open(markdownpath,"r").read(), extensions=['full_yaml_metadata'])

    return folder.articletemplate.format(title = data["title"], data = data["date"], article = article)
def write_articles(articles, folder):
    #Writes Articles to folders
    for article in articles:
        if os.path.exists(folder.srcdir + article + "/article.md"):

            markdownpath = folder.srcdir + f"{article}/article.md"
            html = generate_article(article, markdownpath, folder)
            if not os.path.exists(folder.builddir + article): os.mkdir(folder.builddir + article)
            file = open(folder.builddir + f"{article}/index.html", "w")
            file.write(html)
            file.close()

        #Although this script is intended for use with .md, we should still be able to use folders and other filetypes
        for file in os.listdir(folder.srcdir+article):
            dir = article + "/" + file
            if not os.path.exists(folder.builddir+dir):
                if file.endswith(".html"):
                    if not os.path.exists(folder.builddir + article): os.mkdir(folder.builddir + article)
                    shutil.copyfile(folder.srcdir+dir, folder.builddir+dir)

                if os.path.isdir(folder.srcdir+dir):
                        shutil.copytree(folder.srcdir+dir, folder.builddir+dir)

#Generate indexes
# The process used to generate an HTML index page and an RSS page are basically the same, only with different templates; therefore, generic functions are used
def generate_item(metadata, itemtemplate, returndate = False):
    #Generates item given metadata and template
    item = itemtemplate.format(
    path = metadata["path"], title = metadata["title"], description = metadata["description"], date = metadata["date"])
    if returndate: return [metadata["date"], item]
    else: return item
def generate_page(articles, folder, itemtemplate, pagetemplate):
    #Generates an rss file using a list of items
    item_list = list(generate_item(get_metadata(folder, article), itemtemplate, True) for article in articles)
    item_list = list([list(reversed(i[0].split("-"))), i[1]] for i in item_list)
    item_list.sort()
    item_list = list(reversed(item_list))
    item_list = list(i[1] for i in item_list)

    items = '\n'.join(item_list)
    return pagetemplate.format(items = items)

#Build
def build(folder):
    #Builds a folder using the functions above
    print(folder.indexdir[:-1]+": setting up directories...")
    if not os.path.exists(folder.indexdir): os.mkdir(folder.indexdir)
    if not os.path.exists(folder.builddir): os.mkdir(folder.builddir)
    articles = get_article_list(folder)
    print(folder.indexdir[:-1]+": writing articles...")
    write_articles(articles, folder)
    print(folder.indexdir[:-1]+": writing index page...")
    index = open(folder.indexdir + "index.html", "w")
    index.write(generate_page(articles, folder, folder.previewtemplate, folder.indextemplate))
    index.close()
    if folder.dorss:
        print(folder.indexdir[:-1]+": generating rss...")
        index = open(folder.indexdir + "index.rss", "w")
        index.write(generate_page(articles, folder, folder.rssitemtemplate, folder.rsstemplate))
        index.close()
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
        file.write("""---\ntitle: Sample\ndescription: This is a Sample Article\ndate: 7-23-22\npath: sample\ntesting: false\n---""")
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