"""Settings page rendering tests."""

import re


def test_reset_settings_csrf_token_is_hidden(client):
    client.post(
        "/login",
        data={"email": "admin@example.com", "password": "adminpass"},
        follow_redirects=True,
    )
    response = client.get("/settings")

    assert response.status_code == 200
    page = response.get_data(as_text=True)
    reset_form = re.search(
        r'<form method="post" action="[^"]*/settings/reset"[^>]*>(.*?)</form>',
        page,
        re.DOTALL,
    )
    assert reset_form is not None
    hidden_token = re.search(
        r'<input id="csrf_token" name="csrf_token" type="hidden" value="([^"]+)">',
        reset_form.group(1),
    )
    assert hidden_token is not None
    assert hidden_token.group(1) not in reset_form.group(1).replace(hidden_token.group(0), "")