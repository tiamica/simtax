import requests
import json
from datetime import datetime
import time

BASE_URL = 'http://localhost:5000'

def test_endpoints():
    # Test phone number
    phone_number = '2348012345678'
    current_year = datetime.now().year

    tests = [
        # Test registration first
        {
            'name': 'Registration',
            'endpoint': '/process-message',
            'method': 'POST',
            'data': {
                'phone_number': phone_number,
                'message': 'REG TIN123456'
            }
        },
        
        # Wait a bit before next requests
        {'name': 'Wait', 'delay': 1},
        
        # Test income update
        {
            'name': 'Income Update',
            'endpoint': '/process-message',
            'method': 'POST',
            'data': {
                'phone_number': phone_number,
                'message': f'INC 500000 {current_year}'
            }
        },
        
        {'name': 'Wait', 'delay': 1},
        
        # Test expenditure update
        {
            'name': 'Expenditure Update',
            'endpoint': '/process-message',
            'method': 'POST',
            'data': {
                'phone_number': phone_number,
                'message': f'EXP 200000 {current_year}'
            }
        },
        
        {'name': 'Wait', 'delay': 1},
        
        # Test tax calculation
        {
            'name': 'Tax Calculation',
            'endpoint': f'/calculate-tax/{phone_number}/{current_year}',
            'method': 'GET'
        },
        
        # Test return status
        {
            'name': 'Return Status',
            'endpoint': f'/check-return/{phone_number}/{current_year}',
            'method': 'GET'
        },
        
        # Test user data retrieval
        {
            'name': 'User Data',
            'endpoint': f'/admin/user/{phone_number}',
            'method': 'GET'
        }
    ]

    success_count = 0
    total_tests = len([test for test in tests if 'method' in test])

    for test in tests:
        if test.get('delay'):
            time.sleep(test['delay'])
            continue

        print(f"\nTesting {test['name']}...")
        try:
            if test['method'] == 'POST':
                response = requests.post(
                    f"{BASE_URL}{test['endpoint']}", 
                    json=test['data']
                )
            else:
                response = requests.get(f"{BASE_URL}{test['endpoint']}")
            
            print(f"Status Code: {response.status_code}")
            print("Response:", json.dumps(response.json(), indent=2))
            
            assert response.status_code in [200, 201], f"Failed: {response.status_code}"
            print(f"{test['name']} test passed!")
            success_count += 1
            
        except Exception as e:
            print(f"{test['name']} test failed:", str(e))

    print(f"\nTest Summary: {success_count}/{total_tests} tests passed")

def cleanup_test_data():
    """Clean up test data before running tests"""
    try:
        phone_number = '2348012345678'
        response = requests.delete(f"{BASE_URL}/admin/user/{phone_number}")
        print("Test data cleaned up")
    except:
        print("No cleanup needed")

if __name__ == '__main__':
    cleanup_test_data()
    test_endpoints() 