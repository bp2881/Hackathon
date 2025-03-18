from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

#create for render login.html
@app.route('/login')
def login():
    return render_template('login.html')

#create for render register.html
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/eco-locations')
def ecolocation():
    return render_template('eco-location.html')

if __name__ == '__main__':
    app.run(debug=True)