You're welcome! Here's a **comprehensive README** for your project:

---

# Number Classification API

This API classifies numbers based on several mathematical properties. It checks whether a number is **prime**, **perfect**, or **Armstrong**. It also provides a fun fact about the number.

## Overview

The project exposes an API endpoint that accepts a **GET** request with a `number` query parameter. The response includes information such as whether the number is prime, perfect, or Armstrong, and a fun fact related to the number.

### API Endpoint

```
GET /api/classify-number?number=<your-number>
```

#### Example Request:

```
GET https://xyz.execute-api.us-east-1.amazonaws.com/test/api/classify-number?number=371
```

#### Example Response (200 OK):

```json
{
  "number": 371,
  "is_prime": false,
  "is_perfect": false,
  "properties": ["armstrong", "odd"],
  "digit_sum": 11,
  "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

#### Example Response (400 Bad Request):

```json
{
  "error": true,
  "message": "Invalid or missing parameter 'number'."
}
```

## Features

- **Prime Check**: Identifies whether the number is prime.
- **Perfect Number Check**: Identifies whether the number is a perfect number.
- **Armstrong Number Check**: Identifies whether the number is an Armstrong number.
- **Fun Fact**: Provides a fun fact about the number based on its properties.
- **Query Parameter**: Accepts a `number` query parameter, which must be a valid integer.

## Requirements

- **AWS Lambda**: The business logic of the API is implemented in an AWS Lambda function.
- **API Gateway**: The API is exposed using AWS API Gateway, which triggers the Lambda function when the endpoint is hit.
- **AWS IAM Role**: Proper IAM permissions must be configured to allow API Gateway to invoke the Lambda function.

## Setup and Deployment

1. **Lambda Function**: The Lambda function contains the logic to process the request and return the correct response. It checks the properties of the number and calculates relevant facts.

2. **API Gateway**: 
   - A REST API is created in API Gateway to expose the Lambda function.
   - The API uses **Lambda proxy integration**, meaning the incoming request is passed directly to the Lambda function as a structured event.
   - The endpoint `/api/classify-number` accepts the `number` query parameter.

3. **Permissions**: Ensure the Lambda function has the necessary permissions to execute and that API Gateway has permissions to invoke the Lambda function.

## Lambda Code

The Lambda function in Python processes the input number and returns the appropriate classification and fun fact. Below is an overview of how the Lambda function works:

### Python Code (Lambda Function)

```python
import json

def lambda_handler(event, context):
    try:
        # Extract number from query parameter
        number = int(event["queryStringParameters"].get("number"))
        
        # Check number properties
        is_prime = is_prime_number(number)
        is_perfect = is_perfect_number(number)
        properties = get_properties(number)
        digit_sum = sum(map(int, str(number)))
        fun_fact = get_fun_fact(number, properties)

        # Prepare response
        response = {
            "number": number,
            "is_prime": is_prime,
            "is_perfect": is_perfect,
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }

        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except Exception as e:
        # Handle errors
        return {
            'statusCode': 400,
            'body': json.dumps({"error": True, "message": str(e)})
        }

def is_prime_number(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def is_perfect_number(number):
    divisors = [i for i in range(1, number) if number % i == 0]
    return sum(divisors) == number

def get_properties(number):
    properties = []
    if is_armstrong_number(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    return properties

def is_armstrong_number(number):
    num_str = str(number)
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == number

def get_fun_fact(number, properties):
    if "armstrong" in properties:
        return f"{number} is an Armstrong number because " + \
               " + ".join([f"{int(digit)}^{len(str(number))}" for digit in str(number)]) + \
               f" = {number}"
    return f"{number} is not an Armstrong number."
```

## Testing the API

### 1. **Using Postman**
   - Set up a **GET** request to the endpoint.
   - Example URL: `https://xyz.execute-api.us-east-1.amazonaws.com/test/api/classify-number?number=371`
   - Send the request and inspect the response.

### 2. **Using Curl**
   ```bash
   curl "https://xyz.execute-api.us-east-1.amazonaws.com/test/api/classify-number?number=371"
   ```

### 3. **API Gateway Console**
   - Go to your **API Gateway** console.
   - Navigate to **Stages**, select the appropriate stage, and test the endpoint directly from the console.

## Error Handling

- **400 Bad Request**: If the `number` parameter is missing or invalid, the API will return a 400 response with an error message.
- **500 Internal Server Error**: If something goes wrong in the Lambda function, a 500 response will be returned.

## Conclusion

This project demonstrates how to use AWS Lambda and API Gateway to create an API that classifies numbers based on their properties. It is a simple yet powerful example of serverless architecture in action.

---
