This script cleans EPUB files by removing Apple-specific metadata and rebuilding them into a valid EPUB format.  
Place your .epub files
Copy any EPUB files you want to clean into the same directory as the script.

All care and no responsibility 

The script will:
Verify the EPUB is a valid ZIP archive
Remove unwanted Apple metadata (iTunesMetadata.plist, com.apple.ibooks.display-options.xml)
Rebuild the EPUB with the correct mimetype placement
Keep a backup (.bak) until the cleaned file is successfully validated
Check results
Cleaned EPUBs will overwrite the originals.
If cleaning fails, the backup will be restored automatically.

Notes
Works on all .epub files in the current directory.
Hidden files and .DS_Store are ignored.
Original files are replaced, but a .bak backup is created during processing.
