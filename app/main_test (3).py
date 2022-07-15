# Run by typing python3 main.py

# **IMPORTANT:** only collaborators on the project where you run
# this can access this web server!
"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page?
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building?
    3. What other features you'd like to develop to help AI write better with a user?
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model?
"""

# import basics
import os

# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
# import stuff for our models
from aitextgen import aitextgen
from flask_navigation import Navigation

#genre = genre_text_generation('sadness')
# load up a model from memory. Note you may not need all of these options.
#ai = aitextgen(model_folder =  'model/sadness_files', to_gpu=False)

#ai = aitextgen(model="model/sadness_files", to_gpu=False)

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url + 'static')

app.secret_key = os.urandom(64)

# set up the routes and logic for the webserver
nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home', 'home'),
    nav.Item('Generator', 'gen'),
    nav.Item('Our Team', 'our_team')
])


@app.route(f'{base_url}')
def home():
    return render_template('index.html', generated=None)


@app.route(f'{base_url}', methods=['POST'])
def home_post():
    return redirect(url_for('results'))


@app.route(f'{base_url}/results/')
def results():
    if 'data' in session:
        data = session['data']
        return render_template('generator.html', generated=data)
    else:
        return render_template('generator.html', generated=None)


@app.route(f'{base_url}/gen', methods=['GET', 'POST'])
def gen():
    return render_template('generator.html', generated=None)


@app.route(f'{base_url}/our_team', methods=['GET', 'POST'])
def our_team():
    return render_template('our_team.html', generated=None)


@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text.
    """
    print("Something ran 1")

    num_lines = int(request.form['list'])
    py_prompt = (request.form['promptbox'])
    temp = (int(request.form['temperature'])) / 100
    print("Something ran 2")
    print(temp)
    print(num_lines)
    print(py_prompt)
    ai = aitextgen(model_folder = 'model/', to_gpu=False)
    res = []
    for i in range(num_lines):
        if py_prompt is not None:
            generate = ai.generate_one(
                batch_size=3,
                prompt=str(py_prompt),
                max_length=140,
                temperature=temp
                #return_as_list=True
            )

        data = {'generated_ls': generate}
        session['data'] = generate

        generate = generate.replace('"','')
        generate = generate.replace("â€™", "")
        generate = generate.replace("â€¦", "")
        generate = generate.replace("‘¦", "")
        generate = generate.replace("â€˜", "")
        output = generate.split('\n')
        print(output)
        res.append(output[0])

    final_res = ''

    for ele in res:
        final_res += ele
        final_res += '\n'
    print('Result is: ')
    print(final_res)

    return render_template('generator.html', results=final_res)


# define additional routes here
# for example:
#@app.route(f'{base_url}/spec')
#def team_members():
#return render_template('realprocess.html')

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc16.ai-camp.dev'

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
