import json

def lambda_handler(event, context):
    try:
        number_str = event.get('queryStringParameters', {}).get('number', None)

        if number_str is None:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": True, "message": "Number parameter is missing"})
            }

        try:
            number = float(number_str)
        except ValueError:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": True, "message": f"Invalid number: {number_str}", "number": number_str})
            }

        response = {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": [],
            "digit_sum": digit_sum(number),
            "fun_fact": get_fun_fact(number)
        }

        if is_armstrong(number):
            response["properties"].append("armstrong")
        if number % 2 == 0:
            response["properties"].append("even")
        else:
            response["properties"].append("odd")

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": True, "message": f"An unexpected error occurred: {str(e)}"})
        }
    except: #Inner exception handler must have an indented block
        pass #Do nothing, the outer except block already handles it.


def is_armstrong(num):
    num = abs(int(num))
    num_str = str(num)
    n = len(num_str)
    sum_of_powers = sum(int(digit)**n for digit in num_str)
    return sum_of_powers == num

def is_prime(num):
    num = abs(int(num))
    if num <= 1:
        return False
    for i in range(2, int(abs(num)**0.5) + 1):
        if num % i == 0:
            return False
    return True

def is_perfect(num):
    num = abs(int(num))
    if num <= 0:
        return False
    divisors_sum = sum(i for i in range(1, num) if num % i == 0)
    return divisors_sum == num

def digit_sum(number):
    num = abs(int(number))
    return sum(int(digit) for digit in str(num) if digit.isdigit())

def get_fun_fact(number):
    if is_armstrong(number):
        num_str = str(abs(int(number)))
        power_expression = " + ".join([f"{digit}^{len(num_str)}" for digit in num_str])
        return f"{number} is an Armstrong number because {power_expression} = {number}"
    return f"{number} is an interesting number!"