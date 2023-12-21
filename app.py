from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    use_rp_search = request.form.get('use_rp_search') == 'true'

    cx = '' if use_rp_search else ''
    api_key = ''

    url = f'https://www.googleapis.com/customsearch/v1?q={query}&cx={cx}&key={api_key}'

    try:
        response = requests.get(url)
        data = response.json()
        items = data.get('items', [])
        return jsonify({'items': items})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
