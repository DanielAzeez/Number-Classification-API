import json

def lambda_handler(event, context):
    # Retrieve the 'number' query string parameter
    try:
        number_str = event.get('queryStringParameters', {}).get('number', None)
        
        if not number_str or not number_str.isdigit():
            # If the 'number' is not provided or is invalid, return a 400 error with the template format
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': True,
                    'message': 'Invalid input. Please provide a valid number.'
                })
            }
        
        # Convert the 'number' parameter to an integer
        number = int(number_str)
        
        # Initialize the response dictionary with properties and fun fact
        response = {
            'number': number,
            'properties': [],
            'is_prime': is_prime(number),
            'is_perfect': is_perfect(number),
            'digit_sum': sum(int(digit) for digit in str(number)),
            'fun_fact': get_fun_fact(number)
        }
        
        # Add Armstrong number classification and even/odd logic
        if is_armstrong(number):
            response['properties'].append('armstrong')
        
        if number % 2 == 0:
            response['properties'].append('even')
        else:
            response['properties'].append('odd')
        
        # Return the response
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    
    except Exception as e:
        # Catch unexpected errors and return a generic error message in the 500 response
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': True,
                'message': f"An unexpected error occurred: {str(e)}"
            })
        }

# Helper function to check if a number is Armstrong
def is_armstrong(num):
    num_str = str(num)
    num_digits = len(num_str)
    sum_of_powers = sum(int(digit) ** num_digits for digit in num_str)
    return sum_of_powers == num

# Helper function to check if a number is prime
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Helper function to check if a number is perfect
def is_perfect(num):
    divisors_sum = sum(i for i in range(1, num) if num % i == 0)
    return divisors_sum == num

# Fun fact generator (replace with your logic)
def get_fun_fact(number):
    if is_armstrong(number):
        return f"{number} is an Armstrong number because " + " + ".join([f"{digit}^{len(str(number))}" for digit in str(number)]) + f" = {number}"
    return f"{number} is an interesting number!"
