import os
import glob
import json

root = "./public_html/"
header = "./res/header.html"
footer = "./res/footer.html"
links  = "./res/links.json"
redirect = "./res/redirect.html"
css    = "./source/css"
images = "./source/img"

title = "Energy Demand Observatory & Laboratory"
shorttitle = "EDOL"

os.system(f'rm -rf {root}')
os.system(f'mkdir {root}')
os.system(f'cp -rf {css} {root}')
os.system(f'cp -rf {images} {root}')

# recreate the md files as html files
for item in glob.glob('./source/**', recursive=True):
    target = item[:].replace('./source/',root)
    if item.endswith('.md'):
        # generate HTML
        os.system(f'pandoc -s {item} -o {target[:-3]}.html')
    elif (list(filter(item.endswith, ['.html','.svg','.php','.css','.png','jpg','.pdf'])) != []):
        # Copy file
        os.system(f'cp {item} {target}')
    elif os.path.isdir(item) and not os.path.exists(target):
        os.system(f'mkdir {target}')
    if os.path.isdir(item) and not os.path.exists(f'{item}banner.png'):
        os.system(f'cp ./source/img/banners/banner.png {target}')

# tidy up html (all tags on one line)
for item in glob.glob(f'{root}**', recursive=True):
    if item.endswith('.html'):
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

# find insertion points
with open(header) as file:
    head = file.readlines()
    for i,line in enumerate(head):
        if "cssInsert" in line:
            cssInsert = i
        if "navInsert" in line:
            navInsertMaster = i
        if "navTitle" in line:
            head[i] = line.replace("navTitle",title)

with open(footer) as file:
    foot = file.readlines()

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

for item in sorted(glob.glob(f'{root}**', recursive=True)):
    href  = item.split(root)[1]
    if item.endswith('index.html'):
        # append html files in this folder as boxes
        folder = item.split("index.html")[0]
        flexboxes = []
        for subitem in sorted(glob.glob(f'{folder}*.html'),reverse = True):
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
    for i,line in enumerate(text):
        if find in line:
            text[i] = line.replace(find,replace)
    return text

masterHead = head
for item in glob.glob(f'{root}**', recursive=True):
    if item.endswith('.html'):
        head = masterHead[:]
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

        href  = item.split(root)[1]
        thisFoot = foot[:]

        # Links to subfolders in MENU
        fileName = item.split('/')[-1]
        folderPath = item.split(fileName)[0]
        # Nav item UP one level
        label = folderPath.split('/')[-2]
        navInsert = navInsertMaster
        if label == 'public_html':
            head.insert(navInsert,f'<a class="page-link" href="./"> <b>{shorttitle}</b> </a>\n')
        else:
            if label[1] == '_':
                # first character is for sorting - is removed
                label = label[2:]
            head.insert(navInsert,f'<a class="page-link" href="../"> <b>⇐ {label}</b> </a>\n')
        navInsert+=1
        # Nav: all subfolders with index.html get a menu item
        for folder in glob.glob(f'{folderPath}**', recursive=False):
            if os.path.isdir(folder) and (os.path.exists(f'{folder}/index.html') or os.path.exists(f'{folder}/index.php')):
                label = folder.split('/')[-1]
                head.insert(navInsert,f'<a class="page-link" href="{label}">{label}</a>\n')
                navInsert+=1
        if href.count('/') > 0:
            subLevel = "../" * href.count('/')
            for i,line in enumerate(head):
                if href in line:
                   head[i] = line.replace('page-link','page-link-active')
                if '="./' in line:
                    head[i] = head[i].replace('="./',f'="{subLevel}')
            for i,line in enumerate(lines):
                if '="$' in line:
                    lines[i] = line.replace('="$',f'="{subLevel}')
            for i,line in enumerate(thisFoot):
                if '="./' in line:
                    thisFoot[i] = line.replace('="./',f'="{subLevel}')

        with open(item,'w') as file:
            file.writelines(head)
            file.writelines(lines[start:end])
            file.writelines(thisFoot)

# short links
with open(links) as file:
    url = json.load(file)

with open(redirect) as file:
    linkMaster = file.readlines()

for key in url:
    thisLink = linkMaster[:]
    thisLink = replaceText(thisLink,"$url",f"../{url[key]}")
    thisLink = replaceText(thisLink,"$key",key)
    os.system(f'mkdir {root}{key}')
    with open(f'{root}{key}/index.html','w') as file:
        file.writelines(thisLink)
