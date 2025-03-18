from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/about-us')
def about():
    return render_template('aboutus.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/contactus')
def contact():
    return render_template('contactus.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

#create for render login.html
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/eco-tips')
def ecotips():
    return render_template('eco-tips.html')

@app.route('/eco-location')
def ecolocation():
    return render_template('eco-location.html')

@app.route('/pollutedareas')
def pollutedarea():
    return render_template('polluted_areas.html')

@app.route('/stores')
def stores():
    return render_template('stores.html')

if __name__ == '__main__':
    app.run()