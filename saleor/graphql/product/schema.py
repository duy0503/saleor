import graphene

from ..core.enums import ReportingPeriod
from ..core.fields import FilterInputConnectionField, PrefetchingConnectionField
from ..decorators import permission_required
from ..descriptions import DESCRIPTIONS
from ..translations.mutations import (
    AttributeTranslate,
    AttributeValueTranslate,
    CategoryTranslate,
    CollectionTranslate,
    ProductTranslate,
    ProductVariantTranslate,
)
from .bulk_mutations.attributes import AttributeBulkDelete, AttributeValueBulkDelete
from .bulk_mutations.products import (
    CategoryBulkDelete,
    CollectionBulkDelete,
    CollectionBulkPublish,
    ProductBulkDelete,
    ProductBulkPublish,
    ProductImageBulkDelete,
    ProductTypeBulkDelete,
    ProductVariantBulkCreate,
    ProductVariantBulkDelete,
)
from .enums import StockAvailability
from .filters import (
    AttributeFilterInput,
    CategoryFilterInput,
    CollectionFilterInput,
    ProductFilterInput,
    ProductTypeFilterInput,
)
from .mutations.attributes import (
    AttributeAssign,
    AttributeClearMeta,
    AttributeClearPrivateMeta,
    AttributeCreate,
    AttributeDelete,
    AttributeReorderValues,
    AttributeUnassign,
    AttributeUpdate,
    AttributeUpdateMeta,
    AttributeUpdatePrivateMeta,
    AttributeValueCreate,
    AttributeValueDelete,
    AttributeValueUpdate,
    ProductTypeReorderAttributes,
)
from .mutations.digital_contents import (
    DigitalContentCreate,
    DigitalContentDelete,
    DigitalContentUpdate,
    DigitalContentUrlCreate,
)
from .mutations.products import (
    CategoryClearMeta,
    CategoryClearPrivateMeta,
    CategoryCreate,
    CategoryDelete,
    CategoryUpdate,
    CategoryUpdateMeta,
    CategoryUpdatePrivateMeta,
    CollectionAddProducts,
    CollectionClearMeta,
    CollectionClearPrivateMeta,
    CollectionCreate,
    CollectionDelete,
    CollectionRemoveProducts,
    CollectionReorderProducts,
    CollectionUpdate,
    CollectionUpdateMeta,
    CollectionUpdatePrivateMeta,
    ProductClearMeta,
    ProductClearPrivateMeta,
    ProductCreate,
    ProductDelete,
    ProductImageCreate,
    ProductImageDelete,
    ProductImageReorder,
    ProductImageUpdate,
    ProductTypeClearMeta,
    ProductTypeClearPrivateMeta,
    ProductTypeCreate,
    ProductTypeDelete,
    ProductTypeUpdate,
    ProductTypeUpdateMeta,
    ProductTypeUpdatePrivateMeta,
    ProductUpdate,
    ProductUpdateMeta,
    ProductUpdatePrivateMeta,
    ProductVariantClearMeta,
    ProductVariantClearPrivateMeta,
    ProductVariantCreate,
    ProductVariantDelete,
    ProductVariantUpdate,
    ProductVariantUpdateMeta,
    ProductVariantUpdatePrivateMeta,
    VariantImageAssign,
    VariantImageUnassign,
)
from .resolvers import (
    resolve_attributes,
    resolve_categories,
    resolve_collections,
    resolve_digital_contents,
    resolve_product_types,
    resolve_product_variants,
    resolve_products,
    resolve_report_product_sales,
)
from .scalars import AttributeScalar
from .sorters import (
    AttributeSortingInput,
    CategorySortingInput,
    CollectionSortingInput,
    ProductOrder,
    ProductTypeSortingInput,
)
from .types import (
    Attribute,
    Category,
    Collection,
    DigitalContent,
    Product,
    ProductType,
    ProductVariant,
)


