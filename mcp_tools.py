from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
import os

from pydantic import BaseModel


# Define models
class FileCreationRequest(BaseModel):
    content: str
    path: str

app = FastAPI()

@app.post("/create_file/")
async def create_file(request: FileCreationRequest):
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(request.path), exist_ok=True)
        
        # Write content to file
        with open(request.path, 'w') as f:
            f.write(request.content)
            
        return {"message": f"File created at {request.path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize MCP
mcp = FastApiMCP(
    app,
    name="Code AI Partner API",
    base_url="http://localhost:8000",
    describe_all_responses=True,
    describe_full_response_schema=True
)

mcp.mount()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
