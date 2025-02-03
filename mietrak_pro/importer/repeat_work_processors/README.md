Here are brief descriptions of the tables used by the repeat work importers:

- A `Quote` represents a quoted item
  - A `QuoteQuantity` represents a possible quantity of a `Quote`
  - A `QuoteAssembly` represents a BOM or routing line of a `Quote`

- A `WorkOrder` represents a top-level work order (assemblies have a single work order)
  - A `WorkOrderTotal` represents the total cost, price, etc. of a `WorkOrder`
  - A `WorkOrderRelease` represents an item within a `WorkOrder`
    - A `WorkOrderAssembly` represents a BOM or routing line of a `WorkOrderRelease`
    - A `WorkOrderCompletion` represents a fulfilled portion of a `WorkOrder` or `WorkOrderRelease`

