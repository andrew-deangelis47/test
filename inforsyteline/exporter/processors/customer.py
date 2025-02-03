from baseintegration.exporter import BaseProcessor, logger
from paperless.objects.orders import Order
from inforsyteline.models import CustaddrMst, CustomerMst
from django.db import connection
from paperless.objects.customers import Account
from baseintegration.utils import update_account_erp_code


class CustomerProcessor(BaseProcessor):

    def _process(self, order: Order) -> CustomerMst:
        logger.info("Processing customer")
        customer = None
        if not (order.customer and order.customer.company and order.customer.company.business_name):
            raise ValueError(f"Company info is incomplete on the Paperless order {order.number}")
        else:
            company_name = order.customer.company.business_name
        customer_addr = self.get_customer_addr(order.customer.company.erp_code, company_name)
        if customer_addr:
            logger.info("Cstuomer addr found")
            customer = self.get_customer_from_addr(customer_addr)
        if not customer:
            customer = self.create_customer(order, company_name)
        return customer

    def create_customer(self, order: Order, company_name: str):
        if self._exporter.erp_config.fail_if_new_customer:
            self._exporter.send_email(f"Paperless order {order.number} failed to process through integration",
                                      f"Paperless order {order.number} failed to process through integration "
                                      f"due to the presence of a new customer {company_name} which does not have"
                                      f"an ERP code field in Paperless that maps to Infor Syteline. Please process"
                                      f"this order manually into Syteline and, once you have created a new customer, "
                                      f"add its customer number to the field 'ERP Code' in the Paperless contact")
            raise ValueError(f"Paperless order {order.number} does not have customer")
        logger.info("Creating new customer")
        acct_id = order.contact.account.id
        acct: Account = Account.get(acct_id)
        addr1 = acct.sold_to_address.address1 if acct.sold_to_address else None
        city = acct.sold_to_address.city if acct.sold_to_address else None
        state = acct.sold_to_address.state if acct.sold_to_address else None
        country = acct.sold_to_address.country if acct.sold_to_address else None
        zip = acct.sold_to_address.postal_code if acct.sold_to_address else None
        if not self._exporter._integration.test_mode:
            next_num = self.get_next_number()
            with connection.cursor() as cursor:
                sql = f"""
                                    SET NOCOUNT ON;
                                    DECLARE @RC int;
                                    DECLARE @myid uniqueidentifier;
                                    DECLARE	@Infobar InfobarType;
                                    SET @myid = NEWID();
                                    Exec [{self._exporter.erp_config.name}].[dbo].[SetSiteSp] '{self._exporter.erp_config.site_ref}', Infobar
                                    EXEC [{self._exporter.erp_config.name}].[dbo].[CustomerInsUpdSp]
                                    @CustNum='{next_num}',
                                    @CustSeq='0',
                                    @Addr_1='{addr1}',
                                    @City='{city}',
                                    @Country='{country}',
                                    @State='{state}',
                                    @Zip='{zip}',
                                    @Name='{company_name}',
                                    @InvCategory='DEFAULTCATEGORY',
                                    @ActiveForDataIntegration='0',
                                    @DefaultShipTo='0',
                                    @ExportType='N',
                                    @ShipmentApprovalRequired='0',
                                    @RowPointer=@myid
                                    @Infobar = @Infobar OUTPUT;
                                    SELECT @Infobar as N'@Infobar'
                                    """
                cursor.execute(sql)
                try:
                    # log error message if appropriate
                    logger.info(cursor.fetchone()[0])
                except:
                    pass
        else:
            CustomerMst.objects.create(cust_num="test", cust_seq=0)
            CustaddrMst.objects.create(cust_num="test", cust_seq=0, name=company_name)
        cust_addr = CustaddrMst.objects.filter(name=company_name).first()
        if not cust_addr:
            raise ValueError(f"Customer insert for {company_name} failed, please check")
        else:
            customer = self.get_customer_from_addr(cust_addr)
            if not self._exporter._integration.test_mode:
                update_account_erp_code(self._exporter._integration, acct_id, customer.cust_num)
        return customer

    @staticmethod
    def get_customer_addr(erp_code: str, business_name: str) -> CustaddrMst:
        """First attempt to match directly on name, if not them match on cust_num"""
        addr = CustaddrMst.objects.filter(name__iexact=business_name).first()
        if not addr:
            addr = CustaddrMst.objects.extra(where=[f"LOWER(REPLACE(cust_num,' ','')) = '{erp_code}'"]).first()
        return addr

    @staticmethod
    def get_customer_from_addr(cust_addr: CustaddrMst) -> CustomerMst:
        return CustomerMst.objects.filter(cust_num=cust_addr.cust_num).first()

    def get_next_number(self) -> int:
        cust_num = CustomerMst.objects.extra(select={'myinteger': 'CAST(cust_num AS INTEGER)'}).order_by(
            '-myinteger').first().cust_num
        logger.info(cust_num)
        return int(cust_num.replace(" ", "")) + 1
