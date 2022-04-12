from flask import Flask, render_template, send_from_directory, redirect, url_for, request
import os
from data.reg_form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def main_wind():
    return render_template('Title_page.html')

@app.route('/regist', methods=['GET', 'POST'])
def reg():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('Registration.html', form=form)



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
