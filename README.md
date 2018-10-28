# Order Processing API

This application is used to process orders received to a bakery.
The application has been hosted on AWS as a Lambda service.

## Assumptions

- The format in which the order is received is JSON
- The processed output of the order is returned as JSON
- There can be multiple orders in the same request
- If an invalid product code is requested to be processed an appropriate message is to be displayed for that order
- If an invalid order quantity is requested an appropriate message is to be displayed for that order 
- There is no limitation to the number of orders in a request

## Usage

The application can be invoked by using the below end point:

https://g6rygdl0qi.execute-api.ap-southeast-2.amazonaws.com/prod

Given below are sample usages:

-- Invoke GET request to view order request format

```curl -H "Content-Type: application/json" -X GET ${RUBIX_BAKERY_URL}/order```

-- Invoke POST request with json request to process order

```curl -H "Content-Type: application/json" -X POST ${RUBIX_BAKERY_URL}/order -d '{"order": [{"order_code": "ORD1","order_details": {"VS5": 10,"MB11": 14,"CA": 13}}]}'```

Alternatively execute the `run.sh` to invoke a sample order
## Tests

The application includes unit tests and can be invoked with the below command
sh test.sh`

## Dependencies

Execute `pip install -r requirements.txt` to install all required dependencies. 