import requests

url = "https://api.themoviedb.org/3/movie/550?api_key=f351be27b76787cddc3a8a2646b33cb5"

try:
    response = requests.get(
        url,
        verify=False
    )

    print("Status:", response.status_code)

except Exception as e:
    print("Error:", e)