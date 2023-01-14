% Hyper-Markdown
% Turns markdown files and folder structure into websites


Summary
=======

A python script using [pandoc](https://pandoc.org/) to convert markdown to html. Folder structure becomes menu structure.

Use
---

- Clone this repository
- Edit files in `source/`
- Run `python build.py`
- Servable files end up in `public_html` (this gets rewritten each time, so don't edit files there!)
- Files other than `.md` get copied as are (e.g. html,js,php,css,png,svg,jpg,pdf)
- Done

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

The _\$_ symbol acts are the root of the site (i.e. `public_html`). To link `source/Folder1/text1.md` use

```markdown
  [Text 1]($Folder1/text1.html)
```

as the url. Relative links work as normal.

Short links can be declared in `res/redirect.json`:

```json
{
  "F1t1": "Folder1/text1.html
}
```

```markdown
  [Text 1]($F1t1)
```

now resolves to the `Folder1/text1.html` file, via a redirection file (`F1t1/index.html`)

Customisations
--------------

Classes can be added to links and images:

```markdown
   ![Image caption]($img/navajo.png)%big
```

A link followed by `%box` is renedered as a box, using page `title, author and date` from the first three lines for content.

