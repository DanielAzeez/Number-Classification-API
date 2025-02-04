---

# **Number Classification API**

This project provides a serverless API built with AWS Lambda and API Gateway to classify numbers based on various mathematical properties. The API performs checks such as Armstrong number classification, prime check, perfect number check, and odd/even classification. It now supports both integer and floating-point inputs.

## **Features**
- **Armstrong Number Check**: Determines whether a number is an Armstrong number.
- **Prime Number Check**: Identifies if the number is prime.
- **Perfect Number Check**: Identifies if the number is perfect.
- **Odd/Even Check**: Determines whether the number is odd or even.
- **Fun Fact Generator**: Provides fun facts for each number, especially Armstrong numbers.

## **API Endpoint**

### **URL Format**

```
GET https://<your-api-id>.execute-api.<region>.amazonaws.com/<stage>/api/classify-number?number=<number>
```

Where:
- `<your-api-id>`: The API Gateway's unique ID.
- `<region>`: AWS region (e.g., `us-east-1`).
- `<stage>`: The deployment stage (e.g., `dev`, `prod`).
- `<number>`: The number to classify (e.g., `371` or `3.14`).

### **Example Request**

To classify the number `371`, visit the URL:

```
https://<your-api-id>.execute-api.<region>.amazonaws.com/<stage>/api/classify-number?number=371
```

To classify the floating-point number `3.14`, visit:

```
https://<your-api-id>.execute-api.<region>.amazonaws.com/<stage>/api/classify-number?number=3.14
```

### **Response Format**

#### **Success (HTTP Status: 200 OK)**

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

Explanation of fields:
- `number`: The input number.
- `is_prime`: Boolean indicating if the number is prime.
- `is_perfect`: Boolean indicating if the number is perfect.
- `properties`: List of properties (e.g., "armstrong", "even", "odd").
- `digit_sum`: Sum of digits of the number.
- `fun_fact`: A fun fact about the number (e.g., for Armstrong numbers, it shows the equation that proves it).

#### **Error (HTTP Status: 400 Bad Request)**

If the input is missing or invalid, the response will contain an error message:

```json
{
  "number": "invalid_input",
  "error": true,
  "message": "Invalid input. Please provide a valid number."
}
```

If the `number` parameter is invalid (e.g., not an integer or float), the API will return a `400` error with this message.

---

## **Step-by-Step Guide to Deploy the API**

### **1. Create the Lambda Function**

1. **Log in to AWS Console**.
2. Navigate to **AWS Lambda** and click **Create function**.
3. Choose **Author from scratch**.
4. Set the following options:
   - **Function name**: `NumberClassificationFunction`
   - **Runtime**: `Python 3.x`
5. **Function code**: In the inline editor, paste the following code:

```python
import json

def lambda_handler(event, context):
    # Retrieve the 'number' query string parameter
    try:
        number_str = event.get('queryStringParameters', {}).get('number', None)
        
        if not number_str or not is_valid_number(number_str):
            # If the 'number' is not provided or is invalid, return a 400 error with the template format
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'number': number_str,
                    'error': True,
                    'message': 'Invalid input. Please provide a valid number.'
                })
            }
        
        # Convert the 'number' parameter to a float (can handle integers and floating-point numbers)
        number = float(number_str)
        
        # Initialize the response dictionary with properties and fun fact
        response = {
            'number': number,
            'properties': [],
            'is_prime': is_prime(number),
            'is_perfect': is_perfect(number),
            'digit_sum': sum(int(digit) for digit in str(abs(int(number)))),
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

# Helper function to check if a string is a valid number
def is_valid_number(value):
    try:
        # Try converting the value to float (this will work for both integers and floating-point numbers)
        float(value)
        return True
    except ValueError:
        return False

# Helper function to check if a number is Armstrong
def is_armstrong(num):
    num_str = str(abs(int(num)))  # Consider the absolute value of the number
    num_digits = len(num_str)
    sum_of_powers = sum(int(digit) ** num_digits for digit in num_str)
    return sum_of_powers == abs(int(num))

# Helper function to check if a number is prime
def is_prime(num):
    num = abs(int(num))  # Consider the absolute value of the number
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Helper function to check if a number is perfect
def is_perfect(num):
    num = abs(int(num))  # Consider the absolute value of the number
    divisors_sum = sum(i for i in range(1, num) if num % i == 0)
    return divisors_sum == num

# Fun fact generator (replace with your logic)
def get_fun_fact(number):
    if is_armstrong(number):
        return f"{number} is an Armstrong number because " + " + ".join([f"{digit}^{len(str(number))}" for digit in str(abs(int(number)))]) + f" = {number}"
    return f"{number} is an interesting number!"
```

6. **Click Deploy** to save the function.

### **2. Create the API Gateway**

1. In the AWS Console, go to **API Gateway**.
2. Click **Create API** and choose **HTTP API**.
3. Set the following options:
   - **API Name**: `NumberClassificationAPI`
   - **Protocol**: `HTTP`
4. Under **Integrations**, choose **Lambda Function** and select your previously created Lambda function `NumberClassificationFunction`.
5. Set the **Route** to `GET` and **Path** to `/api/classify-number`.

### **3. Deploy the API**

1. Click **Deploy** and choose **[New Stage]** for the deployment.
2. Enter a **Stage Name** (e.g., `prod`).
3. Once deployed, the URL for your API will be available in the **Invoke URL** section. This is your endpoint for testing.

---

## **Testing the API Using the Browser**

You can test the API directly using your browser.

1. Open your browser.
2. In the address bar, enter the following URL (replace the placeholders with actual values):
   
   ```
   https://<your-api-id>.execute-api.<region>.amazonaws.com/<stage>/api/classify-number?number=<number>
   ```

   Example URL:

   ```
   https://abcd1234.execute-api.us-east-1.amazonaws.com/prod/api/classify-number?number=371
   ```

3. Press **Enter**.

### **Successful Response Example (200 OK)**

If the request is successful, you will see a response similar to:

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

### **Error Response Example (400 Bad Request)**

If you enter an invalid number, you will get the following response:

```json
{
  "number": "number",
  "error": true,
  "message": "Invalid input. Please provide a valid number."
}
```

---

## **Conclusion**

This project allows you to classify numbers based on various mathematical properties using a simple serverless API deployed with AWS Lambda and API Gateway. It supports both integers and floating-point numbers, and provides a rich set of features like Armstrong number checks, prime number identification, perfect number checks, and fun facts about numbers. Testing is simple with just a browser, and the deployment process is straightforward using AWS services.

---
