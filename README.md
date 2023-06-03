% EDOL Hyper-Markdown
% Turns markdown files and folder structure into websites

Author:  Phil Grunewald
Licence: MIT (see docs)
Version: v0.3
Date:    2 June 23

Summary
=======

Project repository for website and file sharing.

Use
---

### Option 1:

- Clone this repository
- Checkout the `source` branch

```git add remote edol edol@edol.uk:/var/www/edol.uk/.git```

- Edit files in `_src/`
- Add, commit, push (only `_res` and `_src` folders)

Done! The website is automatically update.

The site is available on [EDOL.uk](https://edol.uk)

### Option 2:

- Clone this repository
- check out the `site` branch (git checkout site)
- Edit files in `source/`
- Run `python post-update`
- Add, commit, push origin


- Servable files end up in repo root folder (this gets rewritten each time, so don't edit files there!)
- Files other than `.md` get copied as are (e.g. html,js,php,css,png,svg,jpg,pdf)


Conventions
-----------

- All folders that contain an `index.md` file get listed in the menu
- The first three markdown lines with a leading '%' are treated as `title, author and date`
- Subfolders are listed as Menu items
- All pages within a folder are listed as boxes
- Everythind is ordered by `date modified` (unless specified in `order.txt` within a folder)

Styling
-------

The `site.css` style is used by default. Modify this file to affect all pages or add custom css files to override/add styles for specific pages. In markdown identify the css file by adding the line

`% custom.css`

anywhere in the text.

Banners
-------

The file `img/banner.png` is used as default banner. 
If a file named `banner.png` exists within a folder, this is used instead.
If a file and a line containing:

>% banner: mybanner.png

this image is used instead


Cross-referencing
-----------------

The _\$_ symbol acts are the root of the site. To link `source/Folder1/text1.md` use

```markdown
  [Text 1]($Folder1/text1.md)
```

as the url from any sub-folder. Relative links work as normal. (Note that the target file ends

Short links
-----------

Short links can be declared in `res/config.json` under `Links`:

```json
{
  "F1t1": "Folder1/text1.html"
}
```

```markdown
  [Text 1]($F1t1)
```

now resolves to the `Folder1/text1.html` file, via a redirection file (`F1t1/index.html`)

Customisations
--------------

### Custom classes

Classes can be added to links and images with a trailing `%`:

```markdown
   ![Image caption]($img/navajo.png)%big
```

Style classes are declared in `source/css/site.css` and can be modified to suit.

### Boxes

The same box layout that is applied to pages within a folder can be used for linked pages.

A link followed by `%box` is renedered as a box, using page `title, author and date` from the first three lines for content.

Wrapping multiple boxes between `%flex` and `%/flex` comments ensures that they wrap on the page.

```
 %flex

 []($absolute_path)%box

 [Title, address, date, img](relative_path)%box

 %/flex
```
