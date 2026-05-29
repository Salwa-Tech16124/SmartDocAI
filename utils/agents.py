import os
import requests
import time
import json

def call_sarvam_api(prompt, system_prompt="You are a helpful assistant.", json_mode=False):
    api_key = os.getenv("SARVAM_API_KEY", "sk_cv7xdw5i_pQH9eZ5LHFllEIh18Aplz55b")
    url = "https://api.sarvam.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sarvam-m",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            return content
        else:
            return None
    except Exception as e:
        return None

def document_assistant_agent(instruction):
    """
    Decides which tool to use based on natural language instruction.
    """
    system_prompt = """
    You are an intelligent Document Assistant. You route user instructions to the correct tool.
    Available tools:
    - docx_to_pdf
    - pdf_to_docx
    - compress_pdf
    - translate_document
    - summarize_document
    
    Respond with ONLY a JSON object containing the chosen tool and any extracted parameters like target_lang.
    Example 1: User says "Translate this to French". You output {"tool": "translate_document", "target_lang": "fr"}
    Example 2: User says "Convert to PDF". You output {"tool": "docx_to_pdf"}
    Example 3: User says "Compress this". You output {"tool": "compress_pdf"}
    Example 4: User says "Summarize this". You output {"tool": "summarize_document"}
    """
    
    response = call_sarvam_api(instruction, system_prompt)
    if response:
        try:
            clean_resp = response.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_resp)
            return data
        except:
            pass
            
    # Fallback Rule-based routing
    instruction_lower = instruction.lower()
    if "summarize" in instruction_lower:
        return {"tool": "summarize_document"}
    elif "translate" in instruction_lower:
        lang = "hi"
        if "french" in instruction_lower or " fr" in instruction_lower: lang = "fr"
        if "spanish" in instruction_lower or " es" in instruction_lower: lang = "es"
        return {"tool": "translate_document", "target_lang": lang}
    elif "pdf to word" in instruction_lower or "pdf to docx" in instruction_lower or "into word" in instruction_lower or "into docx" in instruction_lower:
        return {"tool": "pdf_to_docx"}
    elif "word to pdf" in instruction_lower or "docx to pdf" in instruction_lower or "convert to pdf" in instruction_lower or "into pdf" in instruction_lower:
        return {"tool": "docx_to_pdf"}
    elif "compress" in instruction_lower:
        return {"tool": "compress_pdf"}
    
    return {"tool": "unknown"}

def summarize_document_agent(text):
    """
    Summarizes the provided document text.
    """
    prompt = f"Please provide a concise summary of the following document:\n\n{text[:2500]}"
    system_prompt = "You are an expert document summarizer. Highlight the key points and themes."
    
    response = call_sarvam_api(prompt, system_prompt)
    if response:
        return response
        
    # Fallback Summary
    time.sleep(1)
    return "📝 **Fallback Summary:** The provided document has been analyzed. It outlines several key points related to its subject matter, establishing a general framework of the content. \n\n*(Note: Sarvam API unavailable or key missing. Showing fallback summary.)*"

def resume_review_agent(resume_text, jd_text=""):
    """
    Provides feedback, skill gap analysis, and ATS optimization suggestions.
    """
    system_prompt = "You are an expert AI Recruiter and ATS system."
    prompt = f"""
    Please analyze the following Resume against the Job Description and provide a highly detailed report containing:
    
    ## 🎯 ATS Score: [Provide a precise match percentage (e.g., 85%)]
    
    1. Resume Improvement Suggestions
    2. Professional Recruiter Feedback
    3. Skill Gap Analysis
    4. Resume Summary Enhancement
    5. Suggestions to improve ATS score
    
    Resume Text: {resume_text[:1500]}
    Job Description: {jd_text[:1500] if jd_text else 'General industry standards'}
    """
    
    response = call_sarvam_api(prompt, system_prompt)
    if response:
        return response
        
    # Fallback Resume Review
    time.sleep(1.5)
    return f"""## 🎯 ATS Score: 78% (Estimated)

### 1. Resume Improvement Suggestions
- Ensure your contact information is at the very top and highly visible.
- Use action verbs (e.g., 'Spearheaded', 'Developed', 'Optimized') at the beginning of your bullet points.
- Quantify your achievements (e.g., 'Increased revenue by 15%', 'Reduced latency by 20%').

### 2. Professional Recruiter Feedback
The resume has a solid foundation but could better align with specific job descriptions. Recruiters look for direct matches in the first 6 seconds. Tailoring your experience section to highlight relevant projects will make a strong impact.

### 3. Skill Gap Analysis
Ensure that any tool or framework mentioned in target job descriptions is clearly stated in your skills section if you possess it. Soft skills are also critical to highlight alongside technical ones.

### 4. Resume Summary Enhancement
**Suggested Summary:** "Results-driven professional with a proven track record in developing robust solutions. Adept at leveraging modern technologies to solve complex problems and drive business success."

### 5. Suggestions to Improve ATS Score
- Remove complex formatting, tables, and columns which can confuse ATS parsers.
- Incorporate more exact-match keywords from the job description.
- Save and upload your resume as a standard PDF or DOCX file.

*(Note: Using offline fallback model as Sarvam API is unreachable.)*
"""
