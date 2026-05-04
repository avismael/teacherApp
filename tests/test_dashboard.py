def test_dashboard_index(client, init_database):
    response = client.get('/')
    assert response.status_code == 200
    assert b'TeacherApp' in response.data or b'Dashboard' in response.data or b'registro' in response.data.lower()
