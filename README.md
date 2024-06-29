## jqpy
Implementation of [jq](https://jqlang.github.io/jq/) tool in python.


### Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/itsknk/jqpy.git
   cd jqpy
   ```

2. Setup the `jqpy` command by adding the following function to your shell configuration file (`~/.bash_profile`, `~/.zshrc`, etc.):
   ```bash
   # jqpy function
   jqpy() {
       # Read input from stdin
       input=$(cat)

       # Execute the jqpy script, passing the input and the filter as arguments
       python /path/to/jqpy.py "$input" "$1"
   }
   ```

   Ensure to replace `/path/to/jqpy.py` with the actual path where `pyjq.py` is located.

3. Source your shell configuration file to apply the changes:
   ```bash
   source ~/.bash_profile   # or ~/.zshrc for zsh users
   ```

### Usage

#### Examples:

- **Fetch and filter JSON data from an API endpoint:**
  ```bash
  curl -s 'https://api.github.com/repos/CodingChallegesFYI/SharedSolutions/commits?per_page=3' | jqpy '.[0]'
  ```
  This example fetches the latest commit from the specified GitHub repository.

- **Filter JSON data from a local file:**
  ```bash
  cat data.json | jqpy '.key'
  ```
  Replace `data.json` with your local JSON file. This command filters the JSON data based on the specified key.

- **Retrieve specific fields from JSON data:**
  ```bash
  curl -s 'https://dummyjson.com/quotes?limit=2' | jqpy '.quotes'
  ```
  This example fetches quotes from a dummy JSON API and extracts the `quotes` field.

### Arguments

- **Input**: JSON data piped into jqpy from stdin.
- **Filter**: A jq-like filter expression to manipulate the JSON data.

### Features

- **Parsing**: Load JSON data from stdin or file.
- **Filtering**: Apply filters to extract specific fields or elements.
- **Pretty Printing**: Format JSON output for readability.

### Dependencies

- Python 3.x
- `json` library

### Motivation
John Crickett's coding challenge. [Challenge 34](https://codingchallenges.fyi/challenges/challenge-jq) involves building a jq tool.
