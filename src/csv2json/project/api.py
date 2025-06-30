"""Project-level API endpoints."""

import csv
import io
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any

# Create a router for project-level endpoints
router = APIRouter(prefix="/api", tags=["api"])


class CsvToJsonRequest(BaseModel):
    """CSV to JSON conversion request model."""
    csv_content: str = Field(..., description="CSV content as string")
    delimiter: str = Field(",", description="CSV delimiter character")
    quotechar: str = Field('"', description="CSV quote character")
    has_header: bool = Field(True, description="Whether CSV has header row")
    encoding: str = Field("utf-8", description="CSV encoding")


class CsvToJsonResponse(BaseModel):
    """CSV to JSON conversion response model."""
    json_data: list[dict[str, Any]]
    row_count: int
    column_count: int


@router.post("/csv2json", response_model=CsvToJsonResponse)
async def convert_csv_to_json(request: CsvToJsonRequest) -> CsvToJsonResponse:
    """Convert CSV content to JSON format.
    
    Takes CSV content as string and converts it to JSON array of objects.
    Supports custom delimiters, quote characters, and encoding options.
    """
    try:
        # Parse CSV content
        csv_file = io.StringIO(request.csv_content)
        csv_reader = csv.DictReader(
            csv_file,
            delimiter=request.delimiter,
            quotechar=request.quotechar
        ) if request.has_header else csv.reader(
            csv_file,
            delimiter=request.delimiter,
            quotechar=request.quotechar
        )
        
        json_data = []
        row_count = 0
        column_count = 0
        
        if request.has_header:
            # Use DictReader for header-based parsing
            for row in csv_reader:
                json_data.append(dict(row))
                row_count += 1
                if row_count == 1:
                    column_count = len(row)
        else:
            # Use basic reader and create numbered columns
            for row in csv_reader:
                if row_count == 0:
                    column_count = len(row)
                row_dict = {f"column_{i+1}": value for i, value in enumerate(row)}
                json_data.append(row_dict)
                row_count += 1
        
        return CsvToJsonResponse(
            json_data=json_data,
            row_count=row_count,
            column_count=column_count
        )
        
    except csv.Error as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}") 