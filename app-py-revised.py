from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import json
import logging
import tempfile
import csv
from werkzeug.utils import secure_filename

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# ----- Gmail Draft Creation Routes -----

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/drafts')
def drafts_index():
    return redirect(url_for('drafts_setup'))

@app.route('/drafts/setup')
def drafts_setup():
    return render_template('drafts_setup.html')

@app.route('/drafts/ai-settings')
def drafts_ai_settings():
    return render_template('drafts_ai.html')

@app.route('/drafts/manual')
def drafts_manual():
    return render_template('drafts_manual.html')

@app.route('/drafts/automation')
def drafts_automation():
    return render_template('drafts_automation.html')

# ----- Gmail Draft Sending Routes -----

@app.route('/sending')
def sending_index():
    return redirect(url_for('sending_setup'))

@app.route('/sending/setup')
def sending_setup():
    return render_template('sending_setup.html')

@app.route('/sending/automation')
def sending_automation():
    return render_template('sending_automation.html')

# ----- API Endpoints -----

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'ok',
        'timestamp': os.environ.get('DEPLOYMENT_TIMESTAMP', 'development')
    })

@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['csv_file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'success': False, 'error': 'File must be a CSV'}), 400
    
    # Save the file temporarily
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Process the CSV file
        result = {
            'email_addresses': [],
            'first_names': [],
            'companies': [],
            'columns': []
        }
        
        # Get column indices from request (default to common values if not provided)
        email_col = request.form.get('email_column', 'C')
        name_col = request.form.get('name_column', 'A')
        company_col = request.form.get('company_column', 'F')
        
        # Convert column letters to indices
        email_idx = ord(email_col.upper()) - ord('A')
        name_idx = ord(name_col.upper()) - ord('A')
        company_idx = ord(company_col.upper()) - ord('A')
        
        with open(filepath, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            
            # Store column names
            result['columns'] = headers
            
            # Validate column indices are within range
            max_index = max(email_idx, name_idx, company_idx)
            if max_index >= len(headers):
                return jsonify({
                    'success': False, 
                    'error': f'Column index out of range. The CSV only has {len(headers)} columns.'
                }), 400
            
            # Process rows
            for row in csv_reader:
                if len(row) > max_index:
                    email = row[email_idx].strip()
                    first_name = row[name_idx].strip() if name_idx < len(row) else ''
                    company = row[company_idx].strip() if company_idx < len(row) else ''
                    
                    if email:  # Only include rows with email addresses
                        result['email_addresses'].append(email)
                        result['first_names'].append(first_name)
                        result['companies'].append(company)
        
        # Store data in session
        session['csv_data'] = result
        
        # Store as JSON in session storage for JS to access
        session['csv_data_json'] = json.dumps({
            'emailAddresses': result['email_addresses'],
            'firstNames': result['first_names'],
            'companies': result['companies']
        })
        
        # Return success with data summary
        return jsonify({
            'success': True, 
            'message': f"Successfully processed {len(result['email_addresses'])} email addresses",
            'count': len(result['email_addresses']),
            'preview': result['email_addresses'][:5] if result['email_addresses'] else []
        })
    
    except Exception as e:
        logger.error(f"Error processing CSV: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        # Clean up the temporary file
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/api/test-perplexity', methods=['POST'])
def test_perplexity():
    api_key = request.json.get('api_key')
    model = request.json.get('model', 'sonar')
    temperature = float(request.json.get('temperature', 0.7))
    
    if not api_key:
        return jsonify({'success': False, 'error': 'API key is required'}), 400
    
    # For demo purposes, we'll simulate a successful API response
    # In a real implementation, you would make an actual API call
    try:
        # Simulate API response
        response = {
            'success': True,
            'message': 'API connection successful',
            'content': 'Hello! I am the Perplexity AI assistant. Your API connection is working correctly.',
            'model': model,
            'tokens': {
                'completion': 15,
                'prompt': 25,
                'total': 40
            }
        }
        
        # Save API key and preferences to session
        session['perplexity_api_key'] = api_key
        session['perplexity_model'] = model
        session['perplexity_temperature'] = temperature
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error testing Perplexity API: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/start-automation', methods=['POST'])
def start_draft_automation():
    """
    Endpoint to start the draft creation automation process
    This would be implemented with background tasks in a production environment
    """
    browser = request.json.get('browser', 'firefox')
    use_ai = request.json.get('use_ai', False)
    
    # In a real implementation, this would start a background process
    # Here we're just returning a success response for demonstration
    
    return jsonify({
        'success': True,
        'message': 'Automation started',
        'browser': browser,
        'use_ai': use_ai
    })

@app.route('/api/sending/start', methods=['POST'])
def start_sending_automation():
    """
    Endpoint to start the draft sending automation process
    """
    delay_minutes = int(request.json.get('delay_minutes', 5))
    delay_seconds = int(request.json.get('delay_seconds', 0))
    limit = int(request.json.get('limit', 0))
    
    # In a real implementation, this would start a background process
    
    return jsonify({
        'success': True,
        'message': 'Sending automation started',
        'delay': f"{delay_minutes} min {delay_seconds} sec",
        'limit': limit if limit > 0 else "All drafts"
    })

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, message="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500, message="Server error"), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
