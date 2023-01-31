<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" type="text/css" href="./slides.css">
</head>
<body>
<iframe id="web" width="1680" height="945" src="" frameborder="0" allowfullscreen></iframe>

<?php
$SVGs = array_reverse(glob('*.svg'));
if (isset($_GET['svg'])) {
  $SVG = $_GET['svg'];
  echo "<object id='slides' type='image/svg+xml' data='$SVG.svg' width='100%'></object>";
  $SVGs = ["$SVG.svg"];
} else {
  foreach ($SVGs as $SVG) {
    $fname = trim($SVG,".svg");
    echo "<a href='index.php?svg=$fname' class='thumbLink'>
      <span class='thumbSpan'>
        <object class='thumb' type='image/svg+xml' data='$SVG'></object>
      </span></a>";
  }
}
echo "<div id='nav' class='nav'>";
echo "<a href='index.php' class='nav-item'><img src='img/home.svg' height='20px'></a>";
foreach ($SVGs as $SVG) {
    $fname = substr($SVG,0,-4);
    echo "<a href='index.php?svg=$fname' class='nav-item'> $fname </a>";
}
?>

<script>
var width = 508;
var height = 285.75;
var extent_x =0;
var extent_y =0;

var slide = document.getElementById("slides");
var nav = document.getElementById("nav");
var page = 0;
var xy = new Array();

document.getElementById('web').style.display = 'none';

slide.addEventListener("load",function(){
    var level = 0;
    var svgDoc = slide.contentDocument;
    var pages = svgDoc.getElementsByTagName('inkscape:page')

    // page ordering by xy position
    for (let p = 0; p < pages.length; p++) {
        var x = pages[p].getAttribute('x');
        var y = pages[p].getAttribute('y');
        console.log(pages[p]);
        extent_x = Math.max(extent_x,x);
        extent_y = Math.max(extent_y,y);
        xy[p] = parseInt(x) + parseInt(width*20*y);
        }
    var rank = [...xy].sort(function (a,b) {return a-b;});
    var pageOrder = new Array();
    for (let p = 0; p < xy.length; p++) {
        pageOrder[rank.indexOf(xy[p])] = p;
        }
    console.log("Page order: ", pageOrder);

    // navigation bar
    for (let p = 0; p < pageOrder.length; p++) {
        var pNav  = document.createElement('span');
        var title = pages[pageOrder[p]].getAttribute('inkscape:label');
        if (title) {
          if (title.startsWith('https://')) {
            pNav.setAttribute("onclick",`page=${p};goURL("${title}")`);
            pNav.innerHTML = "▶";
          } else {
            pNav.innerHTML = title;
            pNav.setAttribute("onclick",`page=${p};moveTo(${pageOrder[p]})`);
          }
        } else {
            pNav.innerHTML = p+1;
            pNav.setAttribute("onclick",`page=${p};moveTo(${pageOrder[p]})`);
        }
        pNav.id = `nav${p}`;
        pNav.className = 'nav-item';
        nav.appendChild(pNav);
        var navSpacer  = document.createElement('span');
        navSpacer.innerHTML = " ";
        nav.appendChild(navSpacer);
        }

    moveTo(pageOrder[page]);

    // next/appear
    svgDoc.addEventListener("mousedown",function(){ advance() }, false);
    svgDoc.addEventListener("keydown",function(e){ 
        if (e.key == 'ArrowLeft') {
            if (level > 1) {
            console.log("LEVEL DOWN ", level);
               var noShow = svgDoc.getElementsByClassName(`show${level-1}`);
               for (let i = 0; i < noShow.length; i++) {
                   noShow[i].setAttribute("visibility","hidden");
               }
               level -= 2;
              }
           else if (page > 0) {
                page -=2;
                level = 0;
              }
            advance();
          }
        if (e.key == 'ArrowRight') { advance(); }
        if (e.key == ' ') { advance(); }
        console.log(e.key);
        }, false);


    function advance() {
       var hide = svgDoc.getElementsByClassName(`hide${level}`);
       for (let i = 0; i < hide.length; i++) {
           hide[i].setAttribute("visibility","hidden");
       }
       var show = svgDoc.getElementsByClassName(`show${level}`);
       var showOnSlide = new Array();
       for (let i = 0; i < show.length; i++) {
           var e = show[i].getBoundingClientRect();
             if ((e.x > 0) && (e.x < window.innerWidth) && (e.y > 0) && (e.y < (window.innerWidth/width*height))) {
              // is on slide
              showOnSlide.push(show[i]);
             }
           }
       for (let i = 0; i < showOnSlide.length; i++) {
           showOnSlide[i].setAttribute("visibility","visible");
       }
        console.log("Animated items at this level: ",showOnSlide.length);
       if (showOnSlide.length < 1) {
          page += 1;
          var title = pages[pageOrder[page]].getAttribute('inkscape:label');
          if (title) {
            if (title.startsWith('https://')) {
              console.log("URL page: ",title);
              moveTo(pageOrder[page]);
              goURL(title);
            } else {
            moveTo(pageOrder[page]);
          }

          } else {
            moveTo(pageOrder[page]);
          }
          level = 1;
       } else {
          level += 1;
       }
    }
}, false);

function goURL(url) {
  var web = document.getElementById('web');
    console.log("GO URL: ",url);
      web.setAttribute('src',url);
      web.style.display = '';
  document.getElementById('slides').style.display = 'none';
}

function moveTo(p) {
  document.getElementById('slides').style.display = '';
  document.getElementById('web').style.display = 'none';

    console.log("X page: ",page);
    level = 1;
    var svgDoc = slide.contentDocument;
    var pages = svgDoc.getElementsByTagName('inkscape:page')
    var x = (pages[p].getAttribute('x'));
    var y = (pages[p].getAttribute('y'));
    console.log(y);
    var svg   = svgDoc.getElementById('svg2')
    svg.setAttribute('viewBox',[x, y, width, height]);

    var prev = document.getElementsByClassName('nav-item visited current');
    if (prev.length > 0) {
        prev[0].className = 'nav-item visited';
    }
    pNav = document.getElementById(`nav${page}`);
    pNav.className = 'nav-item visited current';

    // hide
    for (let l = 0; l < 10; l++) {
        var collection = svgDoc.getElementsByClassName(`show${l}`);
        for (let i = 0; i < collection.length; i++) {
          collection[i].setAttribute("visibility","hidden");
          }
        }

}

function overview() {
  // obsolete
  var svgDoc = slide.contentDocument;
  var svg   = svgDoc.getElementById('svg2')
  console.log(extent_x);
  svg.setAttribute('viewBox',[0, 0, extent_x+width, extent_y+height]);
}

</script>
</body>
