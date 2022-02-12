from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from stories import stories

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

@app.route('/')
def homepage():
    return render_template('homepage.html', stories=stories.keys())

@app.route('/story-form')
def story_form():
    selected_story_key = request.args['story_select']
    selected_story = stories.get(selected_story_key)
    return render_template('story_form.html', key=selected_story_key, prompts=selected_story.prompts)

def generate_text_from_args(key):
    selected_story = stories.get(key)
    ans = dict()
    for prompt in selected_story.prompts:
        ans[prompt] = request.args.get(prompt)
    return selected_story.generate(ans)

@app.route('/story/<key>')
def show_story(key):
    text = generate_text_from_args(key)
    return render_template('story.html', text=text)
 