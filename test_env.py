# test_env.py
import os
from dotenv import load_dotenv
import cloudconvert

load_dotenv()
api_key = os.getenv("CLOUDCONVERT_API_KEY")

if not api_key:
    print("❌ API key not found. Check your .env file.")
    exit()

cloudconvert.configure(api_key=api_key)

try:
    job = cloudconvert.Job.create(payload={
        "tasks": {
            'import-my-file': {
                'operation': 'import/url',
                'url': 'https://file-examples-com.github.io/uploads/2017/10/file-sample_150kB.pdf'
            }
        }
    })
    print("✅ API key works! Job created:\n", job)
except Exception as e:
    print("❌ Error:", e)
