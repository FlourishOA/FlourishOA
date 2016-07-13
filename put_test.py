import requests

r = requests.post('http://localhost:8000/1234-456X', data={
    "issn_number": "1234-456X",
    "journal_name": 'Test Journal',
    'article_influence': 12.5,
    'est_article_influence': None,
    'is_hybrid': 'false',
    'category': None,
})
print str(r)