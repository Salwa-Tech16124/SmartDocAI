def compress_pdf_with_convertapi(filepath, output_folder, bearer_token, quality="medium"):
    import requests
    import base64
    import os

    filename = os.path.basename(filepath)

    # Read and encode the PDF file
    with open(filepath, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode('utf-8')

    url = "https://v2.convertapi.com/convert/pdf/to/pdf"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "Parameters": [
            {
                "Name": "File",
                "FileValue": {
                    "Name": filename,
                    "Data": encoded_file
                }
            },
            {
                "Name": "Quality",
                "Value": quality
            },
            {
                "Name": "StoreFile",
                "Value": True
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.ok:
        file_url = response.json()["Files"][0]["Url"]
        download_response = requests.get(file_url)
        if download_response.ok:
            output_path = os.path.join(output_folder, f"compressed_{filename}")
            with open(output_path, "wb") as f:
                f.write(download_response.content)
            return True, output_path
        else:
            return False, "Download failed."
    else:
        return False, response.text
