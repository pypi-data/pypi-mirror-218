import json


async def test_get_config(jp_fetch):
    # When
    response = await jp_fetch("jupyter_iam", "get_config")

    # Then
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {
        "data": "This is /jupyter_iam/get_config endpoint."
    }
