import argparse
import requests
import base64

def makeRequestWithUseragent(url, useragent):
    request_headers = { "User-Agent" : useragent }
    response = None
    try:
        response = requests.get(url, headers=request_headers)
    except requests.exceptions.Timeout:
        print("/!\\ Got a timeout. Probably the host is down. Check yourself!")
        sys.exit()
    except requests.exceptions.TooManyRedirects:
        print("/!\\ Too many redirects. Probably the host is avoiding you! Check user agent!")
        sys.exit()
    except requests.exceptions.RequestException as e:
        print("/!\\ There was an ambiguous exception that occurred while handling your request")
        sys.exit()
    except requests.ConnectionError:
        print("/!\\ There was a connection error!")
        sys.exit()
    return response

def debase64(data):
    return base64.b64decode(data)
    
def download_iso(url):
    print(f"Downloading ISO from {url}...")
    resp = makeRequestWithUseragent(url, args.u)
    print("Downloaded")
    file_name = url.rsplit('/', 1)[-1]
    print(f"Saving as {file_name}...")
    out_file = f"{args.o}{file_name}"
    with open(out_file, "w") as f:
            f.write(resp.text)
    print("Saved to disk")
    return out_file

if __name__ == "__main__":
    print("""
          @
    ISO (/^\)BDUCT!
        /(o)\ <[Gather and decode]
       /_____\\""")

    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="URL to download and decode")
    parser.add_argument("-o", help="Output directory", default=".")
    parser.add_argument("-i", help="Use local fake iso")
    parser.add_argument("-u", help="Custom user agent", default="Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0")
    
    args = parser.parse_args()
            
    print(f"Output: {args.o}")
    
    # Gather response from the URL
    if args.i:
        iso_file = args.i
        print(f"Using {args.i} (Local file), skipping download!")
    else:
        iso_file = download_iso(args.URL)
           
    with open(iso_file, "r") as f:
        data = f.read()
    
    print("First Base64 decode...")
    decoded = base64.b64decode(data)
    with open(f"{args.o}encoded.b64", "wb") as f:
        f.write(decoded)  
    print("OK")       
    print("Second Base64 decode...")
    decoded = base64.b64decode(decoded)
    with open(f"{args.o}decoded.zip", "wb") as f:
        f.write(decoded) 
    print("OK") 
    print("Decoded zip recovered succesfully")
        