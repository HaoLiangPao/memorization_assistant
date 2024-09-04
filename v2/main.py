import json
import os
import opencc
from datetime import datetime  # Import datetime module for the current date

# Initialize OpenCC converter (Traditional to Simplified Chinese)
converter = opencc.OpenCC('t2s.json')  # Adjust the config if needed

# New template for the markdown file
TEMPLATE = """---
tags:
{tags}
Created: {created}
---

# {title}

**Author**: {author}

---

## Poem:

{paragraphs}

---

## Notes:

- [ ] Add your notes here
- [ ] Observations about the poem

## Memorization Status:

- [ ] First review completed
- [ ] Second review scheduled
"""

# Function to generate a markdown file for a poem
def generate_markdown(poem, output_dir):
    title = converter.convert(poem['title'])
    author = f"#中文/诗人/{converter.convert(poem['author'])}"
    paragraphs = converter.convert("\n\n".join(poem['paragraphs']))

    # Convert tags
    tags_converted = [converter.convert(tag) for tag in poem['tags']]
    tags_formatted = "\n".join([f"  - 中文/{tag}" for tag in tags_converted])

    # Get today's date in YYYY-MM-DD format
    today = datetime.today().strftime('%Y-%m-%d')

    # Format the markdown content using the new template, including today's date
    content = TEMPLATE.format(
        title=title,
        author=author,
        paragraphs=paragraphs,
        tags=tags_formatted,
        created=today  # Insert today's date into the Created field
    )

    # Generate a valid file name from the poem title
    file_name = f"{title.replace(' ', '_')}.md"

    # Write the content to a markdown file
    with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Generated: {file_name}")


# Function to load the poems from a JSON file
def load_poems_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        poem_data = json.load(file)
    return poem_data


# Function to generate markdown files for each poem
def generate_markdown_files(json_file, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load poems from the JSON file
    poems = load_poems_from_json(json_file)

    # Generate markdown files for each poem
    for poem in poems:
        generate_markdown(poem, output_dir)


# Main script execution
if __name__ == "__main__":
    poem_json_file = "poem_simple.json"  # Replace with your actual path
    output_directory = "poems_md"  # Directory where markdown files will be saved

    # Generate markdown files
    generate_markdown_files(poem_json_file, output_directory)