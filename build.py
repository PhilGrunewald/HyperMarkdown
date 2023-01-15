#!/usr/bin/env python3

import os
import glob
import json

root = "./public_html/"
header = "./res/header.html"
footer = "./res/footer.html"
links  = "./res/links.json"
redirect = "./res/redirect.html"
source = "./source/"
css    = "./source/css"
images = "./source/img"

title = "Long title for the website"
shorttitle = "Short title"

""" COMMENT """


def createFolder(item):
    """ create all folders 
        populate all folders with a banner.png
        touch files to bump them up the 'date modified' order
    """
    # touch files to order by 'last modified'
    target = item[:].replace(source,root)
    os.system(f'mkdir -p {target}')
    # add default banner
    if not os.path.exists(f'{item}banner.png'):
        os.system(f'cp {source}img/banner.png {target}')
    # touch to reorder (if specified)
    if os.path.isfile(f'{item}/order.txt'):
        with open(f'{item}/order.txt') as file:
            files = file.readlines()
        for file in reversed(files):
            os.system(f'touch {item}/{file}')

def toHTML(item):
    """ process with pandoc or just copy """
    target = item[:].replace(source,root)
    if item.endswith('.md'):
        # generate HTML
        os.system(f'pandoc -s {item} -o {target[:-3]}.html')
    elif (list(filter(item.endswith, ['.html','.svg','.php','.css','.png','jpg','.pdf'])) != []):
        # Copy file
        os.system(f'cp {item} {target}')

def cleanHTML(item):
    """ tidy up html (all tags on one line) """
    with open(item) as file:
        lines = file.readlines()
    newLines = []
    buffer = ''
    for i,line in enumerate(lines):
        buffer = f'{buffer} {line[:-1]}'
        if line.endswith('>\n'):
            newLines.append(f'{buffer}\n')
            buffer = ''
    with open(item,'w') as file:
        file.writelines(newLines)

def boxContent(htmlFile):
    with open(htmlFile) as file:
        lines = file.readlines()
    lines.reverse()
    url      = htmlFile.replace(root,'$')
    dateLine = 0
    authorLine = 0
    itemType = ''
    title    = ''
    author   = ''
    date     = ''
    image    = ''
    for i,line in enumerate(lines):
        if '%type:' in line:
            itemType = line.split('%type:')[-1].split('</p>')[0]
        if 'class="title"' in line:
            title = line
            if authorLine < i-3:
                # author does not belong to this title
                author = ''
            if dateLine < i-5:
                date = ''
        if 'class="author"' in line:
            author = line
            authorLine = i
        if 'class="date"' in line:
            date = line
            dateLine = i
        if ('img src=' in line): #  and not hasImage:
            className = ''
            if ">%" in line:
                className = line.split('>%')[-1].split('</p>')[0]
            if 'class=' in line:
                line = line.replace('class="',f'class="preview {className} ')
            else:
                line = line.replace(' src=',f' class="preview {className}" src=')
            image = line
    return f"""
              <div class="flex-item">
                <a class="flex-link" href="{url}">
                    <div class="flex-top {itemType}"></div>
                        <div class="flex-content">
                            {image}
                            {title}
                            {author}
                            {date}
                            <p><i>More ...</i></p>
                        </div>
                    </a>
                </div>
            """

def addBoxes(item):
    """ get the first lines in local files and add to box """
    # append html files in this folder as boxes
    folder = item.split("index.html")[0]
    flexboxes = []
    subitems = glob.glob(f'{folder}*.html')
    subitems.sort(key=os.path.getmtime)
    for subitem in reversed(subitems):
        if subitem != item:
            for line in boxContent(subitem):
                flexboxes.append(line)
    if flexboxes:
        flexboxes.insert(0,'<div class="flex-container">\n')
        flexboxes.append('</div>\n<br><br>\n')
    with open(item) as file:
        lines = file.readlines()
    for i,line in enumerate(lines):
        if "</body>" in line:
            end = i
    for line in flexboxes:
        lines.insert(end,line)
        end+=1
    with open(item,'w') as file:
        file.writelines(lines)

def replaceText(text,find,replace):
    """ line by line replacement """
    for i,line in enumerate(text):
        if find in line:
            text[i] = line.replace(find,replace)
    return text

def reorderFolders(srcItems):
    """ touch any folder listed
        add to 'date modified'
        to bump them up the order
    """
    for item in srcItems:
        if os.path.isdir(item):
            target = item[:].replace(source,root)
            # touch to reorder (if specified)
            if os.path.isfile(f'{item}/order.txt'):
                with open(f'{item}/order.txt') as file:
                    files = file.readlines()
                for i,file in enumerate(reversed(files)):
                    dest = f'{target}{file}'.split('\n')[0]
                    if not os.path.isdir(dest):
                        dest = f'{target}/{file}'.split('\n')[0]
                        dest = dest.replace('.md','.html')
                    # add 1s per line to mod time to move up rank
                    os.system(f"touch -r {dest} -A {i:02} {dest}")


