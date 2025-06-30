# CSV to JSON Converter

A web application for converting CSV files to JSON format with configurable parsing options.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install uv
   uv sync
   ```

2. **Start the API backend:**
   ```bash
   uv run service
   ```

3. **Start the web UI (in a new terminal):**
   ```bash
   uv run ui
   ```

4. **Open your browser** and go to `http://localhost:8080`

5. **Upload a CSV file** and configure the parsing settings to convert it to JSON!

## Features

- **Web UI**: Modern, responsive interface built with Flask and Tailwind CSS
- **API Backend**: FastAPI-based REST API for CSV to JSON conversion
- **Configurable Parsing**: Support for different delimiters, quote characters, and encodings
- **File Upload**: Drag-and-drop file upload with 16MB size limit
- **Real-time Conversion**: Instant conversion with progress feedback
- **JSON Preview**: Formatted JSON output with copy-to-clipboard functionality
- **Docker Support**: Containerized deployment with docker-compose
- **Error Handling**: Comprehensive error handling and user feedback

### CSV Conversion Features

- Support for various delimiters (comma, semicolon, tab, pipe)
- Configurable quote characters
- Multiple encoding options (UTF-8, Latin-1, Windows-1252)
- Header row detection
- Row and column count statistics
- Prettified JSON output

## Configuration

The service requires the following environment variables:

### Application Configuration

These variables are prefixed with `CSV2JSON_`:

- `CSV2JSON_NAME`: Name of your service (default: "CSV 2 JSON")
- `CSV2JSON_VERSION`: Version of your service (default: package version)
- `CSV2JSON_LOG_LEVEL`: Logging level (default: 20 for INFO)

### UI Configuration

You can configure the API host and port that the UI connects to:

- `API_HOST`: Host of the CSV2JSON API (default: "localhost")
- `API_PORT`: Port of the CSV2JSON API (default: 5000)

These can be set in your environment or in a `.env` file in the project root.

## Project Structure

The template creates a well-organized project structure:

```
csv2json/
├── src/
│   └── csv2json/
│       ├── api/                  # Core API functionality
│       │   ├── definition.py     # API definition generation
│       │   ├── run.py            # Server startup
│       │   └── server.py         # FastAPI server configuration
│       ├── project/              # Project-specific code
│       │   └── api.py            # CSV conversion API endpoints
│       ├── templates/            # Flask HTML templates
│       │   ├── base.html         # Base template
│       │   └── converter.html    # CSV converter interface
│       ├── static/               # Static assets (logos, etc.)
│       ├── app.py                # Flask web application
│       ├── config.py             # Configuration management
│       └── __init__.py           # Package initialization
├── tests/                        # Test suite
├── kubernetes/                   # Kubernetes deployment files
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
├── pyproject.toml                # Project metadata and dependencies
└── README.md                     # This file
```

## Usage

### Creating a New Project

```bash
cookiecutter gh:mibexx/mbxai-srv-template
```

Follow the prompts to configure your project.

### Installing Dependencies with uv

This project uses [uv](https://github.com/astral-sh/uv) for fast and reliable dependency management:

```bash
# Install uv if you don't have it already
pip install uv

# Install dependencies
uv sync

# Run the service
uv run service
```

Or with command-line arguments:

```bash
uv run service -- --host 127.0.0.1 --port 5000 --reload
```

### Running the Applications

The CSV to JSON converter consists of two applications:

#### 1. Run the API Backend (FastAPI)

```bash
# Using uv
uv run service

# Or directly with Python
python -m src.csv2json.api.run --host 127.0.0.1 --port 5000 --reload
```

#### 2. Run the Web UI (Flask)

```bash
# Using uv
uv run ui

# Or directly with Python
python -m src.csv2json.app
```

The UI will be available at `http://localhost:8080` and will communicate with the API at `http://localhost:5000`.

### Docker Deployment

```bash
# Build the Docker image
docker build -t csv2json .

# Run the container
docker run -p 5000:5000 csv2json
```

Or with docker-compose:

```bash
docker-compose up
```

### API Endpoints

The service includes the following API endpoints:

- `GET /ident`: Returns basic service identity information
- `GET /mbxai-definition`: Returns the definition of all API endpoints
- `POST /api/csv2json`: Converts CSV content to JSON format


#### CSV Conversion Endpoint

The main conversion endpoint accepts the following parameters:

```json
{
  "csv_content": "string (required)",
  "delimiter": "string (default: ',')",
  "quotechar": "string (default: '\"')",
  "has_header": "boolean (default: true)",
  "encoding": "string (default: 'utf-8')"
}
```

Response format:
```json
{
  "json_data": [{"column1": "value1", "column2": "value2"}],
  "row_count": 10,
  "column_count": 3
}
```

## Development

The project is structured as a microservice with separate API and UI components:

### Testing

You can test the CSV conversion API directly using curl:

```bash
# Test the CSV conversion endpoint
curl -X POST "http://localhost:5000/api/csv2json" \
     -H "Content-Type: application/json" \
     -d '{
       "csv_content": "name,age,city\nJohn,30,New York\nJane,25,London",
       "delimiter": ",",
       "quotechar": "\"",
       "has_header": true,
       "encoding": "utf-8"
     }'
```

Expected response:
```json
{
  "json_data": [
    {"name": "John", "age": "30", "city": "New York"},
    {"name": "Jane", "age": "25", "city": "London"}
  ],
  "row_count": 2,
  "column_count": 3
}
```

## Code Quality

The project uses several tools to maintain code quality:

- **Ruff**: For linting and code formatting
- **Type hints**: Full type annotation coverage
- **Pydantic**: For data validation and settings management

Run quality checks:
```bash
# Linting
ruff check .

# Formatting  
ruff format .
```

## Requirements

- Python 3.12+
- uv (recommended) or pip for dependency management

## License

This project is licensed under the MIT License.
