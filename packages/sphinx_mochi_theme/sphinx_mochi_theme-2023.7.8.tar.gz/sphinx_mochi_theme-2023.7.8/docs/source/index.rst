======================
sphinx-mochi-theme
======================

About
===========

This is a developer's documentation for simple sphinx theme named "sphinx-mochi-theme".

To read how to setup, check this page: :doc:`doc/setup`

For requirements when developing this theme, check this page: :doc:`doc/req`


..  toctree::
    :maxdepth: 2
    :caption: Index
    :numbered:

    doc/setup
    doc/customize
    doc/req

Sample
==========

Tree pages (:doc:`doc/sample/tree/page1`) constructs nested navtree. 

The :doc:`doc/sample/kitchen-sink/index` section contains pages that contains basically
everything that you can with Sphinx "out-of-the-box".

..  toctree::
    :titlesonly:
    :caption: Sample Pages

    doc/sample/tree/page1
    doc/sample/tree/page2
    doc/sample/kitchen-sink/index
    doc/sample/page/placeholder-one
    doc/sample/page/placeholder-two
    doc/sample/page/really-long-title
    doc/sample/page/long-page
    doc/sample/page/japanese
    External Link <https://www.sphinx-doc.org>

.. toctree::
    :hidden:
    :caption: Additional "hidden" Pages

    doc/sample/page/placeholder-three
    doc/sample/page/placeholder-four
    Sphinx Theme Gallery <https://sphinx-themes.org>