class ProductQueries(graphene.ObjectType):
    digital_content = graphene.Field(
        DigitalContent,
        description="Look up digital content by ID.",
        id=graphene.Argument(
            graphene.ID, description="ID of the digital content.", required=True
        ),
    )
    digital_contents = PrefetchingConnectionField(
        DigitalContent, description="List of digital content."
    )
    attributes = FilterInputConnectionField(
        Attribute,
        description="List of the shop's attributes.",
        query=graphene.String(description=DESCRIPTIONS["attributes"]),
        in_category=graphene.Argument(
            graphene.ID,
            description=(
                "Return attributes for products belonging to the given category. "
                "DEPRECATED: Will be removed in Saleor 2.10, use the `filter` field "
                "instead."
            ),
        ),
        in_collection=graphene.Argument(
            graphene.ID,
            description=(
                "Return attributes for products belonging to the given collection. "
                "DEPRECATED: Will be removed in Saleor 2.10, use the `filter` "
                "field instead."
            ),
        ),
        filter=AttributeFilterInput(description="Filtering options for attributes."),
        sort_by=AttributeSortingInput(description="Sorting options for attributes."),
    )
    attribute = graphene.Field(
        Attribute,
        id=graphene.Argument(
            graphene.ID, description="ID of the attribute.", required=True
        ),
        description="Look up an attribute by ID.",
    )
    categories = FilterInputConnectionField(
        Category,
        query=graphene.String(description=DESCRIPTIONS["category"]),
        filter=CategoryFilterInput(description="Filtering options for categories."),
        sort_by=CategorySortingInput(description="Sort categories."),
        level=graphene.Argument(
            graphene.Int,
            description="Filter categories by the nesting level in the category tree.",
        ),
        description="List of the shop's categories.",
    )
    category = graphene.Field(
        Category,
        id=graphene.Argument(
            graphene.ID, required=True, description="ID of the category."
        ),
        description="Look up a category by ID.",
    )
    collection = graphene.Field(
        Collection,
        id=graphene.Argument(
            graphene.ID, description="ID of the collection.", required=True
        ),
        description="Look up a collection by ID.",
    )
    collections = FilterInputConnectionField(
        Collection,
        filter=CollectionFilterInput(description="Filtering options for collections."),
        sort_by=CollectionSortingInput(description="Sort collections."),
        query=graphene.String(description=DESCRIPTIONS["collection"]),
        description="List of the shop's collections.",
    )
    product = graphene.Field(
        Product,
        id=graphene.Argument(
            graphene.ID, description="ID of the product.", required=True
        ),
        description="Look up a product by ID.",
    )
    products = FilterInputConnectionField(
        Product,
        filter=ProductFilterInput(description="Filtering options for products."),
        attributes=graphene.List(
            AttributeScalar,
            description=(
                "Filter products by attributes. DEPRECATED: Will be removed in "
                "Saleor 2.10, use the `filter` field instead."
            ),
        ),
        categories=graphene.List(
            graphene.ID,
            description=(
                "Filter products by category. DEPRECATED: Will be removed in "
                "Saleor 2.10, use the `filter` field instead."
            ),
        ),
        collections=graphene.List(
            graphene.ID,
            description=(
                "Filter products by collections. DEPRECATED: Will be removed in "
                "Saleor 2.10, use the `filter` field instead."
            ),
        ),
        sort_by=ProductOrder(description="Sort products."),
        stock_availability=graphene.Argument(
            StockAvailability, description="Filter products by stock availability."
        ),
        query=graphene.String(description=DESCRIPTIONS["product"]),
        description="List of the shop's products.",
    )
    product_type = graphene.Field(
        ProductType,
        id=graphene.Argument(
            graphene.ID, description="ID of the product type.", required=True
        ),
        description="Look up a product type by ID.",
    )
    product_types = FilterInputConnectionField(
        ProductType,
        filter=ProductTypeFilterInput(
            description="Filtering options for product types."
        ),
        query=graphene.String(description=DESCRIPTIONS["product_type"]),
        sort_by=ProductTypeSortingInput(description="Sort product types."),
        description="List of the shop's product types.",
    )
    product_variant = graphene.Field(
        ProductVariant,
        id=graphene.Argument(
            graphene.ID, description="ID of the product variant.", required=True
        ),
        description="Look up a product variant by ID.",
    )
    product_variants = PrefetchingConnectionField(
        ProductVariant,
        ids=graphene.List(
            graphene.ID, description="Filter product variants by given IDs."
        ),
        description="List of product variants.",
    )
    report_product_sales = PrefetchingConnectionField(
        ProductVariant,
        period=graphene.Argument(
            ReportingPeriod, required=True, description="Span of time."
        ),
        description="List of top selling products.",
    )

    def resolve_attributes(self, info, **kwargs):
        return resolve_attributes(info, **kwargs)

    def resolve_attribute(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Attribute)

    def resolve_categories(self, info, level=None, query=None, **kwargs):
        return resolve_categories(info, level=level, query=query, **kwargs)

    def resolve_category(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Category)

    def resolve_collection(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Collection)

    def resolve_collections(self, info, query=None, **kwargs):
        return resolve_collections(info, query, **kwargs)

    @permission_required("product.manage_products")
    def resolve_digital_content(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, DigitalContent)

    @permission_required("product.manage_products")
    def resolve_digital_contents(self, info, **_kwargs):
        return resolve_digital_contents(info)

    def resolve_product(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Product)

    def resolve_products(self, info, **kwargs):
        return resolve_products(info, **kwargs)

    def resolve_product_type(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, ProductType)

    def resolve_product_types(self, info, query=None, **kwargs):
        return resolve_product_types(info, query, **kwargs)

    def resolve_product_variant(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, ProductVariant)

    def resolve_product_variants(self, info, ids=None, **_kwargs):
        return resolve_product_variants(info, ids)

    @permission_required(["order.manage_orders", "product.manage_products"])
    def resolve_report_product_sales(self, *_args, period, **_kwargs):
        return resolve_report_product_sales(period)


