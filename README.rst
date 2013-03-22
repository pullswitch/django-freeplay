django-freeplay
===============

Freeplay is a new approach for easily adding CMS functionality to
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
2. Add ``'freeplay'`` to your ``INSTALLED_APPS`` in your project's settings.py
3. (Optional) Add ``(r"^admin/freeplay/", include("freeplay.urls_admin")),`` to 
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
`Chosen`_, `Isotope`_, and `jQuery.Slugify`_. Simply override the 
templates with ones in your project to define your own paths or libs.

.. _`django-model-utils`: https://github.com/carljm/django-model-utils
.. _`django-imagekit`: https://github.com/jdriscoll/django-imagekit
.. _`django-relatedadminwidget`: https://github.com/benjaoming/django-relatedadminwidget
.. _`Chosen`: https://github.com/harvesthq/chosen/
.. _`Isotope`: https://github.com/desandro/isotope
.. _`jQuery.Slugify`: https://github.com/pmcelhaney/jQuery-Slugify-Plugin

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

``get_bit`` : assignment tag, requires "region_slug" and "item_slug" as args

.. code-block:: html

    {% get_bit "site_constants" "footer-company-summary" as co_summary %}
    <footer>
        <h1>About the Company</h1>
        <p>{{ co_summary.data }}</p>
    </footer>


Also
====

Freeplay regions let you set "Min Items" and "Max Items", optionally. On the 
freeplay admin dashboard, it will then alert you if a region needs more content 
to meet the minimum requirement and won't show the "Add" link if the region has 
met the maximum limit.

Hope you find this useful!




