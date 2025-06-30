"""Main Flask application."""

import os
import json
import logging
import requests
from flask import Flask, render_template, request, flash
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from .config import get_ui_config


class CsvConverterForm(FlaskForm):
    """Form for CSV to JSON conversion."""
    csv_file = FileField('CSV File', validators=[DataRequired()])
    delimiter = SelectField('Delimiter (Trennzeichen)', 
                          choices=[(',', 'Comma (,)'), (';', 'Semicolon (;)'), 
                                 ('\t', 'Tab'), ('|', 'Pipe (|)')], 
                          default=',')
    quotechar = SelectField('Quote Character', 
                          choices=[('"', 'Double Quote (")'), ("'", "Single Quote (')"), 
                                 ('', 'None')], 
                          default='"')
    has_header = BooleanField('Has Header Row', default=True)
    encoding = SelectField('Encoding', 
                         choices=[('utf-8', 'UTF-8'), ('latin-1', 'Latin-1'), 
                                ('cp1252', 'Windows-1252')], 
                         default='utf-8')
    submit = SubmitField('Convert to JSON')


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    config = get_ui_config()
    app.config.from_object(config)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Configure logging
    if config.DEBUG:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        app.logger.setLevel(logging.INFO)
    
    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Add config and csrf_token to template context
    @app.context_processor
    def inject_config():
        from flask_wtf.csrf import generate_csrf
        return dict(config=config, csrf_token=generate_csrf)
    
    # Routes
    @app.route('/')
    def index():
        """Home page with CSV converter form."""
        form = CsvConverterForm()
        return render_template('converter.html', form=form, active_page='overview')
    
    @app.route('/convert', methods=['POST'])
    def convert_csv():
        """Handle CSV to JSON conversion."""
        form = CsvConverterForm()
        
        if form.validate_on_submit():
            try:
                # Read uploaded file
                csv_file = form.csv_file.data
                csv_content = csv_file.read().decode(form.encoding.data)
                
                # Prepare API request
                api_data = {
                    'csv_content': csv_content,
                    'delimiter': form.delimiter.data,
                    'quotechar': form.quotechar.data,
                    'has_header': form.has_header.data,
                    'encoding': form.encoding.data
                }
                
                # Call API endpoint
                api_url = f"{config.API_URL}/api/csv2json"
                response = requests.post(api_url, json=api_data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                
                # Format JSON for display
                formatted_json = json.dumps(result['json_data'], indent=2, ensure_ascii=False)
                
                flash(f'Successfully converted CSV! {result["row_count"]} rows, {result["column_count"]} columns.', 'success')
                
                return render_template('converter.html', 
                                     form=form, 
                                     json_result=formatted_json,
                                     row_count=result['row_count'],
                                     column_count=result['column_count'],
                                     active_page='overview')
                
            except requests.RequestException as e:
                flash(f'API Error: {str(e)}', 'error')
            except UnicodeDecodeError:
                flash('Error reading file. Please check the encoding setting.', 'error')
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'error')
        
        return render_template('converter.html', form=form, active_page='overview')
    
    return app


def run_dev_server() -> None:
    """Run development server."""
    app = create_app()
    config = get_ui_config()
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )


def run_server() -> None:
    """Run production server."""
    app = create_app()
    config = get_ui_config()
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=False
    )


if __name__ == "__main__":
    run_dev_server() 