---
source: "https://www.geeksforgeeks.org/how-to-animate-css-grid/"
title: "How To Animate CSS Grid? - GeeksforGeeks"
fetched_at: "2026-10-06 12:34"
---

# How To Animate CSS Grid?

Last Updated : 8 Oct, 2024

  *   *   * 


CSS Grid is a powerful layout system built in CSS that can easily create complex and responsive web layouts, it defines a 2D layout system that can precisely control rows and columns, you can place elements within this grid by specifying their positions in rows and columns, unlike Flexbox, which is 1-dimensional (works on a single axis).

These are the Following methods through which we can animate CSS Grid:

Table of Content

  * Animating Individual Grid Items with transform
  * Animating Grid Template Areas
  * Animating Grid Track Sizes
  * Animating Grid Item Position 



## ****Animating Individual Grid Items with******`**transform**`**

The easiest way is to animate individual grid objects by changing their position, size, **`**rows**`** or rotation, this does not change the grid layout but it allows adding dynamic effects to elements within the grid.

****Example:**** In this example, we will be animating individual grid items with a transform.

HTML `
    
    
    /* index.html */
    
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content=
    "width=device-width, initial-scale=1.0">
        <title>GeeksforGeeks Grid Animation</title>
        <link rel="stylesheet" href="style.css">
    </head>
    
    <body>
        <div class="container">
            <h1>GeeksforGeeks</h1>
            <h2>Approach 1) Animating Individual Grid Items with transform</h2>
            <div class="grid-container">
                <div class="grid-item">1</div>
                <div class="grid-item">2</div>
                <div class="grid-item">3</div>
                <div class="grid-item">4</div>
                <div class="grid-item">5</div>
                <div class="grid-item">6</div>
            </div>
        </div>
    </body>
    
    </html>
    

` CSS `
    
    
    /* style.css */
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: Arial, sans-serif;
    }
    
    body {
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f4f4f4;
    }
    
    .container {
        text-align: center;
    }
    
    h1 {
        color: #197b43;
        margin-bottom: 10px;
        font-size: 2.5rem;
    }
    
    h2 {
        color: #000000;
        margin-bottom: 20px;
        font-size: 1.5rem;
    }
    
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        padding: 40px;
        border: 5px solid #197b43;
        border-radius: 10px;
        background-color: white;
    }
    
    .grid-item {
        background-color: #197b43;
        padding: 40px;
        color: white;
        text-align: center;
        font-size: 1.5rem;
        transition: transform 0.5s ease-in-out;
        border-radius: 5px;
    }
    
    .grid-item:hover {
        transform: scale(1) rotate(15deg);
    }
    

`

****Output:****

## ****Animating Grid Template Areas****

This method allows you to change between different web template areas and animate the entire web layout, this allows you to create the effect of configuration changes without changing the HTML structure.

****Example:**** In this example, we will animate grid template areas.

HTML `
    
    
    /* index.html */
    
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content=
    "width=device-width, initial-scale=1.0">
        <title>GeeksforGeeks Grid Template Areas Animation</title>
        <link rel="stylesheet" href="style.css">
    </head>
    
    <body>
        <div class="container">
            <h1>GeeksforGeeks</h1>
            <h2>Approach 2) Animating Grid Template Areas</h2>
            <div class="grid-container">
                <div class="header">Header</div>
                <div class="sidebar">Sidebar</div>
                <div class="main">Main Content</div>
                <div class="footer">Footer</div>
            </div>
            <button id="toggle-layout">Toggle Layout</button>
        </div>
    
        <script src="index.js"></script>
    </body>
    
    </html>
    

` CSS `
    
    
    /* style.css */
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: Arial, sans-serif;
    }
    
    body {
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f4f4f4;
    }
    
    .container {
        text-align: center;
    }
    
    h1 {
        color: #197b43;
        margin-bottom: 10px;
        font-size: 2.5rem;
    }
    
    h2 {
        color: #000000;
        margin-bottom: 20px;
        font-size: 1.5rem;
    }
    
    .grid-container {
        display: grid;
        grid-template-areas:
            "header header"
            "sidebar main"
            "footer footer";
        grid-template-columns: 1fr 2fr;
        gap: 15px;
        padding: 20px;
        border: 5px solid #197b43;
        border-radius: 10px;
        background-color: white;
        transition: grid-template-areas 0.5s ease;
    }
    
    .header {
        grid-area: header;
        background-color: #4CAF50;
        color: white;
        padding: 20px;
    }
    
    .sidebar {
        grid-area: sidebar;
        background-color: #87cefa;
        color: white;
        padding: 20px;
    }
    
    .main {
        grid-area: main;
        background-color: #32cd32;
        color: white;
        padding: 20px;
    }
    
    .footer {
        grid-area: footer;
        background-color: #ffa500;
        color: white;
        padding: 20px;
    }
    
    .grid-container.active {
        grid-template-areas:
            "header header"
            "main sidebar"
            "footer footer";
    }
    
    button {
        margin-top: 20px;
        padding: 10px 20px;
        background-color: #10d566;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
    }
    
    button:hover {
        background-color: #388e3c;
    }
    

` JavaScript `
    
    
    document.getElementById('toggle-layout').addEventListener('click', function() {
        document.querySelector('.grid-container').classList.toggle('active');
      });
      
    

`

