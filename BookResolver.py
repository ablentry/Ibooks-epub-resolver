import os
import shutil
import zipfile
import tempfile

def is_valid_epub(epub_path):
    """Check if the EPUB file is a valid ZIP archive."""
    try:
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            return zip_ref.testzip() is None
    except zipfile.BadZipFile:
        return False

def remove_unwanted_metadata(extracted_dir):
    """Remove unwanted metadata files from the extracted EPUB."""
    for root, _, files in os.walk(extracted_dir):
        for filename in files:
            if filename.startswith("iTunesMetadata") and filename.endswith(".plist") or filename == "com.apple.ibooks.display-options.xml":
                os.remove(os.path.join(root, filename))

def rebuild_epub(extracted_dir, output_epub):
    """Rebuild the EPUB file from its extracted contents, ensuring proper structure."""
    mimetype_path = os.path.join(extracted_dir, "mimetype")
    epub_files = []
    
    # Collect files in sorted order to maintain structure
    for root, _, files in os.walk(extracted_dir):
        for file in sorted(files):
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, extracted_dir)
            if arcname != "mimetype" and not file.endswith(".DS_Store"):
                epub_files.append((file_path, arcname))
    
    with zipfile.ZipFile(output_epub, 'w') as zip_ref:
        # Ensure mimetype is first and uncompressed
        if os.path.exists(mimetype_path):
            zip_ref.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)
        
        # Add remaining files
        for file_path, arcname in epub_files:
            zip_ref.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)

def zip_epub_directory(epub_path):
    """If the EPUB is a directory, compress it into a ZIP archive before processing."""
    if os.path.isdir(epub_path):
        temp_zip = epub_path.rstrip('/') + ".zip"
        shutil.make_archive(epub_path, 'zip', epub_path)
        shutil.rmtree(epub_path)
        os.rename(temp_zip, epub_path)

def process_epub(epub_path):
    """Process an EPUB file: ensure proper ZIP format, extract, clean, and rebuild if needed."""
    if not os.path.exists(epub_path):
        print(f"❌ File not found: {epub_path}")
        return
    
    print(f"Processing: {epub_path}")
    
    zip_epub_directory(epub_path)  # Ensure it's a proper ZIP file
    
    if not is_valid_epub(epub_path):
        print(f"Skipping corrupt file: {epub_path}")
        return
    
    backup_path = epub_path + ".bak"
    shutil.copy(epub_path, backup_path)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        remove_unwanted_metadata(temp_dir)
        
        temp_epub = epub_path + ".tmp"
        rebuild_epub(temp_dir, temp_epub)
        
        if is_valid_epub(temp_epub):
            shutil.move(temp_epub, epub_path)
            os.remove(backup_path)
            print(f"✔️ Cleaned: {epub_path}")
        else:
            print(f"❌ Failed: {epub_path} (restoring backup)")
            shutil.move(backup_path, epub_path)
            if os.path.exists(temp_epub):
                os.remove(temp_epub)

def main():
    """Process all EPUB files in the current directory."""
    for epub_file in os.listdir():
        if epub_file.endswith(".epub") and not epub_file.startswith("."):
            process_epub(os.path.abspath(epub_file))

if __name__ == "__main__":
    main()
