import json
import os

from epicor.customer import ShipTo


def test_create_ship_to():
    with open(os.path.join(os.path.dirname(__file__),
                           'data/ship_to.json')) as f:
        sp_data = f.read()
    json_data = json.loads(sp_data)
    st = ShipTo.from_json(json_data)
    print(f'ShipToNum: {st.ShipToNum}')
