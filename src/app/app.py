from flask import Flask, render_template, request, redirect, url_for
import csv
import os


app = Flask(__name__)


def search_data(query, phrase=False):
    results = []
    with open('./data/data.csv', 'r', encoding='utf-8') as file:
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
    with open('./data/progress_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    return render_template('index.html', progress_data=rows)

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
    return render_template('contact.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
