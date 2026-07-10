import requests

def fetch_problem(title_slug):
    url = f"https://alfa-leetcode-api.onrender.com/select?titleSlug={title_slug}"
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    data = response.json()

    if not data or 'questionFrontendId' not in data:
        return None
    
    return {
        'problem_number': int(data['questionFrontendId']),
        'title': data['questionTitle'],
        'difficulty': data['difficulty'],
        'link': data['link']
    }