import argparse
import os

def main():
  
    parser = argparse.ArgumentParser(prog ='wiggler', description ='WiggleR API')

    parser.add_argument('-s', '--server')
    
    args = parser.parse_args()
  
    if args.server:
        os.system(f"uvicorn main:app --reload --host 0.0.0.0")
