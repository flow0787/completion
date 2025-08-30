import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app

def test_healthcheck():
    client = app.test_client()
    response = client.get('/healthcheck')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ok'
    assert 'version' in data
    print("/healthcheck passed ")

if __name__ == "__main__":
    test_healthcheck()