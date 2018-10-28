export RUBIX_BAKERY_URL="https://g6rygdl0qi.execute-api.ap-southeast-2.amazonaws.com/prod"
curl -H "Content-Type: application/json" -X POST ${RUBIX_BAKERY_URL}/order -d '{"order": [{"order_code": "ORD1","order_details": {"VS5": 10,"MB11": 14,"CA": 13}}]}'
