# Customize

Sphinx theme is customizable. 


## Variables

**`html_title`**: set title of the document. 

**`html_logo`**: set logo image. Set relative path to image from the current document.

**`html_permalinks_icon`**: change permalink symbol from ¶


## Variables (theme specific)

**`mochi_navtree_titlesonly`**: If True, only the first heading is included in the sidebar navtree. Defaults to False.

**`mochi_navtree_maxdepth`**: Specifies the maxdepth of navtree. Defaults to -1 (unlimited)



Note: The navtree source is limited by your `.toctree::` declaration. If you specify some attributes like `:titlesonly:` or `:maxdepth:N` in your reST, the dropped headers are not included in the navtree, regardless of your theme-options.