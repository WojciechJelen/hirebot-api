import requests
import json


def test_browse_job_postings():
    """
    Test the /browse-job-postings endpoint.
    """
    url = "http://localhost:8000/browse-job-postings"

    # Request payload
    payload = {"query": "Python developer", "location": "San Francisco, CA"}

    # Make the request
    print(f"Sending request to {url} with payload: {payload}")
    response = requests.post(url, json=payload)

    # Print the response
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        # Pretty print the JSON response
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")


if __name__ == "__main__":
    test_browse_job_postings()
