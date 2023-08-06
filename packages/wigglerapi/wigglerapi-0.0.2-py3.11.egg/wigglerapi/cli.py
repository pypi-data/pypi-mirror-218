import argparse
import os

def main():
  
    parser = argparse.ArgumentParser(prog ='wiggler', description ='WiggleR API')

    parser.add_argument('-s', '--server', action='start_server')
    
    args = parser.parse_args()
  
    if args.start_server: 
        os.system(f"uvicorn main:app --reload --host 0.0.0.0")
