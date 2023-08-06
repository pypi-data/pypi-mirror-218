# Theme Requirements

Guidelines for future development

## Layout

-- The theme must have 3 columns, when the width is wide enough.

-- The theme must show 2 columns, when the width is shorter

-- For mobile, the theme must show 1 columns, and it must be navigatable

-- The theme should provide good document readability in any circumstances.

## Customization 1

-- The theme should use the sphinx-defined basic configuration options, as listed in this link:   
[https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output](https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output)


Some important options

| config key                |     explanation    |
|---------------------------|--------------------|
|  `html_theme_options`     |  dictionary for theme-specific options.|
|  `html_theme_path`        |  this theme cannot be loaded with this option, since initialization script will not run.|
|  `html_title`             |  the title for HTML documentation. Defaults to '&lt;project>v&lt;revision> documentation'|
|  `html_short_title`       |  a shorter title . If not given, defaults to `html_title`|
|  `html_baseurl`           |  base url which points to the root of HTML documentation. Defaults to ''|
|  `html_logo`              |  path (or URL) to the image file. path is relative to config dir. good to use `_static` as Sphinx copies the image file to the _static directory if not exists |
|  `html_favicon`           |  path (or URL) to the favicon file. |
|  `html_css_files`         |  |
|  `html_js_files`          |  |

