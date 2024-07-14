from flask import Flask, request, jsonify, render_template
from serpapi import GoogleSearch
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    category = data.get('category')
    detail = data.get('detail')
    custom_query = data.get('custom_query')
    
    if custom_query:
        query = custom_query
    elif category and detail:
        query = f"{category} {detail}"
    else:
        return jsonify({'error': 'Incomplete question provided'}), 400

    answer = fetch_google_results(query)
    return jsonify({'answer': answer})

def fetch_google_results(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": "49a7e61c21b23ef2c0341eedcbaa8dcd86622b142910aeb963009a250e4684cf"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if 'organic_results' in results:
        top_results = results['organic_results'][:10]  # Get the top 5 results
        return [{'title': res['title'], 'link': res['link']} for res in top_results]
    return "No results found"

@app.route('/clone', methods=['POST'])
def clone():
    data = request.json
    url = data.get('url')
    
    if url:
        command = f"wget {url} -P downloads/"
        subprocess.run(command, shell=True)
        return jsonify({'status': 'Download started'})
    return jsonify({'error': 'No URL provided'}), 400

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
