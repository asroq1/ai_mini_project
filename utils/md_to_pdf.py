import subprocess
import os
import sys

def convert_md_to_pdf(md_file_path, output_dir):
    """
    Converts a Markdown file to PDF using the markdown-pdf command-line tool.

    Args:
        md_file_path (str): The absolute path to the Markdown file.
        output_dir (str): The absolute path to the directory where the PDF should be saved.

    Returns:
        tuple: (str, bool) - Path to the generated PDF and success status.
    """
    if not os.path.isabs(md_file_path):
        print(f"Error (md_to_pdf): md_file_path must be an absolute path. Got: {md_file_path}")
        return None, False
    if not os.path.isabs(output_dir):
        print(f"Error (md_to_pdf): output_dir must be an absolute path. Got: {output_dir}")
        return None, False

    if not os.path.exists(md_file_path):
        print(f"Error (md_to_pdf): Markdown file not found at {md_file_path}")
        return None, False

    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Info (md_to_pdf): Created output directory {output_dir}")
        except Exception as e:
            print(f"Error (md_to_pdf): Could not create output directory {output_dir}: {e}")
            return None, False

    base_name = os.path.basename(md_file_path)
    pdf_filename = os.path.splitext(base_name)[0] + ".pdf"
    pdf_file_path = os.path.join(output_dir, pdf_filename)

    try:
        # Check if markdown-pdf is installed
        subprocess.run(["markdown-pdf", "--version"], check=True, capture_output=True, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error (md_to_pdf): 'markdown-pdf' command not found or not working.")
        print("Please install it globally using: npm install -g markdown-pdf")
        print("Alternatively, make sure it's in your PATH.")
        return None, False

    try:
        print(f"Info (md_to_pdf): Converting {md_file_path} to {pdf_file_path}...")
        # Ensure paths are correctly quoted if they contain spaces
        # command = ["markdown-pdf", f'"''{md_file_path}'"'', "-o", f'"''{pdf_file_path}'"''] # This line causes SyntaxError
        # On Windows, shell=True might be needed if command quoting is tricky, but try without first for security.
        # For macOS/Linux, shell=False is generally safer.
        # Using a more robust way to pass arguments that might contain spaces:
        command = ["markdown-pdf", md_file_path, "-o", pdf_file_path]
        
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        print(f"Info (md_to_pdf): PDF conversion successful: {pdf_file_path}")
        if result.stdout:
            print(f"markdown-pdf stdout:\n{result.stdout}")
        if result.stderr:
            print(f"markdown-pdf stderr:\n{result.stderr}") # Should be empty on success
        return pdf_file_path, True
    except subprocess.CalledProcessError as e:
        print(f"Error (md_to_pdf): markdown-pdf conversion failed for {md_file_path}.")
        print(f"  Command: {' '.join(e.cmd)}")
        print(f"  Return code: {e.returncode}")
        print(f"  Stdout:\n{e.stdout}")
        print(f"  Stderr:\n{e.stderr}")
        return None, False
    except FileNotFoundError:
        # This specific check is somewhat redundant due to the earlier check, but good for safety.
        print("Error (md_to_pdf): 'markdown-pdf' command not found. Please ensure it is installed and in your PATH.")
        print("  Installation: npm install -g markdown-pdf")
        return None, False
    except Exception as e:
        print(f"Error (md_to_pdf): An unexpected error occurred during PDF conversion: {e}")
        return None, False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python md_to_pdf.py <markdown_file_path> <output_directory>")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_dir_arg = sys.argv[2]

    # Ensure paths are absolute for the script's internal logic
    if not os.path.isabs(md_file):
        md_file = os.path.abspath(md_file)
    if not os.path.isabs(output_dir_arg):
        output_dir_arg = os.path.abspath(output_dir_arg)

    print(f"Debug (md_to_pdf_main): MD file: {md_file}")
    print(f"Debug (md_to_pdf_main): Output dir: {output_dir_arg}")

    pdf_path, success = convert_md_to_pdf(md_file, output_dir_arg)

    if success:
        print(f"Successfully converted to PDF: {pdf_path}")
    else:
        print("PDF conversion failed.")
        sys.exit(1)
