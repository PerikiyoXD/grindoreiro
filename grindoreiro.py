import subprocess
import base64
import zipfile
import hashlib
import argparse
import os
import shutil
import re
import sys

# Path of dark.exe (Wix toolkit) https://wixtoolset.org/releases/
dark = "./tools/wix/dark.exe"

# Project (file) path
projects = "./samples/"

output_directory = "./output/"


def mkdir(nam):
    try:
        os.makedirs(nam)
    except:
        #print(f"|INFO| {sys.exc_info()[0]} Directory {nam} already exists!")
        return
def extract_contents(zip_file, out):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        mkdir(out)
        zip_ref.extractall(out)
        

def initProject():
    print("x")

def do_sha256(_bytes):
    return hashlib.sha256(_bytes).hexdigest()



if __name__ == "__main__":
    print("""
   _____      _           _                _           
  / ____|    (_)         | |              (_)          
 | |  __ _ __ _ _ __   __| | ___  _ __ ___ _ _ __ ___  
 | | |_ | '__| | '_ \ / _` |/ _ \| '__/ _ \ | '__/ _ \ 
 | |__| | |  | | | | | (_| | (_) | | |  __/ | | | (_) |
  \_____|_|  |_|_| |_|\__,_|\___/|_|  \___|_|_|  \___/ 
                              \Grinding grandoreiro!\
    """)
    
    mkdir(projects)
    mkdir(output_directory)

    parser = argparse.ArgumentParser()
    parser.add_argument("sample", help="Name of the sample inside ./samples/ to extract")
    args = parser.parse_args()
    
    
    
    # Check if dark is installed
    if not os.path.isfile(dark):
        print(f"Error: dark.exe wasn't found @ '{dark}'. Please, download WiX and try again")
        sys.exit(1)
    
    
    # Input file name from projects directory
    project_file_name = f"{projects}{args.sample}"
    
    # Open and read basic data from the file
    with open(project_file_name, "rb", buffering=0) as project_file:
        project_file_bytes = project_file.readall()
        project_file_sha256 = do_sha256(project_file_bytes)
        print(f"| Filename: {project_file_name}")
        print(f"| SHA256: {project_file_sha256}")
       
       
    # Define steps and paths all together if possible
    project_directory = f"{projects}{project_file_sha256}/"
    step00 = f"{project_directory}00_extract/"
    step01 = f"{project_directory}01_msi_output/"
    step02 = f"{project_directory}02_msi_script/"
    step03 = f"{project_directory}03_dll/"
    step04 = f"{project_directory}04_iso/"
    step05 = f"{project_directory}05_exe/"
    
    # create folder with sha256 of zip as foldername
    mkdir(project_directory)
        
    # extractall
    print(f"> Extracting contents from ZIP @ {project_file_name}...")
    extract_contents(project_file_name, step00)
    print(f"> Extracted!")
    
    
    # find msi name
    for (_, _, fn) in os.walk(step00):
        for dir_file in fn:
            if dir_file.endswith(".msi"):
                msi_filename = dir_file
    
    # Get MSI file path
    msi_path = f"{step00}{msi_filename}"
    print(f"! Found MSI path @ {msi_path}")

    # make step directories
    mkdir(step01) 
    mkdir(step02)
    mkdir(step03)
    mkdir(step04)
    
    
    # run dark
    print(f"> Extracting contents from MSI @ {step02}...")
    print("--------------------------------")
    subprocess.run([f"{dark}", msi_path, "-x", step01, "-o", step02])
    print("--------------------------------")
    print("> Extracted MSI contents!")
    
    # Find dlls in step01
    files = list()
    names = list()
    
    # Get best dll candidate from step01, not aicustact.dll!
    for (dp, dn, fn) in os.walk(step01):
        for dir_file in fn:
            if dir_file.find("dll") is not -1:
                if not "aicustact" in dir_file:
                    dll = (f"{dp}/{dir_file}")
                    dll_name = (f"{dir_file}")
            
    dll_path = f"{step03}{dll_name}"
    

    # Copy dll from step01 to step03
    print(f"> Copying DLL {dll} -> {dll_path}...")
    shutil.copy(dll,dll_path)
    print("> Copied DLL!")
    
    # Extract strings
    print(f"> Extracting strings (UTF-8, UTF-16) from {dll_path}...")
    print("--------------------------------")
    subprocess.run(["python", "stringripper.py", dll_path ], shell=True)
    print("--------------------------------")
    print("> Extracted strings!")
    
    # Find urls, possibly malware!
    
    strings_path = f"{dll_path}.strings"
    
    urls = list()
    
    print("> Looking for download URLs...")
    with open(strings_path,"r") as strings:
        allstrings = strings.readlines()
        
        print("> HTTP Results: ")
        for string in allstrings:
            pattern = re.compile("(http://.+\..+)")
            result = pattern.search(string)
            if result is not None:
                print(result.group())
                urls.append(result.group())
                    
        print("> HTTPS Results: ")
        for string in allstrings:
            pattern = re.compile("(https://.+\..+)")
            result = pattern.search(string)
            if result is not None:
                print(result.group())
                urls.append(result.group())
          
    print("--------------------------------")
    for i in range(len(urls)): 
        print(urls[i])
    print("--------------------------------")
        
        
    download_url_file = f"{step04}download.txt"
    cnc_url_file = f"{step04}cnc.txt"
    
        
    # Find C&C URL
    for url in urls:
        if "5050/index.php" in url:
            cnc_url = url
            break    
    
    print("> Saving C&C server URL")
    
    with open(cnc_url_file,"w") as f:
        f.write(cnc_url) 
        
    # Find download URL (iso)
    for url in urls:
        if "iso" in url:
            iso_download_url = url
            break
    
    print("> Saving fake ISO download URL")
    
    with open(download_url_file,"w") as f:
        f.write(iso_download_url) 
     
    print(f"iso_download_url={iso_download_url}")
     
    iso_file = f"{step04}{iso_download_url.rsplit('/', 1)[-1]}"
     
    print(f"Looking for cached {iso_file}...")
     
    # Check if any ISO is already cached. (Sometimes the files won't be there anymore)
    if os.path.isfile(iso_file):
        print("> Local ISO found! Skipping download on IsoAbduct")
        print(f"--------------------------------")
        subprocess.run(["python", "isoabduct.py", iso_download_url, "-o", step04, "-i", iso_file], shell=True)
        print(f"--------------------------------")
    else: 
        # Run IsoAbduct
        print(f"> No local ISO found! Gathering ISO...")
        print(f"--------------------------------")
        subprocess.run(["python", "isoabduct.py", iso_download_url, "-o", step04], shell=True)
        print(f"--------------------------------")
        
    print(f"> Recovered ZIP file from ISO")
    print(f"> Extracting...")
    mkdir(step05)
    extract_contents(f"{step04}decoded.zip", step05)
    
    for (dp, dn, fn) in os.walk(step05):
        for dir_file in fn:
            if dir_file.endswith("exe"):
                executable = dir_file
    
    shutil.copy(f"{step05}{executable}" , f"{output_directory}{executable}")
    
    print("Finished.")
    
    
