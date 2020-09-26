import sys
import re
import argparse

chars = br"A-Za-z0-9/\-:.,_$%'()[\]<> "
chars2 = r"A-Za-z0-9/\-:.,_$%'()[\]<> "
shortest_run = 4

regexp = b'[%s]{%d,}' % (chars, shortest_run)
regexp2 = '[%s]{%d,}' % (chars2, shortest_run)
pattern = re.compile(regexp)
pattern2 = re.compile(regexp2)

def process(stream):
    return pattern.findall(stream)
def process2(stream):
    return pattern2.findall(stream)

if __name__ == "__main__":
    print("""| String Ripper v1.0 /w love PXD |""")
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The file to search strings")
    args = parser.parse_args()
    #print(args.file)
    file = open(args.file, "rb")
    print(f"""| Processing: {args.file}...""")
    #print(file)
    xs = bytearray()
    #print(xs)
    data = file.read()
    utf16_data = data.decode('UTF-16', errors='ignore')
    output_file = f"{args.file}.strings"
    # Open output file
    with open(output_file, "w") as f:
        # Search basic strings
        for found_str in process(data):
            str = f"{found_str.decode('ANSI')}\n"
            f.write(str)
        # Search UTF-16 strings
        for found_str in process2(utf16_data):
            str = f"{found_str}\n"
            f.write(str)
    
    # Done
    print(f"""| Done! Generated strings file: {output_file}!""")   