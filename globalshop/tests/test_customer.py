import decimal

from globalshop.tests.test_connection import mock_conn_client, \
    FakeCursor, mock_fetchone, mock_fetchall
from globalshop.client import GlobalShopClient
from globalshop.customer import CustomerRecord, Customer, ContactRecord, \
    Contact

dummy_cus_row = ('ABC123', 'rec', 'customer_name', 'addr1', 'addr2', 'city',
                 'state', 'zip', 'country', 'county', 'attn', 'salesperson',
                 'intl', 'terr', 'code_area', '10000.00',
                 'phone',
                 'crm_res_lev',
                 'assgn_usr_grp', 'normal_gl_acct', 'flag_balance_fwd',
                 # 'flag_print_state',
                 'flag_credit_hold', 'change_mode',
                 'intercompany')

dummy_cont_row = ('123', 'C', '456', 'Willy Waffle',
                  '123-456-7890', 'x1234',
                  'Waffle Lord', 'waffle', 'lord',
                  'Eater of Waffles, Demander of Tribute',
                  'Willy@waffles.com')


def dummy_cus_rows():
    return [dummy_cus_row for _ in range(10)]


def dummy_cont_rows():
    return [dummy_cont_row for _ in range(10)]


dummy_client = GlobalShopClient(server_name='test', database='dbq',
                                username='user1', password='pwd1')


def mock_fetchall_contacts(mocker, dummy_rows):
    mocker.patch.object(FakeCursor,
                        'fetchall',
                        return_value=dummy_rows)


def dummy_cust_record() -> CustomerRecord:
    rec = CustomerRecord(account_id='123', gss_customer_number='ABC123',
                         customer_name='Wollys Waffle house',
                         address_1='123 Fake st',
                         address_2='Attn Stan the Man',
                         city='Cedar Rapids', state='Iowa', zip='52405',
                         country='USA',
                         phone='1234567890',
                         credit_limit=decimal.Decimal('100.00'),
                         salesperson_code='JBG', credit_hold=False,
                         terms=None)
    return rec


class TestCustomer:
    def test_create_cust_data(self, mocker):
        "Create a CustomerRecord without erroring out"
        rec = dummy_cust_record()
        assert rec

    def test_get(self, mocker):
        mock_conn_client(mocker)
        mock_fetchone(mocker, dummy_cus_row)
        rec = Customer.get('ABC123')
        assert rec
        assert rec.gss_customer_number == 'ABC123'

    def test_select_ids(self, mocker):
        mock_conn_client(mocker)
        rows = dummy_cus_rows()
        mock_fetchall(mocker, rows)
        ids = Customer.select_ids()

        assert ids
        assert len(ids) == len(rows)

    def test_select_all(self, mocker, capsys):
        mock_conn_client(mocker)
        # This will force it to terminate
        rows = dummy_cus_rows()
        # rows.append(None)
        # with capsys.disabled():
        #     print(f'rows: {rows}')
        # mock_fetchone(mocker,rows,capsys)
        mock_fetchall(mocker, rows)
        recs = Customer.select()
        # print(recs)
        assert recs

    def test_insert(self, mocker):
        mock_conn_client(mocker)

    def test_contact_rec(self, mocker):
        ContactRecord(customer_id='123',
                      contact_type='C', contact_id='123', name='Willy Waffle',
                      phone1='123-456-7890', ext1='x1234',
                      title='Waffle Lord', first_name='waffle',
                      last_name='lord',
                      job_function='Eater of Waffles, Demander of Tribute',
                      email1='Willy@waffles.com')

    def test_select_contacts(self, mocker):
        mock_conn_client(mocker)
        # This will force it to terminate
        rows = dummy_cont_rows()  # rows.append(None)
        # mock_fetchone(mocker,rows,capsys)
        mock_fetchall(mocker, rows)
        recs = Contact.select(customer_id='123')
        # print(recs)
        assert recs
