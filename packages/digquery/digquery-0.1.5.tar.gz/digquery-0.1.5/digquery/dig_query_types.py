#!/usr/bin/env python3
import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode('utf-8')

def get_query_types(domain):
    query_types = ['TXT', 'A', 'MX', 'NS']  # Add more query types if needed
    query_results = {}

    for query_type in query_types:
        command = f"dig +noall +answer {domain} -t {query_type}"
        output = run_command(command)
        query_results[query_type] = output.strip()

    return query_results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dig_query_types.py <domain>")
    else:
        domain = sys.argv[1]
        results = get_query_types(domain)

        for query_type, result in results.items():
            print("====================================================")
            print(f"dig query for domain: {domain}, type: {query_type}")
            print("====================================================")
            print(result)
            print()
def main():
    if len(sys.argv) != 2:
        print("Usage: digquery <domain>")
    else:
        domain = sys.argv[1]
        results = get_query_types(domain)

        for query_type, result in results.items():
            print("====================================")
            print(f"dig query for domain: {domain}, type: {query_type}")
            print("====================================")
            print(result)
            print()

if __name__ == "__main__":
    main()