class ProductMutations(graphene.ObjectType):
    attribute_create = AttributeCreate.Field()
    attribute_delete = AttributeDelete.Field()
    attribute_bulk_delete = AttributeBulkDelete.Field()
    attribute_assign = AttributeAssign.Field()
    attribute_unassign = AttributeUnassign.Field()
    attribute_update = AttributeUpdate.Field()
    attribute_translate = AttributeTranslate.Field()
    attribute_update_metadata = AttributeUpdateMeta.Field()
    attribute_clear_metadata = AttributeClearMeta.Field()
    attribute_update_private_metadata = AttributeUpdatePrivateMeta.Field()
    attribute_clear_private_metadata = AttributeClearPrivateMeta.Field()

    attribute_value_create = AttributeValueCreate.Field()
    attribute_value_delete = AttributeValueDelete.Field()
    attribute_value_bulk_delete = AttributeValueBulkDelete.Field()
    attribute_value_update = AttributeValueUpdate.Field()
    attribute_value_translate = AttributeValueTranslate.Field()
    attribute_reorder_values = AttributeReorderValues.Field()

    category_create = CategoryCreate.Field()
    category_delete = CategoryDelete.Field()
    category_bulk_delete = CategoryBulkDelete.Field()
    category_update = CategoryUpdate.Field()
    category_translate = CategoryTranslate.Field()
    category_update_metadata = CategoryUpdateMeta.Field()
    category_clear_metadata = CategoryClearMeta.Field()
    category_update_private_metadata = CategoryUpdatePrivateMeta.Field()
    category_clear_private_metadata = CategoryClearPrivateMeta.Field()

    collection_add_products = CollectionAddProducts.Field()
    collection_create = CollectionCreate.Field()
    collection_delete = CollectionDelete.Field()
    collection_reorder_products = CollectionReorderProducts.Field()
    collection_bulk_delete = CollectionBulkDelete.Field()
    collection_bulk_publish = CollectionBulkPublish.Field()
    collection_remove_products = CollectionRemoveProducts.Field()
    collection_update = CollectionUpdate.Field()
    collection_translate = CollectionTranslate.Field()
    collection_update_metadata = CollectionUpdateMeta.Field()
    collection_clear_metadata = CollectionClearMeta.Field()
    collection_update_private_metadata = CollectionUpdatePrivateMeta.Field()
    collection_clear_private_metadata = CollectionClearPrivateMeta.Field()

    product_create = ProductCreate.Field()
    product_delete = ProductDelete.Field()
    product_bulk_delete = ProductBulkDelete.Field()
    product_bulk_publish = ProductBulkPublish.Field()
    product_update = ProductUpdate.Field()
    product_translate = ProductTranslate.Field()
    product_update_metadata = ProductUpdateMeta.Field()
    product_clear_metadata = ProductClearMeta.Field()
    product_update_private_metadata = ProductUpdatePrivateMeta.Field()
    product_clear_private_metadata = ProductClearPrivateMeta.Field()

    product_image_create = ProductImageCreate.Field()
    product_image_delete = ProductImageDelete.Field()
    product_image_bulk_delete = ProductImageBulkDelete.Field()
    product_image_reorder = ProductImageReorder.Field()
    product_image_update = ProductImageUpdate.Field()

    product_type_create = ProductTypeCreate.Field()
    product_type_delete = ProductTypeDelete.Field()
    product_type_bulk_delete = ProductTypeBulkDelete.Field()
    product_type_update = ProductTypeUpdate.Field()
    product_type_reorder_attributes = ProductTypeReorderAttributes.Field()

    product_type_update_metadata = ProductTypeUpdateMeta.Field()
    product_type_clear_metadata = ProductTypeClearMeta.Field()
    product_type_update_private_metadata = ProductTypeUpdatePrivateMeta.Field()
    product_type_clear_private_metadata = ProductTypeClearPrivateMeta.Field()

    digital_content_create = DigitalContentCreate.Field()
    digital_content_delete = DigitalContentDelete.Field()
    digital_content_update = DigitalContentUpdate.Field()

    digital_content_url_create = DigitalContentUrlCreate.Field()

    product_variant_create = ProductVariantCreate.Field()
    product_variant_delete = ProductVariantDelete.Field()
    product_variant_bulk_create = ProductVariantBulkCreate.Field()
    product_variant_bulk_delete = ProductVariantBulkDelete.Field()
    product_variant_update = ProductVariantUpdate.Field()
    product_variant_translate = ProductVariantTranslate.Field()
    product_variant_update_metadata = ProductVariantUpdateMeta.Field()
    product_variant_clear_metadata = ProductVariantClearMeta.Field()
    product_variant_update_private_metadata = ProductVariantUpdatePrivateMeta.Field()
    product_variant_clear_private_metadata = ProductVariantClearPrivateMeta.Field()

    variant_image_assign = VariantImageAssign.Field()
    variant_image_unassign = VariantImageUnassign.Field()
