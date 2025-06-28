import os
import cloudconvert
import requests
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get the API key from .env
api_key = os.getenv("CLOUDCONVERT_API_KEY")
cloudconvert.configure(api_key=api_key)

def convert_word_to_pdf_cloud(docx_path, output_path):
    try:
        # Step 1: Create the job with import/upload → convert → export
        job = cloudconvert.Job.create(payload={
            "tasks": {
                "import-my-file": {
                    "operation": "import/upload"
                },
                "convert-my-file": {
                    "operation": "convert",
                    "input": "import-my-file",
                    "input_format": "docx",
                    "output_format": "pdf"
                },
                "export-my-file": {
                    "operation": "export/url",
                    "input": "convert-my-file"
                }
            }
        })

        # DEBUG: print the job structure
        print("===== CloudConvert Job Response =====")
        print(job)
        print("=====================================")

        # Step 2: Get the upload task and URL
        upload_task = next((task for task in job["tasks"] if task["name"] == "import-my-file"), None)
        if not upload_task:
            raise ValueError("No 'import-my-file' task found in job response.")

        upload_url = upload_task["result"]["form"]["url"]
        form_data = upload_task["result"]["form"]["parameters"]

        # Step 3: Upload the file to the URL
        with open(docx_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(upload_url, data=form_data, files=files)
            if response.status_code != 204:
                raise Exception(f"Upload failed with status code {response.status_code}")

        # Step 4: Wait for the job to complete
        job = cloudconvert.Job.wait(id=job['id'])

        # Step 5: Get export URL from task result
        export_task = next((task for task in job["tasks"] if task["name"] == "export-my-file"), None)
        if not export_task:
            raise ValueError("No 'export-my-file' task found in job result.")

        file_url = export_task["result"]["files"][0]["url"]

        # Step 6: Download the final PDF
        r = requests.get(file_url)
        with open(output_path, 'wb') as f:
            f.write(r.content)

        print("✅ Word to PDF conversion successful.")
        return True

    except Exception as e:
        print("❌ Error during conversion:", e)
        return False