****Output:****

## ****Animating Grid Track Sizes****

The alteration of grid track size animation can help to implement the sensitive resizing of columns or rows, this is helpful in responsive or interactive designs where some space expands or contracts based on user action.

****Example:**** In this example, we will animate grid track sizes.

HTML `
    
    
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content=
    "width=device-width, initial-scale=1.0">
        <title>GeeksforGeeks Grid Track Sizes Animation</title>
        <link rel="stylesheet" href="style.css">
    </head>
    
    <body>
        <div class="container">
            <h1>GeeksforGeeks</h1>
            <h2>Approach 3) Animating Grid Track Sizes</h2>
            <div class="grid-container">
                <div class="grid-item">1</div>
                <div class="grid-item">2</div>
                <div class="grid-item">3</div>
            </div>
            <button id="resize-grid">Resize Grid</button>
        </div>
    
        <script src="index.js"></script>
    </body>
    
    </html>
    

` CSS `
    
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: Arial, sans-serif;
    }
    
    body {
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f4f4f4;
    }
    
    .container {
        text-align: center;
    }
    
    h1 {
        color: #197b43;
        margin-bottom: 10px;
        font-size: 2.5rem;
    }
    
    h2 {
        color: #000000;
        margin-bottom: 20px;
        font-size: 1.5rem;
    }
    
    .grid-container {
        display: grid;
        grid-template-columns: 1fr 2fr 1fr;
        gap: 15px;
        padding: 20px;
        border: 5px solid #197b43;
        border-radius: 10px;
        background-color: white;
        transition: grid-template-columns 1s ease-in-out;
    }
    
    .grid-item {
        background-color: #197b43;
        padding: 40px;
        color: white;
        text-align: center;
        font-size: 1.5rem;
        border-radius: 5px;
    }
    
    button {
        margin-top: 20px;
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
    }
    
    button:hover {
        background-color: #197b43;
    }
    
    .grid-container.resized {
        grid-template-columns: 2fr 1fr 2fr;
    }
    

` JavaScript `
    
    
    document.getElementById('resize-grid').addEventListener('click', function() {
        document.querySelector('.grid-container').classList.toggle('resized');
      });
      
    

`

****Output:****

## ****Animating Grid Item Position****

This approach allows you to animate the position of individual grid items by transitioning their `grid-column` and `grid-row` values. It can create a visual effect of moving elements within the grid, such as reordering items or shifting them to different sections.

****Example:**** In this example, we will animate grid item position using grid-column and grid-row.

HTML `
    
    
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content=
    "width=device-width, initial-scale=1.0">
        <title>GeeksforGeeks Grid Item Position Animation</title>
        <link rel="stylesheet" href="style.css">
    </head>
    
    <body>
        <div class="container">
            <h1>GeeksforGeeks</h1>
            <h2>Approach 4) Animating Grid Item Position Using grid-column and grid-row</h2>
            <div class="grid-container">
                <div class="grid-item item-1">1</div>
                <div class="grid-item item-2">2</div>
                <div class="grid-item item-3">3</div>
                <div class="grid-item item-4">4</div>
            </div>
            <button id="reposition-grid">Reposition Items</button>
        </div>
    
        <script src="index.js"></script>
    </body>
    
    </html>
    

` CSS `
    
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: Arial, sans-serif;
    }
    
    body {
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f4f4f4;
    }
    
    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    h1 {
        color: #197b43;
        margin-bottom: 10px;
        font-size: 2.5rem;
    }
    
    h2 {
        color: #020202;
        margin-bottom: 20px;
        font-size: 1.5rem;
    }
    
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        /* Use auto-fit to dynamically adjust the column width */
        gap: 15px;
        padding: 20px;
        border: 5px solid #197b43;
        border-radius: 10px;
        background-color: white;
        transition: grid-column 1s ease, grid-row 1s ease;
        width: 100%;
        /* Set width to 100% to prevent overflow */
        max-width: 500px;
        /* Add a maximum width if needed */
    }
    
    .grid-item {
        background-color: #197b43;
        padding: 40px;
        color: white;
        text-align: center;
        font-size: 1.5rem;
        border-radius: 5px;
    }
    
    .item-1 {
        grid-column: 1;
        grid-row: 1;
    }
    
    .item-2 {
        grid-column: 2;
        grid-row: 1;
    }
    
    .item-3 {
        grid-column: 3;
        grid-row: 1;
    }
    
    .item-4 {
        grid-column: 1;
        grid-row: 2;
    }
    
    .grid-container.repositioned .item-1 {
        grid-column: 2;
        grid-row: 2;
    }
    
    .grid-container.repositioned .item-2 {
        grid-column: 3;
        grid-row: 1;
    }
    
    .grid-container.repositioned .item-3 {
        grid-column: 1;
        grid-row: 1;
    }
    
    .grid-container.repositioned .item-4 {
        grid-column: 2;
        grid-row: 1;
    }
    
    button {
        margin-top: 20px;
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
    }
    
    button:hover {
        background-color: #197b43;
    }
    

` JavaScript `
    
    
    document.getElementById('reposition-grid').addEventListener('click', function() {
        document.querySelector('.grid-container').classList.toggle('repositioned');
      });
    

`

