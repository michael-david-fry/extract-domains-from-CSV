# Domain Extractor Script

This script extracts domains (including subdomains) from a CSV file and filters out email addresses. It's designed to be run in a Linux terminal environment, with support for colored output to differentiate between newly added domains and duplicates.

## Features

- Processes CSV files to extract domains.
- Filters out email addresses and HTML tags.
- Supports colored terminal output for added domains (green) and skipped duplicates (red).
- Prints the total count of unique domains processed to the console.
- Allows user interaction for selecting the CSV file and specifying the output file name.

## Requirements

- Python 3.x
- `tldextract` library
- `termcolor` library

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install the required Python libraries:

```bash
pip install tldextract termcolor
```

## Usage

1. Place the script in the same directory as your CSV files.
2. Run the script using Python:

```bash
python3 domain_extractor.py
```

3. Follow the prompts to select a CSV file and specify the name of the output file.

4. If you want verbose output, include the `-v` or `--verbose` flag when running the script:

```bash
python3 domain_extractor.py --verbose
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

## License

This script is provided under the MIT License. See the LICENSE file for more details.
