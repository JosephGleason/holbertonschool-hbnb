#!/bin/bash

TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDI1NDg4OSwianRpIjoiYTNjNjU2ZmItY2QyZS00MTg3LWI2ZjQtNDkwMDRlN2U2MjBiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6IjRkNmY4ZjkwLTgyZTMtNGE0Yi04MTViLTE2ZWE1ZDlmOTM1MyIsImlzX2FkbWluIjp0cnVlfSwibmJmIjoxNzU0MjU0ODg5LCJjc3JmIjoiMmJhNWYyODgtYTRiOC00ZTEyLWI1YmMtZTA0MjVhY2VlMWQyIiwiZXhwIjoxNzU0MjU1Nzg5fQ.hHG3TDUozSOp5dRoUkNayinQT06Iobsv0jLOjC7wIOI"

PLACE_IDS=(
  "8c45f23b-d967-41f4-add0-e636d5b8a916"  # Casa del Sol
  "fc7b01ef-f089-4ae5-a5fb-109d4af1aac1"  # Ocean View Retreat
  "c5b753e0-f4b0-4e1e-b95e-c578b50afcc6"  # Rainforest Cabin
)

for PLACE_ID in "${PLACE_IDS[@]}"; do
  echo -e "\nFetching reviews for Place: $PLACE_ID..."
  REVIEW_IDS=$(curl -s -X GET http://127.0.0.1:5000/api/v1/reviews/place/$PLACE_ID \
    -H "Authorization: Bearer $TOKEN" | jq -r '.[].id')

  for id in $REVIEW_IDS; do
    echo "Deleting review $id..."
    curl -s -X DELETE http://127.0.0.1:5000/api/v1/reviews/$id \
      -H "Authorization: Bearer $TOKEN"
    echo "✔️ Deleted $id"
  done
done
