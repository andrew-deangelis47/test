from globalshop.client import GlobalShopClient


class FakeConnection:

    def cursor(self):
        return FakeCursor()


class FakeCursor:

    def execute(self, sql_cmd):
        print(f'mocking executing sql: {sql_cmd}')

        if "SELECT" in sql_cmd and "V_SALESPERSONS" in sql_cmd:
            print('mocking salesperson fetchone')
            from globalshop.tests.test_salesperson import TestSalesperson

            def fetchone_salesperson():
                return TestSalesperson().dummy_salesperson_row()

            self.fetchone = fetchone_salesperson
        elif "SELECT" in sql_cmd and "V_OP_CODES" in sql_cmd:
            # sql_cmd = "SELECT OPERATION FROM V_OP_CODES WHERE LMO='C' AND "
            # f"OPERATION = '{comment_code}' "
            print(sql_cmd.split('OPERATION = ')[1])
            code = sql_cmd.split('OPERATION = ')[1].strip()
            code = code.replace("'", '')

            def fetch_comment_op_code():
                return code

            self.fetchone = fetch_comment_op_code

    def fetchone(self):
        return (123, 'abc')

    def fetchall(self):
        return ((123, 'abc') * 2)

    def commit(self):
        print('mocking sql commit!')

    def close(self):
        print('mocking sql close!')


def mock_conn_client(mocker):
    # mocker.patch('pyodbc.cursor',return_value=FakeCursor())
    dummy_client()
    mocker.patch('pyodbc.connect', return_value=FakeConnection())
    mocker.patch('globalshop.client.GlobalShopClient.cursor',
                 return_value=FakeCursor())
    # setattr(GlobalShopClient,'cursor',


def dummy_client():
    client = GlobalShopClient(server_name='test', database='dbq',
                              username='user1', password='pwd1')
    return client


def fetch_one_at_a_time(dummy_rows: list, capsys):
    v = dummy_rows.pop() if dummy_rows else None
    if capsys:
        with capsys.disabled():
            print(f'Removed 1, {len(dummy_rows)} remain')
    return v


def mock_fetchone(mocker, dummy_rows, capsys=None):
    # logger.debug(dummy_rows)

    # def fetch_lambda():
    #     return fetch_one_at_a_time(dummy_rows, capsys=capsys)

    mocker.patch.object(FakeCursor,
                        'fetchone',
                        # return_value=fetch_lambda())
                        return_value=dummy_rows)


def mock_fetchall(mocker, dummy_rows):
    mocker.patch.object(FakeCursor,
                        'fetchall',
                        return_value=dummy_rows)


class TestClient:

    def test_create_client(self, mocker):
        client = dummy_client()
        assert client

    def test_connection(self, mocker):
        mock_conn_client(mocker)
        client = GlobalShopClient(server_name='test', database='dbq',
                                  username='user1', password='pwd1')
        conn = client.connect()
        assert conn

    def test_cursor(self, mocker):
        mock_conn_client(mocker)
        client = GlobalShopClient(server_name='test', database='dbq',
                                  username='user1', password='pwd1')
        cur = client.cursor()
        assert cur
