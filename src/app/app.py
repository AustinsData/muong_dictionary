from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import csv
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)  # Define the Mail instance

def search_data(query, phrase=False):
    results = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if phrase:
                if query.lower() in row['muong'].lower():
                    results.append(row)
            else:
                if query.lower() == row['muong'].lower():
                    results.append(row)
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        data = search_data(query)
    else:
        data = None
    return render_template('search.html', data=data)

@app.route('/phrase_search')
def phrase_search():
    query = request.args.get('query')
    if query:
        data = search_data(query, phrase=True)
    else:
        data = None
    return render_template('phrase_search.html', data=data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Send email
        msg = Message(subject='Contact Us Form Submission',
                      sender=os.environ.get('MAIL_USERNAME'),
                      recipients=['austintanng@gmail.com'])
        msg.body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        mail.send(msg)
        
        # Redirect to thank you page or homepage
        return redirect(url_for('thank_you'))
    return render_template('contact.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
