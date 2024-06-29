import json

class pyjq:

    def __init__(self, json_str):
        self.comma = ","
        self.quotes = ["'", '"']
        self.open = ["{", "["]
        self.close = ["}", "]"]
        self.level = 0
        self.spl_char = ["{", "}", "[", "]"]
        self.json_str = json_str
        self.default_space = 2


    def leave_space(self):
        """
        Returns a string of spaces corresponding to the current indentation level.
        Used to format the output with current amount of indentation.
        """
        return " " * self.level


    def pretty_print(self):
        """
        Iterates through the json string, character by character and builds a pretty-printed json.
        The current variable holds the current state of the formatted json string.
        """
        index = 0
        current = ""
        """
        When a quote character is encountered, code enters a loop to cpature all characters until the matching closing quote is found.
        The captured text is enclosed in quotes and appened to current.

        When an opening brace { or [ is encountered, it is appended to current.
        The indentation level is increased by default space.
        A newline and appropriate amount of spaces are added to the current.

        When a closing brace } or ] is found, it checks if the previous character was not a closing brace.
        If not, it addes a newline to the current.
        The indentation level is decreased.
        The closing brace is added to the current, along with appropriate space.
        If the the next character is not a comma, a newline and appropriate spacing are added.

        When a comma is encountered, a newline is added.
        If the previous character was not a closing brace, the appropriate space is added for the next line.
        """
        while index < len(self.json_str):
            if self.json_str[index] in self.quotes:
                text = ""
                index += 1
                while self.json_str[index] not in self.quotes:
                    text += self.json_str[index]
                    index += 1
                current += "'" + text + "'"

            elif self.json_str[index] in self.open:
                current += self.json_str[index]
                self.level += self.default_space
                if (index + 1 < len(self.json_str) and self.json_str[index + 1] != self.comma):
                    current += "\n"
                    current += self.leave_space()

            elif self.json_str[index] in self.close:
                if self.json_str[index-1] not in self.close:
                    current += "\n"
                self.level -= self.default_space
                current += self.leave_space()
                current += self.json_str[index]
                if (index + 1 < len(self.json_str) and self.json_str[index + 1 != self.comma]):
                    current += "\n"
                    current += self.leave_space()

            else:
                current += self.json_str[index]
                if self.json_str[index] == self.comma:
                    current += "\n"
                if self.json_str[index - 1] != self.close:
                    current += self.leave_space()
            index += 1
        print(current)
        return 0
    
    
    def parse_argument(self, pyjq_arg):
        """
        Check if the argument starts and ends with [], which indicates result should be a list.
        Remove [, ] if a list result is expected.
        Load json data from the json_str.
        Split pyjq argument by | to handle multiple filters.
        Iterate over each filter and apply it to the data.
        Return the data wrapped in a list if needed, else return it as-is.
        """
        as_list = pyjq_arg.startswith('[') and pyjq_arg.endswith(']')
        if as_list:
            pyjq_arg = pyjq_arg[1:-1]
        
        data = json.loads(self.json_str)
        
        for filter_part in pyjq_arg.split('|'):
            data = self.apply_filter(data, filter_part)
        
        return [data] if as_list else data
    
    
    def extract_data(self, data, standard):
        """
        Convert the key to an integer if it represents an array index.
        Access the array elements if the key is a valid index, else return None.
        If the data is a list, extract the specified field from each element.
        If the data is a dictionary, extract the value for the specified key.
        Return the extracted data.
        """
        if data is None:
            return None

        if standard.isdigit():
            standard = int(standard)
        
        if isinstance(standard, int):
            if isinstance(data, list):
                data = data[standard] if 0 <= standard < len(data) else None
            else:
                data = None
        else:
            if isinstance(data, list):
                data = [i.get(standard, None) for i in data if isinstance(i, dict)]
            elif isinstance(data, dict):
                data = data.get(standard, None)
            else:
                data = None

        return data
    

    def apply_filter(self, data, filter_part):
        """
        If the filter is ., it means no filtering is needed.
        Split the filter by . and process each part -- skip the first empty element due to leading dot.
        Remove trailing ? if present, which indicates an optional field.
        Strip the outer [ and ] and process filter as array index or key.
        Handle cases where the filter is in the format field[index], splitting it into two parts and processing each part separately.
        Process standard field names.
        """
        if data is None:
            return None

        if filter_part == '.':
            return data
        
        for part in filter_part.split('.')[1:]:
            part = part.strip()
            
            if part.endswith('?'):
                part = part[:-1]
            
            if part.startswith('[') and part.endswith(']'):
                part = part[1:-1]
                data = self.extract_data(data, part)
            
            elif str(part).endswith(']'):
                a, b = part.strip(']').split('[')
                data = self.extract_data(data, a)
                if b:
                    data = self.extract_data(data, b)
            
            else:
                data = self.extract_data(data, part)

        return data   


# Example
example_json = '''
{
    "quotes": [
        {"quote": "First Quote"},
        {"quote": "Second Quote"}
    ],
    "codingchallenge": "Complete",
    "commit": {
        "message": "Initial commit"
    }
}
'''

# Creating an instance of pyjq
jq = pyjq(example_json)

# Testing pretty_print
print("Pretty Printed JSON:")
jq.pretty_print()

# Testing parse_argument
print("\nParsed Arguments:")
print(jq.parse_argument('[.quotes[].quote]'))       # Should print: ['First Quote', 'Second Quote']
print(jq.parse_argument('[.quotes[1].quote]'))      # Should print: ['Second Quote']
print(jq.parse_argument('.quotes[1].quote'))        # Should print: Second Quote
print(jq.parse_argument('.codingchallenge'))        # Should print: Complete
print(jq.parse_argument('.codingchallenge?'))       # Should print: Complete
print(jq.parse_argument('.["codingchallenge"]'))    # Should print: Complete
print(jq.parse_argument('.["codingchallenge"]?'))   # Should print: Complete
print(jq.parse_argument('.quotes'))                 # Should print: [{'quote': 'First Quote'}, {'quote': 'Second Quote'}]
print(jq.parse_argument('.commit.message'))  
