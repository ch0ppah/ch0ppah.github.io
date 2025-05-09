import os
import sys
import shutil
from pathlib import Path
from block_markdown import markdown_to_html_node


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)



def copy_files_recursive(source_dir, dest_dir):
    # Removes destination directly, ensures clean copy
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    # List all items in source directory
    items = os.listdir(source_dir)

    # Process items
    for item in items:
        # Structure filepaths in both directories
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        print(f" * Copied {source_path} to {dest_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_files_recursive(source_path, dest_path)

def extract_title(markdown):
    # Pull the h1 header and return it (first line starting with #)
    md_lines = markdown.splitlines()

    for line in md_lines:
        # Checks for the first line starting with a single #
        # AND checks to make sure the title isn't empty after slicing off
        # the '#' and stripping whitespace
        if line.startswith("# "):
            if len(line[2:].strip()) > 0:
                # Returns line without the `# ` & stripped whitespace
                return line[2:].strip()
            else:
                raise Exception("h1 header is empty")
    
    raise Exception("h1 header not found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path, "r")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    content = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    content = content.replace('href="/', 'href="' + basepath)
    content = content.replace('src="/', 'src="' + basepath)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

main()