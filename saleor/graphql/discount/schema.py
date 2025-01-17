import graphene

from ..core.fields import FilterInputConnectionField
from ..core.types import FilterInputObjectType
from ..decorators import permission_required
from ..translations.mutations import SaleTranslate, VoucherTranslate
from .bulk_mutations import SaleBulkDelete, VoucherBulkDelete
from .filters import SaleFilter, VoucherFilter
from .mutations import (
    SaleAddCatalogues,
    SaleCreate,
    SaleDelete,
    SaleRemoveCatalogues,
    SaleUpdate,
    VoucherAddCatalogues,
    VoucherCreate,
    VoucherDelete,
    VoucherRemoveCatalogues,
    VoucherUpdate,
)
from .resolvers import resolve_sales, resolve_vouchers
from .sorters import SaleSortingInput, VoucherSortingInput
from .types import Sale, Voucher


class VoucherFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = VoucherFilter


class SaleFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = SaleFilter


class DiscountQueries(graphene.ObjectType):
    sale = graphene.Field(
        Sale,
        id=graphene.Argument(graphene.ID, description="ID of the sale.", required=True),
        description="Look up a sale by ID.",
    )
    sales = FilterInputConnectionField(
        Sale,
        filter=SaleFilterInput(description="Filtering options for sales."),
        sort_by=SaleSortingInput(description="Sort sales."),
        query=graphene.String(description="Search sales by name, value or type."),
        description="List of the shop's sales.",
    )
    voucher = graphene.Field(
        Voucher,
        id=graphene.Argument(
            graphene.ID, description="ID of the voucher.", required=True
        ),
        description="Look up a voucher by ID.",
    )
    vouchers = FilterInputConnectionField(
        Voucher,
        filter=VoucherFilterInput(description="Filtering options for vouchers."),
        sort_by=VoucherSortingInput(description="Sort voucher."),
        query=graphene.String(description="Search vouchers by name or code."),
        description="List of the shop's vouchers.",
    )

    @permission_required("discount.manage_discounts")
    def resolve_sale(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Sale)

    @permission_required("discount.manage_discounts")
    def resolve_sales(self, info, query=None, **kwargs):
        return resolve_sales(info, query, **kwargs)

    @permission_required("discount.manage_discounts")
    def resolve_voucher(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Voucher)

    @permission_required("discount.manage_discounts")
    def resolve_vouchers(self, info, query=None, **kwargs):
        return resolve_vouchers(info, query, **kwargs)


class DiscountMutations(graphene.ObjectType):
    sale_create = SaleCreate.Field()
    sale_delete = SaleDelete.Field()
    sale_bulk_delete = SaleBulkDelete.Field()
    sale_update = SaleUpdate.Field()
    sale_catalogues_add = SaleAddCatalogues.Field()
    sale_catalogues_remove = SaleRemoveCatalogues.Field()
    sale_translate = SaleTranslate.Field()

    voucher_create = VoucherCreate.Field()
    voucher_delete = VoucherDelete.Field()
    voucher_bulk_delete = VoucherBulkDelete.Field()
    voucher_update = VoucherUpdate.Field()
    voucher_catalogues_add = VoucherAddCatalogues.Field()
    voucher_catalogues_remove = VoucherRemoveCatalogues.Field()
    voucher_translate = VoucherTranslate.Field()
