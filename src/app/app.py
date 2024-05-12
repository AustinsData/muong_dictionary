from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def get_data_by_muong(muong_word):
    result = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['muong'] == muong_word:
                result.append(row)
    print(result)
    return result

def get_data_by_vietnamese(viet_word):
    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['viet'] == viet_word:
                return row
    return None

@app.route('/')
def index():
    return render_template('index.html', data=None)

@app.route('/search')
def search():
    muong_word = request.args.get('muong')
    viet_word = request.args.get('vietnamese')
    
    if muong_word:
        data = get_data_by_muong(muong_word)
    elif viet_word:
        data = get_data_by_vietnamese(viet_word)
    else:
        data = None

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
