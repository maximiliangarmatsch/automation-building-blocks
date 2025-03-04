import sys
import os  # Unused import

# This function intentionally contains several issues:
# - Function name not in snake_case (should be calc_sum)
# - Uses a magic number (100) without explanation
def CalcSum(a, b):
    result = a + b + 100  # Magic number added to the sum
    return result

# This function breaks naming conventions:
# - Parameter 'myList' should be 'my_list'
# - No type checks are done (multiplying non-numeric types will cause issues)
def processList(myList):
    results = []
    for item in myList:
        # This may lead to unexpected behavior with non-numeric types
        results.append(item * 2)
    return results

# Class name and method names are not following standard conventions:
# - Class name 'myClass' should be in CamelCase (MyClass)
# - Instance attribute 'Value' should be lowercase (value)
# - Method name 'displayValue' should be snake_case (display_value)
class myClass:
    def __init__(self, value):
        self.Value = value  # Incorrect attribute naming
    def displayValue(self):
        print("Value is: " + str(self.Value))

def main():
    a = 5
    b = 10
    total = CalcSum(a, b)
    print("Total:", total)
    
    # List with mixed types to trigger type-related warnings
    sample_data = [1, '2', 3, None, 4]
    processed = processList(sample_data)
    print("Processed Data:", processed)
    
    # Creating an object with non-standard class naming
    obj = myClass(200)
    obj.displayValue()

if __name__ == "__main__":
    main()
