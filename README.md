django-tidbits
==============

Tidbits is a Django app for managing (and allowing clients to manage) bits of content on your site that don't need the full build-out of custom apps. For example, that short company description in the site footer or the photo and bio of the CEO.

Tidbits aims to be as simple or powerful as you need, so it uses a template approach for each area you setup and renders them with Django's template processor.


Installation
============

1. `pip install django-tidbits`
2. Add `'tidbits'` to your `INSTALLED_APPS` in your project's settings.py
3. (Optional) Add `(r"^admin/bits/", include("tidbits.urls_admin")),` to your main urls.py, before you include the admin urls
4. Sync your db or use your migration tool of choice (recommended: nashvegas)


Requirements
============

Installing tidbits will also bring django-model-utils, django-imagekit, and django-relatedadminwidget with it. Hopefully these aren't deal-killers for you, as each is extremely useful.

The admin templates assume the existence of a few CSS and JS libraries: Chosen, Isotope, and jQuery.Slugify. Simply override the templates with ones in your project to define your own paths or libs.


Usage
=====

In the django admin, create a new tidbits template. Start by defining the bits and then write the template code. For example, let's say we want to manage a few FAQs. We'd create one bit like so:

Kind: Plain Text
Name: Question
Context name: question
Order: 1
Text Widget: Textarea Input Field
Required: True

And another:

Kind: Markdown
Name: Answer
Context name: answer
Order: 2
Text Widget: Textarea Input Field
Required: True

(Note: if you use Markdown, be sure you've added markdown to your requirements)

When you set up the bits for a template, you're defining the form that you or your clients will use to add and edit content for items that use this template. As such, you can include help text with each bit.

Now we can write the following for our template Code:

.. code-block:: html

    <span class="number">{{ order }}</span>
    {{ question|titlecase }}
    <div class="answer">{{ answer|safe }}</div>

Note we need to use the `safe` filter for HTML content, and also that each item will include its `order` in context as well as `label`.

As soon as you have a template, create an Area and then you can start adding content, which is easily done using the included admin urls and templates.

Templatetags
------------

Two template tags are included to fetch bits for display in your templates:

.. code-block:: html

    {% load tidbits_tags %}


`content_bits` : assignment tag, accepts `area_slug` as argument

.. code-block:: html
    
    {% content_bits "question-answer" as qa_items %}
    {% for item in qa_items %}
    <li>{{ item.data|safe }}</li>

`get_bit` : assignment tag, requires `area_slug` and `item_slug` as args

.. code-block:: html

    {% get_bit "site_constants" "footer-company-summary" as co_summary %}
    <footer>
        <h1>About the Company</h1>
        <p>{{ co_summary.data }}</p>
    </footer>


Also
====

Tidbit areas let you set "Min Items" and "Max Items", optionally. On the tidbits dashboard, it will then alert you if an area needs more content to meet the minimum requirement and won't show the "Add" link if an area has met the maximum limit.




