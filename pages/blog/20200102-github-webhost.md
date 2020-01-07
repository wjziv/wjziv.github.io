title: Website Hosting on Github
date: 2020-01-02
hero:
description: Utilize Github's offer to host a website for you for free!
tags:
    - How-to
    - Github
    - Flask
    - Beginner

See the finished project on [Github]().

#### Introduction

[Github Pages](https://pages.github.com/) allows you to host your own static personal and project pages on their website for absolutely free, so long as you do the heavy-lifting and bake your pages all together. It isn't too difficult to get started, and there's already a well-known project called [Jekyll](https://jekyllrb.com/docs/github-pages/) which allows you to do exactly that. Github even features clear [instructions](https://help.github.com/en/github/working-with-github-pages/setting-up-a-github-pages-site-with-jekyll) on how to get your own page up and running within their help docs.

While Jekyll was nice and convenient, I'm primarily a Python developer, and I'd prefer to approach the problem with tools I was more comfortable with and expand my understanding of them with a new challenge.

#### Python Tools

I chose to utilize [Flask](http://flask.palletsprojects.com/en/1.1.x/) for its simplicity in URI routing and Jinja templating, [Flask-Flatpages](https://pythonhosted.org/Flask-FlatPages/) so I may take advantage of Markdown syntax and use .md files for the majority of my pages, and [Frozen-Flask](https://pythonhosted.org/Frozen-Flask/) to build my website into a directory of static HTML files which Github Pages can handle appropriately--this is to say, there is no need for an active server once the webpage has been frozen.

#### Beginning with Flask

Start off creating a Flask App. Open up your preferred IDE and create the following files:

```text
my_website/
- requirements.txt
- run.py
```

Inside of `requirements.txt`:
```text
Flask==1.1.1
Flask-Flatpages==0.7.1
Frozen-Flask==0.15
```

Inside of `run.py`:
```python
from flask import Flask
import sys
import os

app = Flask(__name__)

@app.route('/')
def index(path):
    return 'Hello World!'

if __name__ == '__main__':
    app.run(port=8000)
```

Head to your terminal, navigate to the directory where you've saved `run.py` and install `requirements.txt` to your preferred environment. Then enter `python run.py`. It'll be followed with a few lines that look like this:

```bash
(my_website) walterzielenski@penguin:~/dev/wjziv/my_website$ python run.py
 * Serving Flask app "run" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)
```

Follow [http://127.0.0.1:8000](http://127.0.0.1:8000) to see your website in all of its glory!

If you'd like to add an alternative page, add another endpoint in `run.py`:
```python
from flask import Flask
import sys
import os

app = Flask(__name__)

@app.route('/')
def index(path):
    return 'Hello World!'

@app.route('/hello')
def index(path):
    return 'My Second Page!'

if __name__ == '__main__':
    app.run(port=8000)
```

View this one at [http://127.0.0.1:8000/hello](http://127.0.0.1:8000/hello)

Flask has a whole lot more to offer than returning words in a browser when you go to a pre-designed URL, but this nearly all that'll be necessary to complete this project. I encourage the reader to learn more about Flask on their own later on.

#### Beginning with Flask-Flatpages

We're going to begin expanding on our simple website by rendering some templates. Make a new folder and file such that your directory looks like this:

```text
my_website/
- requirements.txt
- run.py
  pages/
  - blog_post_1.md
  templates/
  - base.html
  - post.html
```

Inside of `blog_post_1.md` (This will be the contents within one of our pages.):
```markdown
title: My First Blog Post
date: 2020-01-02

This is the **first** blog post of *many*!
```

Inside of `base.html` (This will be the skeleton for all kinds of content we'll be putting on the website. The `block` part is a modular component which can receive contents from other HTML files. We'll see this soon.):
```html
{% raw %}
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>My Blog</title>
</head>

<body>
    <h1><a href="{{ url_for('index') }}">My Blog</a></h1>

    <div>
        {% block content %}
        <p>If you see this, this is the main page default stuff.</p>
        {% endblock content %}
    </div>
</body>
</html>
{% endraw %}
```

Inside of `post.html` (This will be the skeleton for any and all blog posts we have.):

```html
{% raw %}
{% extends "base.html" %}
{% block content %}
    <h2>
        {{ page.title }}
    </h2>
    {{ page|safe }}
{% endblock content %}
{% endraw %}
```

##### Navigating Jinja
The items within curly brackets in the HTML files are part of the Jinja templating language. When we follow the templating logic as though we are trying to render `post.html`...

{% raw %}
1. `{% extends "base.html" %}` tells the script where to insert this content.
2. `{% block content %} ... {% endblock content %}` outlines the extent of the content to be inserted, along with what the name of the insertion zone is (`content`, in this case).
3. `{{ page.title }}` (where `page` is the variable name for the markdown content file) is some meta data contained within a markdown file; in this case, it's the `title` within that file.
    See `blog_post_1.md` to refresh your memory on how we know this value exists.
4. `{{ page|safe }}` retreives the rest of the content from the markdown file, where `page` refers to the same thing as above. `|safe` tells Jinja that it is safe to refrain from auto-escaping the characters within the file.
5. Finally, within `base.html`, `{% block content %} ... {% endblock content %}` outlines the location to drop the new content. Anything that exists in between those statements is default content, and it will be overwritten.
{% endraw %}

The next question is "How does Flask-Flatpages and jinja know what `page` is?!"

##### Finishing Flask-Flatpages
Crack open `run.py` and let's edit it again.
```python
from flask_flatpages import FlatPages # Refer to the FlatPages library
from flask import Flask, render_template # include render_template
import sys
import os

DEBUG = True # Run Flask in Debug Mode; apply changes on-the-fly.
FLATPAGES_AUTO_RELOAD = DEBUG # Run Flask in Debug mode.
FLATPAGES_EXTENSION = '.md' # Seek out `.md` files within the `pages` folder.

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)

@app.route('/')
def index(path):
    return 'Hello World!'

@app.route('/hello')
def index(path):
    return 'My Second Page!'

@app.route("/<path:path>/") # route to ambiguous paths
def page(path):
    page = pages.get_or_404(path) # retreive our desired page at an arbitrary path (if it exists)
    return render_template("page.html", page=page) # Return the page, rendered from markdown to HTML.

if __name__ == '__main__':
    app.run(port=8000)
```

Our answer to this question lies at the bottom of this file. For example: the URI for our page `my_blog_post_1.md` exists at `/my_blog_post_1`. If our website is running, all that needs to happen is for somebody to navigate to [http://127.0.0.1:8000/my_blog_post_1](http://127.0.0.1:8000/my_blog_post_1). Go to your terminal, re-run `run.py`, and navigate there now.

Tada! You have a working templating engine running on your website. You can fill that `pages` directory with as many markdown files as you like. Each on will render into HTML as you expect it to.

The next question: "How does a visitor to my website know how to get to all of my content?"

##### Advanced Jinja

There are plenty of properties that go along with [Jinja](https://jinja.palletsprojects.com/en/2.10.x/), but we'll only go over for-loops here. You can find our all about conditionals, exposing Python functions to your templates, creating variables, and more on your own.

Let's flesh out the home page such that there's a list of all of our blog posts. Make a new template file, `index.html`:

```text
my_website/
- requirements.txt
- run.py
  pages/
  - blog_post_1.md
  templates/
  - base.html
  - post.html
  - index.html
```

Inside the `index.html` file:
```html
{% raw %}
{% extends "base.html" %}
{% block content %}
    {% for blog in blog_posts %}
    <a href="{{ url_for('page', path=blog.path) }}">
    <h2>
        {{ blog.title }}
    </h2>
    </a>
    {% endfor %}
{% endblock content %}
{% endraw %}
```
A few notes:

{% raw %}
1. As with `page.html`, we start with `{% extends "base.html" %}` and contain our HTML code with `{% block content %}...{% endblock content %}`.
2. The for-loop has a declarative stop, at `{% endfor %}`.
3. Lastly, while we've seen this before, we hadn't touched upon it: the `href` value is a variable contained within quotes; keep in mind that Jinja will still work when inside these quotes, and they are necessary for HTML rendering down the road. The `url_for()` function within is built into Jinja; the contents are fed back to `run.py`. This function will vicariously execute `page()` using kwarg `path=blog.path`, where blog is an arbitrary markdown folder within the `pages/` folder.

Last question: "How does Jinja know what the `blog_posts` are?" We still need to feed that information through.
{% endraw %}

```python
from flask_flatpages import FlatPages
from flask import Flask, render_template
import sys
import os

DEBUG = True 
FLATPAGES_AUTO_RELOAD = DEBUG 
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)

@app.route('/')
def index(path):
    return render_template("index.html", blog_posts=pages) # Supply the `blog_posts` variable in the render_template command.

@app.route('/hello')
def index(path):
    return 'My Second Page!'

@app.route("/<path:path>/")
def page(path):
    page = pages.get_or_404(path)
    return render_template("page.html", page=page) 

if __name__ == '__main__':
    app.run(port=8000)
```

Finally, since you're already running your website in debug mode, head to your home page at  [http://127.0.0.1:8000](http://127.0.0.1:8000), or refresh the page if you're already there. You should see links to your blog post pages, right at the front!

#### Frozen-Flask

Now that we have a website made, it's time to freeze it into a set of static HTML pages to post to Github. We'll edit the `run.py` file one more time.

```python
from flask_frozen import Freezer # New
from flask_flatpages import FlatPages
from flask import Flask, render_template
import sys
import os

DEBUG = True 
FLATPAGES_AUTO_RELOAD = DEBUG 
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app) # New

@app.route('/')
def index(path):
    return render_template("index.html", blog_posts=pages)

@app.route('/hello')
def index(path):
    return 'My Second Page!'

@app.route("/<path:path>/")
def page(path):
    page = pages.get_or_404(path)
    return render_template("page.html", page=page) 

if __name__ == "__main__":
    if "freeze" in sys.argv: # New
        freezer.freeze() # New
    else: # New
        app.run(port=8000)
```

Adding these few elements from Frozen-Flask allows us to create the static HTML pages we'd like to push to Github. Freeze your web app by heading to your terminal and typing `python run.py freeze`.

A new folder called `build/` will appear in your directory:

```text
my_website/
- requirements.txt
- run.py
  pages/
  - blog_post_1.md
  templates/
  - base.html
  - post.html
  - index.html
  build/
  - index.html
    blog_post_1/
    - index.html
```

#### Hosting on Github


#### Other Concerns

##### Custom Domain

##### Using Flask Extensions

##### Exposing Python Functions to Jinja