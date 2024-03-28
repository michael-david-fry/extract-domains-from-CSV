
import argparse
import csv
import tldextract
import os
import sys
import glob
import re
from termcolor import colored

# Increase the maximum CSV field size limit
csv.field_size_limit(2**31 - 1)

def list_csv_files():
    csv_files = glob.glob('*.csv')
    if not csv_files:
        print("No CSV files found in the current directory.")
        sys.exit(1)
    print("\nFound CSV files:")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file}")
    return csv_files

def user_select_file(csv_files):
    while True:
        try:
            selection = int(input("Select the number of the CSV file you want to use: "))
            if 1 <= selection <= len(csv_files):
                return csv_files[selection - 1]
            else:
                print("Invalid selection. Please select a number from the list.")
        except ValueError:
            print("Please enter a numeric value.")

def clean_html_tags(text):
    return re.sub(r'<[^>]+>', '', text)

def extract_domains_and_filter_emails(csv_file_path, verbose=False):
    domains = set()
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for field in row:
                    potential_domains = re.split(r'[,;|]+', field)
                    for item in potential_domains:
                        for word in item.split():
                            word = clean_html_tags(word).lower()
                            if '@' in word:
                                continue
                            extracted = tldextract.extract(word)
                            if extracted.domain and extracted.suffix:
                                full_domain = f"{extracted.subdomain + '.' if extracted.subdomain else ''}{extracted.domain}.{extracted.suffix}"
                                cleaned_domain = full_domain.lstrip("*.()")
                                if cleaned_domain in domains:
                                    if verbose:
                                        print(colored(f"Duplicate domain skipped: {cleaned_domain}", 'red'))
                                else:
                                    if verbose:
                                        print(colored(f"{len(domains)+1} - Found and added domain: {cleaned_domain}", 'green'))
                                    domains.add(cleaned_domain)
    except FileNotFoundError:
        print(f"\U0001F50D Error: The file '{csv_file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"\U0001F6A8 An unexpected error occurred: {e}")
        sys.exit(1)
    return domains

def write_domains_to_file(domains, output_file_path):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for domain in sorted(domains):
                f.write(f"{domain}\n")
        print(f"\U00002705 Domains were successfully written to '{output_file_path}'.")
        print(f"Total unique domains added: {len(domains)}")
    except Exception as e:
        print(f"\U0000274C Failed to write to file: {e}")
        sys.exit(1)

def get_user_input():
    csv_files = list_csv_files()
    selected_csv_file = user_select_file(csv_files)
    output_file_path = input("Enter the name for the output file (it will be saved in the current directory): ")
    verbose = input("Would you like verbose output? (yes/no): ").lower() == 'yes'
    return selected_csv_file, output_file_path, verbose

def main():
    parser = argparse.ArgumentParser(description="Extract domains from a CSV file and filter out email addresses.")
    parser.add_argument("-o", "--output", help="Name of the output file", required=False)
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    args = parser.parse_args()
    
    if args.output:
        output_file_path = args.output
        verbose = args.verbose
        csv_files = list_csv_files()
        selected_csv_file = user_select_file(csv_files)
    else:
        selected_csv_file, output_file_path, verbose = get_user_input()
        
    if not os.path.isfile(selected_csv_file):
        print(f"\U0001F50D Error: The file '{selected_csv_file}' does not exist.")
        sys.exit(1)
        
    domains = extract_domains_and_filter_emails(selected_csv_file, verbose)
    write_domains_to_file(domains, output_file_path)

if __name__ == "__main__":
    main()