****Output:****

Comment

### Explore

CSS Basics __

    * [Introduction __2 min read](https://www.geeksforgeeks.org/css/css-introduction/)
    * [Syntax __2 min read](https://www.geeksforgeeks.org/css/css-syntax/)
    * [Combinators __2 min read](https://www.geeksforgeeks.org/css/css-combinators/)
    * [Selectors __6 min read](https://www.geeksforgeeks.org/css/css-selectors/)
    * [Comments __2 min read](https://www.geeksforgeeks.org/css/css-comments/)

Styling & Properties __

    * [Colors __5 min read](https://www.geeksforgeeks.org/css/css-colors/)
    * [Bckground __4 min read](https://www.geeksforgeeks.org/css/css-background/)
    * [Borders __5 min read](https://www.geeksforgeeks.org/css/css-borders/)
    * [Margins Padding __3 min read](https://www.geeksforgeeks.org/css/css-margins-padding/)
    * [Padding __6 min read](https://www.geeksforgeeks.org/css/css-padding/)
    * [Overflow __4 min read](https://www.geeksforgeeks.org/css/css-overflow/)
    * [Height & Width __4 min read](https://www.geeksforgeeks.org/css/css-height-and-width/)

Text & Fonts __

    * [Text Formatting __8 min read](https://www.geeksforgeeks.org/css/css-text-formatting/)
    * [Fonts __4 min read](https://www.geeksforgeeks.org/css/css-fonts/)
    * [Text Align Property __3 min read](https://www.geeksforgeeks.org/css/css-text-align-property/)
    * [Text Decoration Property __3 min read](https://www.geeksforgeeks.org/css/css-text-decoration-property/)

Layouts & Design __

    * [Box Model __7 min read](https://www.geeksforgeeks.org/css/css-box-model/)
    * [Display Property __3 min read](https://www.geeksforgeeks.org/css/css-display-property/)
    * [Float and Clear __4 min read](https://www.geeksforgeeks.org/css/css-layout-float-and-clear/)
    * [Overflow Property __2 min read](https://www.geeksforgeeks.org/css/css-overflow-property/)
    * [Index Property __4 min read](https://www.geeksforgeeks.org/css/css-z-index-property/)

Modern Layout Systems __

    * [Flexbox __3 min read](https://www.geeksforgeeks.org/css/introduction-to-css-flexbox/)
    * [Content Property __6 min read](https://www.geeksforgeeks.org/css/css-justify-content-property/)
    * [Align Items Property __7 min read](https://www.geeksforgeeks.org/css/css-align-items-property/)
    * [Align Content Property __4 min read](https://www.geeksforgeeks.org/css/css-align-content-property/)
    * [Grid Layout __5 min read](https://www.geeksforgeeks.org/css/css-grid-layout-module/)
    * [Grid Template Columns Property __4 min read](https://www.geeksforgeeks.org/css/css-grid-template-columns-property/)
    * [Grid Gap Property __2 min read](https://www.geeksforgeeks.org/css/css-grid-gap-property/)

Effects, Animations & Advanced CSS __

    * [Transitions __4 min read](https://www.geeksforgeeks.org/css/css-transitions/)
    * [Transform Property __8 min read](https://www.geeksforgeeks.org/css/css-transform-property/)
    * [Animations __6 min read](https://www.geeksforgeeks.org/css/css-animations/)
    * [Box Shadow Property __6 min read](https://www.geeksforgeeks.org/css/css-box-shadow-property/)
    * [Text Shadow Property __2 min read](https://www.geeksforgeeks.org/css/css-text-shadow-property/)
    * [Specificity __3 min read](https://www.geeksforgeeks.org/css/css-specificity/)
    * [Variables __2 min read](https://www.geeksforgeeks.org/css/css-variables/)
    * [Pseudo Classes __6 min read](https://www.geeksforgeeks.org/css/css-pseudo-classes/)
    * [Pseudo Elements __4 min read](https://www.geeksforgeeks.org/css/css-pseudo-elements/)

Courses __

    * [MERN Full Stack Course __2 min read](https://www.geeksforgeeks.org/courses/full-stack-node)



