% Main Title
% Main Author
% Main Date

All folders that contain a `index.html` file are included in the Menu above. Other pages can be linked like [Folder3/text1](Folder3/text1.html).

By adding `%box` to a markdown link, the page is linked as a box:

[Folder3/text1](Folder3/text1.html)%box

Any `html` pages within the same folder are listed as boxes.

Images are presented by default

![Default image with caption]($img/logo.png)

or with custom style, say `preview`

![Image caption]($img/logo.png)%preview

Style `person` moves images to the right and makes them black and white.

`_src/css/site.css` can be edited to change the style and add new ones.

![Image caption]($img/logo.png)%person
