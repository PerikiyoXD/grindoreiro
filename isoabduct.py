import argparse
import requests
import base64
import sys
import os


def make_request_with_user_agent(url, user_agent):
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"/!\\ Error: {e}")
        sys.exit()
    return response


def download_iso(url, output_dir, user_agent):
    print(f"Downloading ISO from {url}...")
    response = make_request_with_user_agent(url, user_agent)
    print("Downloaded")
    file_name = os.path.basename(url)
    out_file = os.path.join(output_dir, file_name)
    print(f"Saving as {out_file}...")
    with open(out_file, "wb") as f:
        f.write(response.content)
    print("Saved to disk")
    return out_file


def debase64(data):
    return base64.b64decode(data)


def main():
    print("""
          @
    ISO (/^\)BDUCT!
        /(o)\ <[Gather and decode]
       /_____\\""")
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to download and decode")
    parser.add_argument("-o", "--output-dir", help="Output directory", default=".")
    parser.add_argument("-i", "--input-file", help="Use local fake iso")
    parser.add_argument("-u", "--user-agent", help="Custom user agent", default="Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0")
    args = parser.parse_args()

    print(f"Output: {args.output_dir}")

    # Gather response from the URL
    if args.input_file:
        iso_file = args.input_file
        print(f"Using {args.input_file} (Local file), skipping download!")
    else:
        iso_file = download_iso(args.url, args.output_dir, args.user_agent)

    with open(iso_file, "rb") as f:
        data = f.read()

    print("First Base64 decode...")
    decoded = debase64(data)
    with open(os.path.join(args.output_dir, "encoded.b64"), "wb") as f:
        f.write(decoded)
    print("OK")
    print("Second Base64 decode...")
    decoded = debase64(decoded)
    with open(os.path.join(args.output_dir, "decoded.zip"), "wb") as f:
        f.write(decoded)
    print("OK")
    print("Decoded zip recovered successfully")


if __name__ == "__main__":
    main()
