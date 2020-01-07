import sys, os
import yaml
from flask import Flask, render_template, make_response, render_template_string
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import markdown

# Retreive website-specific data.
## This includes site-name, author, social media accounts, etc...
with open('config.yaml') as f:
    config = yaml.safe_load(f)
html_basics = ['author','site_title','description','keywords','favicon']
basics = {k:v for k,v in config.items() if k in html_basics}

contentwalk = [x for x in os.walk('pages')][0]
DIRECTORIES = [x.lower() for x in contentwalk[1]]
STAND_ALONE = [x.split('.')[0] for x in contentwalk[2] if x.split('.')[0].lower() not in DIRECTORIES]
SOCIAL = config['social']
basics = {**basics, 
          'directories': DIRECTORIES, 
          'stand_alone': STAND_ALONE,
          'social': SOCIAL}

# Flask Configuration.
## Tell Flask how to render the site properly.
extensions = ['codehilite','fenced_code','tables','def_list']
def renderer(text):
    """Inject the markdown rendering into the jinga template"""
    rendered_body = render_template_string(text)
    markdown_body = markdown.markdown(rendered_body, extensions=extensions)
    return markdown_body

DEBUG=True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION =  ['.md', '.markdown']
FLATPAGES_MARKDOWN_EXTENSIONS = extensions
FLATPAGES_HTML_RENDERER = renderer

# Flask Building Command.
app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

# Functions for use within the Jinja Templates.
@app.context_processor
def utility_processor():
    def get_icon(icon,source,size=32,color='F5F5F5'):
        """Retrieve icons from icongr.am"""
        color = f'&color={color}' if color else ''
        return f'https://icongr.am/{source}/{icon}.svg?size={size}{color}'
    return dict(get_icon=get_icon)

# Flask Routing.
@app.route('/')
def index():
    page = pages.get_or_404('index')
    projects = [p for p in pages if p.path.startswith('projects/')]
    print(projects)
    return render_template('index.html', page=page, projects=projects, **basics)

@app.route('/<string:landing>/')
def landing_page(landing):
    prologue = pages.get_or_404(landing)
    contents = [p for p in pages if p.path.startswith(f'{landing}/')]
    return render_template('landing.html', page=prologue, contents=contents, **basics)

@app.route('/<path:path>/')
def content_page(path):
    page = pages.get_or_404(path)
    return render_template('content.html', page=page, **basics)

if __name__ == '__main__':
    if "freeze" in sys.argv:
        freezer.freeze()
    else:
        app.run(port=8000)
