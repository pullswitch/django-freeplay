django-freeplay
===============

Freeplay is a unique approach to easily add CMS functionality to
your Django app. Define regions for managing (and allowing clients to manage) 
bits of content on your site that don't need the full build-out of 
custom apps. For example, that list of links in the footer, or the photo 
and bio of the CEO. With Freeplay, each region can contain one or many 
items, so you quickly gain flexible model-like functionality.

Each bit of content gets rendered onsave with Django's template 
processor, so you have all the power of the Django's parser.


Installation
============

1. ``pip install django-freeplay``
2. Add ``'freeplay'`` and ``'relatedwidget'`` to your ``INSTALLED_APPS``
    in your project's settings.py
3. Add ``(r"^admin/content/", include("freeplay.urls_admin")),`` to 
   your main urls.py, before you include the admin urls
4. Sync your db or use your migration tool of choice 
   (recommended: `nashvegas`_)

.. _`nashvegas`: https://github.com/paltman/nashvegas


Requirements
============

Installing freeplay will also bring 
`django-model-utils`_, `django-imagekit`_, 
and `django-relatedadminwidget`_ with it.

The admin templates assume the existence of a few CSS and JS libraries: 
`Chosen`_, `Masonry`_, and `jQuery.Slugify`_. Place
the files here (in relation to your staticfiles directory) to "just make it
work":

- chosen_v1.0.0/chosen.jquery.min.js
- masonry/jquery.masonry.min.js
- jquery-slugify/dist/slugify.min.js

Note: All three of these can be installed quickly using `bower`_. Add
`django-bower`_ to your project if you haven't yet!

These paths can also be overridden with a `FREEPLAY` setting in your settings
file:

.. code-block:: python

    FREEPLAY = {
        "CHOSEN_PATH": "some/path/chosen.js",
        "SLUGIFY_PATH": "some/path/slugify.js",
        "MASONRY_PATH": "some/path/masonry.js"
    }

And for more advanced customization, you can always override the freeplay
templates with your own.

.. _`django-model-utils`: https://github.com/carljm/django-model-utils
.. _`django-imagekit`: https://github.com/jdriscoll/django-imagekit
.. _`django-relatedadminwidget`: https://github.com/benjaoming/django-relatedadminwidget
.. _`Chosen`: https://github.com/harvesthq/chosen/
.. _`Masonry`: http://masonry.desandro.com
.. _`jQuery.Slugify`: https://github.com/pmcelhaney/jQuery-Slugify-Plugin
.. _`bower`: http://bower.io/
.. _`django-bower`: https://github.com/nvbn/django-bower

Usage
=====

In the django admin, create a new freeplay **Template**. Start by defining the 
template **bits** and then write the template **code**. For example, let's say we want to 
manage a few FAQs. We'd create one bit like so:

| Kind: Plain Text  
| Name: Question  
| Context name: question  
| Order: 1  
| Text Widget: Textarea Input Field  
| Required: True  

And another:

| Kind: Markdown  
| Name: Answer  
| Context name: answer  
| Order: 2  
| Text Widget: Textarea Input Field  
| Required: True

(Note: if you use Markdown, be sure you've added ``markdown`` to your 
requirements)

When you set up the bits for a template, you're defining the form that you 
or your clients will use to add and edit content for items that use this 
template. As such, you can include help text with each bit.

Now we can write the following for the template Code:

.. code-block:: html

    <span class="number">{{ order }}</span>
    {{ question|title }}
    <div class="answer">{{ answer|safe }}</div>

Note we need to use the ``safe`` filter for HTML content, and also that each 
item will include its "order" in context as well as "label".

As soon as you have a template, create a **Region** and then you can start adding 
content, which is easily done using the included admin urls and templates.

Templatetags
------------

Here's how you fetch and display freeplay content in your templates:

.. code-block:: html

    {% load freeplay_tags %}


``content_bits`` : assignment tag, accepts "region_slug" as argument

.. code-block:: html
    
    {% content_bits "question-answer" as qa_items %}
    {% for item in qa_items %}
    <li>{{ item.data|safe }}</li>
    {% endfor %}

``get_bit`` : assignment tag, requires "region_slug" and, optionally, "item_slug" 

.. code-block:: html

    {% get_bit "site_constants" "footer-company-summary" as co_summary %}
    <footer>
        <h1>About the Company</h1>
        <p>{{ co_summary.data }}</p>
    </footer>

.. code-block:: html

    {% get_bit "footer-address" as address %}
    <footer>
        <h1>Come Visit!</h1>
        <p>{{ address.data }}</p>
    </footer>

Images
-------

Image bits can be rendered in your template using `{{ item }}` (if the context
name for this bit is "item". Thisenerates the `<img>` tag including an `alt`
attribute. If you just want to get the image path, you can either use
`{{ item.contentbit.image_url }}` or `{{ item_url }}`.


Also
====

Freeplay regions let you set "Min Items" and "Max Items", optionally. On the 
freeplay admin dashboard, it will then alert you if a region needs more content 
to meet the minimum requirement and won't show the "Add" link if the region has 
met the maximum limit.

Image constraints should be entered as width followed by height, separated with "x": 150x80

To display an image in your template, something like this will work:

.. code-block:: html

    <img src="{{ headshot.image_path }}" alt="Headshot">

Or...

.. code-block:: html

    {{ headshot.markup }}

Hope you find this useful!




