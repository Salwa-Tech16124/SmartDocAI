import pypandoc

try:
    pypandoc.download_pandoc()  # Optional: Ensures it's available
    output = pypandoc.convert_file("test.docx", "pdf", outputfile="test.pdf")
    print("✅ Converted to PDF successfully!")
except Exception as e:
    print("❌ Conversion failed:", e)
