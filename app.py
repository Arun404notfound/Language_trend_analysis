from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
from flask import send_from_directory

app = Flask(__name__)
CORS(app)  # Allow all origins for now

# Load the processed CSV file
df = pd.read_csv('language_trend_summary.csv')  # Make sure this file exists!

@app.route('/')
def index():
    return send_from_directory('templates','index.html')

@app.route('/api/languages')
def get_languages():
    languages = sorted(df['language'].unique().tolist())
    return jsonify(languages)

@app.route('/api/data/<language>')
def get_language_data(language):
    language=language.lower()
    data = df[df['language'] == language]
    response = data[['year', 'count']].to_dict(orient='records')
    return jsonify(response)

@app.route('/api/total_counts')
def get_total_counts():
    total_counts = df.groupby('language')['count'].sum().reset_index()
    sorted_counts = total_counts.sort_values(by='count', ascending=False)
    return jsonify(sorted_counts.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)