def getHead(item):
    # Links to subfolders in MENU
    head = globalHead[:]
    fileName = item.split('/')[-1]
    folderPath = item.split(fileName)[0]
    # Nav item UP one level
    label = folderPath.split('/')[-2]
    navInsert = navInsertMaster
    if label == 'public_html':
        head.insert(navInsert,f'<a class="page-link" href="./"> <b>{shorttitle}</b> </a>\n')
    else:
        head.insert(navInsert,f'<a class="page-link" href="../"> <b>⇐ {label}</b> </a>\n')
    navInsert+=1
    # Nav: all subfolders with index.html get a menu item
    folders = glob.glob(f'{folderPath}**', recursive=False)
    folders.sort(key=os.path.getmtime)
    # for folder in glob.glob(f'{folderPath}**', recursive=False):
    for folder in reversed(folders):
        if os.path.isdir(folder) and (os.path.exists(f'{folder}/index.html') or os.path.exists(f'{folder}/index.php')):
            label = folder.split('/')[-1]
            head.insert(navInsert,f'<a class="page-link" href="{label}">{label}</a>\n')
            navInsert+=1
    return head


def relativeLinks(item,text):
    """ highlight current page if in Menu
        $  > absolute path
        ./ > relative path
    """
    href  = item.split(root)[1]
    sublevel = './'
    if href.count('/') > 0:
        sublevel = "../" * href.count('/')
    for i,line in enumerate(text):
        if href in line:
           text[i] = line.replace('page-link','page-link-active')
        if '="./' in line:
            text[i] = line.replace('="./',f'="{sublevel}')
        if '="$' in line:
            text[i] = line.replace('="$',f'="{sublevel}')
    return text


def processHTML(item):
    """ line by line check of changes needed 
        insert Header
        update css
        insert banner
        format title
        classify images
        turn links into boxes
        add links to Menu
    """
    head = getHead(item)
    foot = globalFoot[:]
    with open(item) as file:
        lines = file.readlines()
    body = 0
    for i,line in enumerate(lines):
        if ("<body>" in line) or ("<!-- HeaderEnd -->" in line):
            start = i+1
        if "</body>" in line:
            end = i
        if "<p>%" in line:
            if ".css</p>" in line:
                css = line.split("<p>%")[-1]
                css = css.split("</p>")[0].strip()
                head.insert(cssInsert,f'  <link rel="stylesheet" href="./css/{css}">\n')
            if "banner:" in line:
                banner = line.split("banner:")[-1].split("</p>")[0].strip()
                head = replaceText(head,"url('banner.png')",f"url('{banner}')")
            lines[i] = ''
        if '<h1 class="title">' in line:
            title = line.split('<h1 class="title">')[1]
            title = title.split('</h1>')[0]
            lines[i] = f"{line}<title>{title}</title>"
        if '<img ' in line:
            className = ''
            if ">%" in line:
                className = line.split('>%')[-1].split('</p>')[0]
                line = f"{line.split('>%')[0]}>"
            line = line.replace('<p>','')
            line = line.replace('</p>','')
            line = line.replace(f'>',f'onclick="this.classList.toggle(\'big\');" class="{className}">\n')
            lines[i] = line
        if '</a>%box' in line:
            url = line.split('href="')[-1].split('"')[0]
            lines[i] = boxContent(f"{root}{url}")


    head = relativeLinks(item,head)
    lines = relativeLinks(item,lines)
    foot = relativeLinks(item,foot)

    with open(item,'w') as file:
        file.writelines(head)
        file.writelines(lines[start:end])
        file.writelines(foot)

def shortlinks():
    """ add folders with index.html as short link destination """
    # short links
    with open(links) as file:
        url = json.load(file)
    # template
    with open(redirect) as file:
        linkMaster = file.readlines()
    for key in url:
        thisLink = linkMaster[:]
        thisLink = replaceText(thisLink,"$url",f"../{url[key]}")
        thisLink = replaceText(thisLink,"$key",key)
        os.system(f'mkdir {root}{key}')
        with open(f'{root}{key}/index.html','w') as file:
            file.writelines(thisLink)

## END FUNCTIONS ##

## GLOBAL ##

# find insertion points
with open(header) as file:
    globalHead = file.readlines()
for i,line in enumerate(globalHead):
    if "cssInsert" in line:
        cssInsert = i
    if "navInsert" in line:
        navInsertMaster = i
    if "navTitle" in line:
        globalHead[i] = line.replace("navTitle",title)

with open(footer) as file:
    globalFoot = file.readlines()


## MAIN ##
# clean slate
os.system(f'rm -rf {root} && mkdir {root}')
# process source files
srcItems = glob.glob(f'{source}**', recursive=True)
for item in srcItems:
    if os.path.isdir(item):
        createFolder(item)
# process in order of modification
srcItems.sort(key=os.path.getmtime)
for item in srcItems:
    toHTML(item)

reorderFolders(srcItems)
# switch to public_html
items = glob.glob(f'{root}**', recursive=True)
items.sort(key=os.path.getmtime)
for item in items:
    if item.endswith('.html'):
        cleanHTML(item)
        addBoxes(item)
        processHTML(item)

shortlinks()
