from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from openai import OpenAI  
from typing import List
import os
import fitz
from docx import Document
import pandas as pd
import asyncio
from io import BytesIO
import json
from fastapi.responses import StreamingResponse

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # New client initialization
print(os.getenv("OPENAI_API_KEY"))

async def extract_text(file: UploadFile) -> str:
    content = await file.read()
    try:
        if file.filename.lower().endswith('.pdf'):
            with fitz.open(stream=content, filetype="pdf") as doc:
                return "".join(page.get_text() for page in doc)
        elif file.filename.lower().endswith('.docx'):
            return "\n".join(p.text for p in Document(BytesIO(content)).paragraphs)
        else:
            raise HTTPException(400, "Unsupported file type")
    except Exception as e:
        raise HTTPException(500, f"Text extraction error: {str(e)}")
    finally:
        await file.close()

@app.post("/extract-criteria")
async def extract_criteria(file: UploadFile = File(...)):
    try:
        text = await extract_text(file)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Extract key ranking criteria as JSON list from:\n{text}"
            }]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(500, f"LLM processing error: {str(e)}")

@app.post("/score-resumes")
async def score_resumes(
    criteria: List[str] = Form(...),
    files: List[UploadFile] = File(...)
):
    async def process_resume(file: UploadFile):
        try:
            text = await extract_text(file)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": f"Score 0-5 for {criteria} in resume:\n{text}. Return JSON with 'name' and 'scores'."
                }]
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"name": file.filename, "scores": [0]*len(criteria)}
    
    results = await asyncio.gather(*[process_resume(f) for f in files])
    df = pd.DataFrame(results)
    stream = BytesIO()
    df.to_excel(stream, index=False)
    stream.seek(0)
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=scores.xlsx"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
