import requests

url = "https://api.instagram.com"

config = {
    "client_id":
 "redirect_uri":"https://script.google.com/macros/s/AKfycbxkDewtgpXflxVzrS74aewg-CgfvGU8kXoG466Db4G7ZGTNJkJ8Df5l-yIG8Uy24BUYOQ/exec"
  "scope":
  "response_type":"code"
}

publish_response = requests.post(publish_url, data=publish_payload)