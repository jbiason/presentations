"use strict";

/* htmlslides

Info and examples: https://gitlab.com/andybalaam/htmlslides

Structure your HTML like this:

<html>
<head>
    <meta charset="utf-8"/>
    <link rel="stylesheet" href="htmlslides.css">
    <script src="htmlslides.js"></script>
    <title>How to Surf the Mist</title>
</head>

<body>
    <header>
        <h1>How to Surf the Mist</h1>
        <!-- ... some stuff ... -->
    </header>
    <section id="contents">
        <h2>Contents</h2>
        <ul><li><a href="#breathin">First, breath in</a></ul>
        <!-- ... some stuff ... -->
    </section>
    <section id="breathin">
        <h2>First, breath in</h2>
        <!-- ... some stuff ... -->
    </section>
    <!-- ... more slides ... -->
</body>
</html>

Open the Developer Tools in your browser and check the Console output. If
htmlslides was unable to understand your HTML, it will print error messages
there.

You can disable mouse-clicking by including htmlslides.js like this:

<script src="htmlslides.js"></script>
<script>
htmlslides.config.mouse_moves_pages = false;
</script>

*/

let htmlslides = {}

htmlslides.config = {
    "mouse_moves_pages": true
};

(function() {

let slide_anchors;
let current_slide;
let header;
let sections;

const KEY_PAGEUP   = 33;
const KEY_PAGEDOWN = 34;
const KEY_END      = 35;
const KEY_HOME     = 36;
const KEY_LEFT     = 37;
const KEY_RIGHT    = 39;

function on_load() {
    window.addEventListener("scroll", on_scroll);
    document.addEventListener("keydown", on_key);
    document.body.addEventListener('click', on_left_click);
    document.body.addEventListener('contextmenu', on_right_click);

    header = document.getElementsByTagName("header")[0];
    sections = document.getElementsByTagName("section");
    slide_anchors = scan_slides();
    current_slide = find_slide(slide_anchors, window.location.hash);
}

function is_interactive_element(element) {
    let tag = element.tagName.toLowerCase();
    return (tag === "a" || tag === "button" || tag === "input");
}

function on_left_click(event) {
    if (!htmlslides.config.mouse_moves_pages) {
        return;
    }
    if (is_interactive_element(event.target)) {
        return;
    }
    event.preventDefault();
    return go_to_slide(current_slide + 1);
}

function on_right_click(event) {
    if (!htmlslides.config.mouse_moves_pages) {
        return;
    }
    if (is_interactive_element(event.target)) {
        return;
    }
    event.preventDefault();
    return go_to_slide(current_slide - 1);
}

function on_key(event) {
    if (event.altKey || event.ctrlKey || event.shiftKey) {
        return;
    }

    switch(event.keyCode) {
        case KEY_LEFT:
        case KEY_PAGEUP:
            event.preventDefault();
            return go_to_slide(current_slide - 1);
        case KEY_RIGHT:
        case KEY_PAGEDOWN:
            event.preventDefault();
            return go_to_slide(current_slide + 1);
        case KEY_HOME:
            event.preventDefault();
            return go_to_slide(0);
        case KEY_END:
            event.preventDefault();
            return go_to_last_slide();
    }
}

function on_scroll() {
    if (isVisible(header)) {
        history.replaceState(null, null, ' ');
        current_slide = 0;
        return;
    }

    for (let section of sections) {
        if (isVisible(section)) {
            let anchor = "#" + section.id;
            history.replaceState(null, null, anchor);
            current_slide = find_slide(slide_anchors, anchor);
            break;
        }
    }
}

function isVisible(obj) {
    let rect = obj.getBoundingClientRect();
    return (rect.top >= 0 && rect.top < window.innerHeight / 2);
}

function go_to_last_slide() {
    go_to_slide(slide_anchors.length - 1);
}

function go_to_slide(n) {
    current_slide = n;

    if (current_slide < 0) {
        current_slide = 0;
    } else if (current_slide >= slide_anchors.length) {
        current_slide = slide_anchors.length - 1;
    }

    if (current_slide === 0) {
        if (header) {
            header.scrollIntoView();
        }
        window.scrollTo(0, 0);
        history.replaceState(null, null, ' ');
    } else {
        window.location.hash = slide_anchors[current_slide];
    }
}

function find_slide(slide_anchors, anchor) {
    let ret = slide_anchors.indexOf(anchor);
    if (ret === -1) {
        ret = 0;
    }
    return ret;
}

function scan_slides() {
    let ret = [""];

    for (let section of sections) {
        ret.push(find_anchor(section));
    }

    return ret;
}

function find_anchor(section) {
    if (section.id === "") {
        fail("This section does not have an id='blah' attribute!:", section);
    }
    return "#" + section.id;
}

function fail(msg, obj) {
    console.error(`htmlslides error: ${msg}`);
    if (obj) {
        console.error(obj);
    }
}

window.addEventListener("load", on_load);

}());
