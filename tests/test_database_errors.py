"""Database configuration error page tests."""


def test_missing_database_url_shows_connection_error(client, app):
    app.config["DATABASE_CONFIGURED"] = False

    response = client.get("/")

    assert response.status_code == 503
    assert b"Error connecting to your database" in response.data
    assert b"DATABASE_URL is missing" in response.data