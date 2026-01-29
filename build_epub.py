import os
import subprocess

def main():
    chapters_dir = "chapters"
    output_file = "Franklin_Autobiography.epub"
    
    # Get all markdown files
    files = [f for f in os.listdir(chapters_dir) if f.endswith('.md')]
    
    # Sort files
    # We want 15_PRIMECHANIYA.md to be last, after 19_...
    # Standard sort might put it in the middle.
    
    def sort_key(filename):
        if "PRIMECHANIYA" in filename:
            return (999, filename) # Force to end
        return (0, filename)
        
    files.sort(key=sort_key)
    
    # Verify order (debug print)
    print("Files to be included:")
    for f in files:
        print(f)
        
    # Construct full paths
    file_paths = [os.path.join(chapters_dir, f) for f in files]
    
    # Pandoc command
    cmd = [
        "pandoc",
        "-o", output_file,
        "--metadata", "title=Автобиография Бенджамина Франклина",
        "--metadata", "creator=Benjamin Franklin",
        "--metadata", "lang=ru",
        "--toc" # Table of Contents
    ] + file_paths
    
    print("\nRunning pandoc...")
    try:
        subprocess.run(cmd, check=True)
        print(f"\nSuccessfully created {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running pandoc: {e}")
    except FileNotFoundError:
        print("Error: pandoc not found. Please install pandoc.")

if __name__ == "__main__":
    main()
