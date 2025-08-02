import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
 
load_dotenv()
 
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"Error configuring Gemini API: {e}") 
    exit()
 
app = Flask(__name__)

def summarize_with_gemini(text_to_summarize):
    """
    Uses the Gemini API to summarize the provided text.
    """
    if not text_to_summarize:
        return "Error: No text provided for summarization."

    try:
        
        prompt = f"""
        Please act as a scientific research assistant. Your task is to provide a concise,
        easy-to-understand summary of the following scientific text. Focus on the key
        findings, methodology, and conclusions. The summary should be about 3-4 sentences long.

        Scientific Text:
        ---
        {text_to_summarize}
        ---

        Summary:
        """
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return f"Error: Could not generate summary. Details: {e}"

 
@app.route('/summarize', methods=['POST'])
def summarize_endpoint():
    """
    API endpoint that receives text and returns a summary.
    """
    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'No text provided in the request.'}), 400

    text = request.json['text']
    summary = summarize_with_gemini(text)

    return jsonify({'summary': summary})
 
@app.route('/')
def index():
    """
    Serves the main HTML page for the user interface.
    The 'index.html' file should be in a folder named 'templates'.
    """
    return render_template('index.html')

 
if __name__ == '__main__':
    
    if not os.path.exists('templates'):
        os.makedirs('templates')
     
    app.run(debug=True, port=5001)
