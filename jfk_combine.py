from PyPDF2 import PdfMerger
import os

# Configuration
download_dir = '.'  # Current directory (where the script and PDFs are)
output_file = 'combined.pdf'

# Initialize the PDF merger
merger = PdfMerger()

# Get list of all PDF files in the directory
pdf_files = [f for f in os.listdir(download_dir) if f.endswith('.pdf')]

# Sort by modification time (approximates download order)
pdf_files.sort(key=lambda f: os.path.getmtime(os.path.join(download_dir, f)))

# Merge each PDF into the combined file
for pdf in pdf_files:
    try:
        full_path = os.path.join(download_dir, pdf)
        merger.append(full_path)
        print(f"Added: {pdf}")
    except Exception as e:
        print(f"Skipping {pdf}: {e}")

# Save the combined PDF
merger.write(output_file)
merger.close()

print(f"\nCombined PDF saved as {output_file}")