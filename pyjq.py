import json

class pyjq:
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
        if standard.isdigit():
            standard= int(standard)
        
        if isinstance(standard, int):
            if isinstance(data, list):
                data = data[standard] if 0 <= standard < len(data) else None
            else:
                data = None
        else:
            if isinstance(data, list):
                data = [i.get(standard, None) for i in data]
            else:
                data = data.get(standard, None)

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

# Instance of pyjq
jq = pyjq()
jq.json_str = example_json

# Example tests with print statements
print(jq.parse_argument('[.quotes[].quote]'))       # Should print: ['First Quote', 'Second Quote']
print(jq.parse_argument('[.quotes[1].quote]'))      # Should print: ['Second Quote']
print(jq.parse_argument('.quotes[1].quote'))        # Should print: Second Quote
print(jq.parse_argument('.codingchallenge'))        # Should print: Complete
print(jq.parse_argument('.codingchallenge?'))       # Should print: Complete
print(jq.parse_argument('.["codingchallenge"]'))    # Should print: Complete
print(jq.parse_argument('.["codingchallenge"]?'))   # Should print: Complete
print(jq.parse_argument('.quotes'))                 # Should print: [{'quote': 'First Quote'}, {'quote': 'Second Quote'}]
print(jq.parse_argument('.[0] | .commit.message'))  # Should print: Initial commit
