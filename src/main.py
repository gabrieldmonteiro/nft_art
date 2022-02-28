from functions import generate_art
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=1, help="Number of images to generate.")
    parser.add_argument("--c", type=str, help="Collection name for the art.")
    args = parser.parse_args()
    n = args.n
    collection_name = args.c

    for i in range(n):
        print("Generating: " + collection_name + "...")
        generate_art(collection_name, f"{collection_name}_image_{i}")
