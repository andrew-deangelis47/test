from baseintegration.utils.custom_table import CustomTableFormat


class PurchaseOrderLineCustomTableFormat(CustomTableFormat):

    _custom_table_name = "purchase_order_line_custom_table"  # This is what will appear in paperless, and how the table will be referenced
    _primary_key = "purchaseorderlinepk"  # This is the attribute alias

    def __init__(self):
        self.purchaseorderlinepk = 0
        self.purchaseorderfk = 0
        self.itemfk = 0
        self.unitofmeasurecode = "EA"
        self.quantity = 0
        self.price = 0
        self.createdate = ""
        self.closeddate = ""
