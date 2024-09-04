import random
import argparse
from memory import load_poems_from_json


# Function to randomly display a poem
def random_display_poem(json_poem_file):
    # Load poems from the JSON file
    poems = load_poems_from_json(json_poem_file)

    # Randomly select a poem
    poem = random.choice(poems)

    # Display the poem information
    print(f"\nTitle: {poem.title}")
    print(f"Author: {poem.author}")
    print("\n".join(poem.content))
    print("\nTags: ", ", ".join(poem.tags))


# Main function for the CLI
def main():
    parser = argparse.ArgumentParser(description="Memorization CLI Application")

    # Add an argument to display a random poem
    parser.add_argument(
        '-rd', '--random-display',
        action='store_true',
        help="Display a random poem from the dataset"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Define the path to the poem JSON file
    poem_json_file = "poems.json"  # Replace with the actual path to your JSON file

    # If the random display flag is set, show a random poem
    if args.random_display:
        random_display_poem(poem_json_file)

if __name__ == "__main__":
    main()