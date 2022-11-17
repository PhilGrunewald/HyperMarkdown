import os
import glob
import re

root = "./public_html/"
header = "./res/header.html"
footer = "./res/footer.html"
css    = "./source/css"
images = "./source/img"

title = "Energy Demand Observatory & Laboratory"

os.system(f'rm -rf {root}')
os.system(f'mkdir {root}')
os.system(f'cp -rf {css} {root}')
os.system(f'cp -rf {images} {root}')

# recreate the md files as html files
for item in glob.glob('./source/**', recursive=True):
    target = item[:].replace('./source/',root)
    if item.endswith('.md'):
        print(item, "to html")
        os.system(f'pandoc -s {item} -o {target[:-3]}.html')
    elif os.path.isdir(item) and not os.path.exists(target):
        os.system(f'mkdir {target}')

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
            navInsert = i
        if "navTitle" in line:
            head[i] = line.replace("navTitle",title)

with open(footer) as file:
    foot = file.readlines()

for item in sorted(glob.glob(f'{root}**', recursive=True)):
    href  = item.split(root)[1]
    if item.endswith('index.html'):
        label = item.split('/index.html')[0]
        label = label.split('/')[-1]
        if label[1] == '_':
            # first character is for sorting - is removed
            label = label[2:]
        if label != "public_html":
            # Don't do Home as nav item (title does that)
            head.insert(navInsert,f'<a class="page-link" href="./{href}">{label}</a>\n')
            navInsert+=1

        # append any other html files in this folder as boxes
        folder = item.split("index.html")[0]
        flexboxes = []
        for subitem in sorted(glob.glob(f'{folder}*.html'),reverse = True):
            subtext = []
            if subitem != item:
                with open(subitem) as file:
                    lines = file.readlines()
                hasImage = False
                subItemType = ''
                for i,line in enumerate(lines):
                    if '%type:' in line:
                        subItemType = line.split('%type:')[-1].split('</p>')[0]
                    if 'class="title"' in line:
                        subtext.append(line)
                    if 'class="author"' in line:
                        subtext.append(line)
                    if 'class="date"' in line:
                        subtext.append(line)
                    if ('img src=' in line) and not hasImage:
                        className = ''
                        if ">%" in line:
                            className = line.split('>%')[-1].split('</p>')[0]
                        if 'class=' in line:
                            line = line.replace('class="',f'class="preview {className} ')
                        else:
                            line = line.replace(' src=',f' class="preview {className}" src=')
                        subtext.insert(1,line)
                        hasImage = True # only one image allowed
            if subtext:
                url = subitem.split('/')[-1]
                subtext.insert(0,f"""
                        <a class="flex-link" href="{url}">\n
                          <div class="flex-item">\n
                            <div class="flex-top {subItemType}"></div>\n
                        <div class="flex-content">\n""")
                subtext.append('<p><i>More ...</i></p>  </div></div></a>\n')
                for line in subtext:
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
                lines[i] = ''
            if '<h1 class="title">' in line:
                title = line.split('<h1 class="title">')[1]
                title = title.split('</h1>')[0]
                lines[i] = f"{line}<title>{title}</title>"
            if '<img ' in line:
                # href = re.search(r'src=".+?"',line).group().replace('src','<a href')
                # if "/>%icon" in line:
                className = ''
                if ">%" in line:
                    className = line.split('>%')[-1].split('</p>')[0]
                    line = f"{line.split('>%')[0]}>"
                line = line.replace('<p>','')
                line = line.replace('</p>','')
                line = line.replace(f'>',f'onclick="this.classList.toggle(\'big\');" class="{className}">\n')
                lines[i] = line

        href  = item.split(root)[1]
        print(href)
        thisFoot = foot[:]
        if href.count('/') > 0:
            subLevel = "../" * href.count('/')
            print(href, subLevel)
            for i,line in enumerate(head):
                if href in line:
                   head[i] = line.replace('page-link','page-link-active')
                if '="./' in line:
                    head[i] = head[i].replace('="./',f'="{subLevel}')

            for i,line in enumerate(thisFoot):
                if '="./' in line:
                    thisFoot[i] = line.replace('="./',f'="{subLevel}')

        with open(item,'w') as file:
            file.writelines(head)
            file.writelines(lines[start:end])
            file.writelines(thisFoot)
