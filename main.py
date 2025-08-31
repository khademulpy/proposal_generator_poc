from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import  Response
from typing import Optional
import google.generativeai as genai
import os
from proposal_generation import get_private_prompt_template, get_government_prompt_template
# Configure Gemini API
genai.configure(api_key="AIzaSyDFrwdXUKIKmoadahKvsugzCQwJtJi3mgw")

app = FastAPI(title="ACCOES Proposal Generation API", version="1.0.0")

@app.get("/generate-proposal")
async def generate_proposal(
    template_type: str = Query("private", description="Type of template: 'private' or 'government'")
):
    """
    Generate a proposal document based on the template type and provided parameters.
    
    Template types:
    - 'private': For private sector clients
    - 'government': For government sector clients
    """
    
    # Validate template type
    if template_type.lower() not in ['private', 'government']:
        return Response(content="Invalid template type. Use 'private' or 'government'.", status_code=400)
    
    # Select the appropriate template
    if template_type.lower() == 'private':
        prompt_template = get_private_prompt_template()
    else:
        prompt_template = get_government_prompt_template()
    
    # Create the full prompt with provided data
    full_prompt = prompt_template
    
    # Use the template as-is without additional parameters
    
    try:
        print("Generating proposal document... This may take several minutes due to the large amount of data.")
        
        # Generate content using Gemini API
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(full_prompt)
        
        print("Response received from Gemini API:")
        
        # Clean the response text by removing ```html markdown formatting

        
        # Save HTML file locally (exactly like proposal_generation.py)
        html_filename = "proposal_document.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"\nHTML document saved as: {html_filename}")
        print(f"File location: {os.path.abspath(html_filename)}")
        
        # Return success message instead of HTML content
        return {
            "message": "Proposal generated successfully",
            "filename": html_filename,
            "file_location": os.path.abspath(html_filename),
            "template_type": template_type,
            "file_size": len(response.text)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating proposal: {str(e)}")
    
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
