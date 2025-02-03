from baseintegration.exporter import BaseProcessor, logger
from paperless.objects.orders import Order, OrderItem
from inforsyteline.models import CustomerMst, CoMst, CoitemMst
from inforsyteline.utils import get_part_number_and_name
from django.db import connection


class CustomerOrderProcessor(BaseProcessor):

    def _process(self, order: Order, customer: CustomerMst) -> None:
        logger.info(f"Processing customer order for order {order.number}")
        self.add_customer_order(customer)
        co = CoMst.objects.filter(cust_num=customer.cust_num).order_by("-recorddate").first()
        if co:
            co_num = co.co_num
            self._exporter.success_message = f"Associated Infor Syteline customer order number is {co_num}"
            self.update_customer_order_price(co_num, order)
        else:
            raise ValueError("Co was not created")
        order_line_no = 1
        for item in order.order_items:
            item: OrderItem = item
            part_no = get_part_number_and_name(item.root_component)[0]
            logger.info(f"Inserting line no {order_line_no} w part no {part_no}")
            cost = float(item.unit_price.dollars)
            self.add_customer_order_line(co_num, order_line_no, part_no, item, customer, cost)
            order_line_no += 1

    def add_customer_order(self, customer: CustomerMst) -> None:
        if not self._exporter._integration.test_mode:
            with connection.cursor() as cursor:
                sql = f"""
                        SET NOCOUNT ON;
                        DECLARE @RC int;
                        DECLARE @myid uniqueidentifier;
                        DECLARE	@Infobar InfobarType;
                        SET @myid = NEWID();
                        Exec [{self._exporter.erp_config.name}].[dbo].[SetSiteSp] '{self._exporter.erp_config.site_ref}', Infobar
                        BEGIN TRAN;
                        EXEC [{self._exporter.erp_config.name}].[dbo].[InventoryConstoCustOrderSp]
                        @pOrderType='Standard',
                        @pStat='Open',
                        @CoCustNum='{customer.cust_num}',
                        @CoCustSeq='{customer.cust_seq}',
                        @pOrderDate=NULL,
                        @pWhse='MAIN',
                        @pCoConsignment=NULL,
                        @RowPointer=@myid,
                        @Infobar=@Infobar OUTPUT;
                        COMMIT TRAN;
                        SELECT @Infobar as N'@Infobar'
                        """
                cursor.execute(sql)
                try:
                    # log error message if appropriate
                    logger.info(cursor.fetchone()[0])
                except:
                    pass
        else:
            import random
            co_num = random.randint(1, 100)
            CoMst.objects.create(site_ref="SYTE",
                                 cust_num=customer.cust_num,
                                 cust_seq=customer.cust_seq,
                                 co_num=str(co_num))

    def update_customer_order_price(self, co_num: str, order: Order) -> None:
        if order.payment_details:
            po_number = order.payment_details.purchase_order_number
            total_price = float(order.payment_details.total_price.dollars)
        else:
            po_number = "N/A"
            total_price = 0
        if not self._exporter._integration.test_mode:
            with connection.cursor() as cursor:
                sql = f"""
                        SET NOCOUNT ON;
                        UPDATE [{self._exporter.erp_config.name}].[dbo].[Co_Mst]
                        SET [cust_po] = '{po_number}', [price] = '{total_price}'
                        WHERE [co_num] = '{co_num}'
                        """
                cursor.execute(sql)
        else:
            co: CoMst = CoMst.objects.filter(co_num=co_num).first()
            co.cust_po = po_number
            co.price = total_price

    def add_customer_order_line(self, co_num: str, order_line_no: int, part_no: str, item: OrderItem,
                                customer: CustomerMst, cost: float) -> None:
        if not self._exporter._integration.test_mode:
            with connection.cursor() as cursor:
                sql = f"""
                        SET NOCOUNT ON;
                        DECLARE @RC int;
                        DECLARE @myid uniqueidentifier;
                        DECLARE	@Infobar InfobarType;
                        SET @myid = NEWID();
                        Exec [{self._exporter.erp_config.name}].[dbo].[SetSiteSp] '{self._exporter.erp_config.site_ref}', Infobar
                        BEGIN TRAN;
                        EXEC [{self._exporter.erp_config.name}].[dbo].[InventoryConstoCustOrderLineSp]
                        @pCoNum='{co_num}',
                        @pCoLine='{order_line_no}',
                        @pStat='Open',
                        @pItem='{part_no}',
                        @pQtyOrderedConv='{item.quantity}',
                        @pUM='EA',
                        @CoCustNum='{customer.cust_num}',
                        @CoCustSeq='{customer.cust_seq}',
                        @ItemPriceConv='{cost}',
                        @ItemPrice='{cost}',
                        @ColProjectedDate=NULL,
                        @ColDueDate=NULL,
                        @ColPromiseDate=NULL,
                        @RowPointer=@myid,
                        @Infobar=@Infobar OUTPUT;
                        COMMIT TRAN;
                        UPDATE [{self._exporter.erp_config.name}].[dbo].[CoItem_Mst]
                        SET [cost] = '{cost}', [price] = '{cost}', [price_conv] = '{cost}'
                        WHERE [co_num] = '{co_num}' AND [co_line] = '{order_line_no}' AND [item] = '{part_no}'
                        SELECT @Infobar as N'@Infobar'
                        """
                cursor.execute(sql)
                try:
                    # log error message if appropriate
                    logger.info(cursor.fetchone()[0])
                except:
                    pass
        else:
            CoitemMst.objects.create(site_ref="SYTE",
                                     co_num=co_num,
                                     co_line=order_line_no,
                                     item=part_no,
                                     cost=cost,
                                     price=cost,
                                     qty_ordered=item.quantity
                                     )
        co_item = CoitemMst.objects.filter(co_num=co_num).filter(co_line=order_line_no).filter(item=part_no).first()
        if not co_item:
            raise ValueError(f"Co item for line {order_line_no} could not be found")
