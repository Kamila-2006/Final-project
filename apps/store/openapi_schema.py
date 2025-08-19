from drf_yasg import openapi

# ===============================
# 📄 Categories list
# ===============================
categories_list_response = openapi.Response(
    description="List of top-level categories",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                    "next": openapi.Schema(type=openapi.TYPE_STRING, nullable=True, example=None),
                    "previous": openapi.Schema(
                        type=openapi.TYPE_STRING, nullable=True, example=None
                    ),
                    "results": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                "name": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Electronics"
                                ),
                                "icon": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_URI,
                                    example="http://example.com/media/category_icons/electronics.png",
                                ),
                            },
                        ),
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📄 Categories with children
# ===============================
categories_with_children_response = openapi.Response(
    description="List of categories with their child categories",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                    "next": openapi.Schema(type=openapi.TYPE_STRING, nullable=True, example=None),
                    "previous": openapi.Schema(
                        type=openapi.TYPE_STRING, nullable=True, example=None
                    ),
                    "results": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                "name": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Electronics"
                                ),
                                "icon": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_URI,
                                    example="http://example.com/media/category_icons/electronics.png",
                                ),
                                "children": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(
                                                type=openapi.TYPE_INTEGER, example=11
                                            ),
                                            "name": openapi.Schema(
                                                type=openapi.TYPE_STRING, example="Smartphones"
                                            ),
                                            "icon": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                format=openapi.FORMAT_URI,
                                                example="http://example.com/media/category_icons/smartphones.png",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📄 Subcategories list
# ===============================
subcategories_list_response = openapi.Response(
    description="List of subcategories filtered by parent_id",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=3),
                    "next": openapi.Schema(type=openapi.TYPE_STRING, nullable=True, example=None),
                    "previous": openapi.Schema(
                        type=openapi.TYPE_STRING, nullable=True, example=None
                    ),
                    "results": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=11),
                                "name": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Smartphones"
                                ),
                                "icon": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_URI,
                                    example="http://example.com/media/category_icons/smartphones.png",
                                ),
                            },
                        ),
                    ),
                },
            ),
        },
    ),
)
# ===============================
# 📄 Ad create (POST /store/ads/)
# ===============================
ad_create_response = openapi.Response(
    description="Created ad",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                    "name": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone 14 Pro"),
                    "slug": openapi.Schema(type=openapi.TYPE_STRING, example="iphone-14-pro"),
                    "price": openapi.Schema(
                        type=openapi.TYPE_NUMBER, format="decimal", example=1200.50
                    ),
                    "photos": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                    ),
                    "photo": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                    "published_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                    ),
                    "address": openapi.Schema(type=openapi.TYPE_STRING, example="Tashkent"),
                    "seller": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            "full_name": openapi.Schema(
                                type=openapi.TYPE_STRING, example="Kamila Abdurahmanova"
                            ),
                            "phone_number": openapi.Schema(
                                type=openapi.TYPE_STRING, example="+998994053129"
                            ),
                            "profile_photo": openapi.Schema(
                                type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                            ),
                        },
                    ),
                    "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                    "updated_time": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📄 Ad detail (GET /store/ads/{slug}/)
# ===============================
ad_detail_response = openapi.Response(
    description="Detailed ad info",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                    "name": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone 14 Pro"),
                    "slug": openapi.Schema(type=openapi.TYPE_STRING, example="iphone-14-pro"),
                    "description": openapi.Schema(
                        type=openapi.TYPE_STRING, example="Brand new iPhone 14 Pro"
                    ),
                    "price": openapi.Schema(
                        type=openapi.TYPE_NUMBER, format="decimal", example=1200.50
                    ),
                    "photos": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                "image": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                                ),
                                "is_main": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                "product_id": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, example=101
                                ),
                                "created_at": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                                ),
                            },
                        ),
                    ),
                    "published_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                    ),
                    "address": openapi.Schema(type=openapi.TYPE_STRING, example="Tashkent"),
                    "seller": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            "full_name": openapi.Schema(
                                type=openapi.TYPE_STRING, example="Kamila Abdurahmanova"
                            ),
                            "phone_number": openapi.Schema(
                                type=openapi.TYPE_STRING, example="+998994053129"
                            ),
                            "profile_photo": openapi.Schema(
                                type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                            ),
                        },
                    ),
                    "category": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Electronics"),
                        },
                    ),
                    "view_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=15),
                    "updated_time": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                    ),
                    "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                },
            ),
        },
    ),
)
# ===============================
# 📄 Ad list (GET /store/list/ads/) с фильтрами
# ===============================
ad_list_response = openapi.Response(
    description="List of ads",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=20),
                    "next": openapi.Schema(type=openapi.TYPE_STRING, nullable=True, example=None),
                    "previous": openapi.Schema(
                        type=openapi.TYPE_STRING, nullable=True, example=None
                    ),
                    "results": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                                "name": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="iPhone 14 Pro"
                                ),
                                "slug": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="iphone-14-pro"
                                ),
                                "price": openapi.Schema(
                                    type=openapi.TYPE_NUMBER, format="decimal", example=1200.50
                                ),
                                "photo": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                                ),
                                "published_at": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                                ),
                                "address": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Tashkent"
                                ),
                                "seller": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                        "full_name": openapi.Schema(
                                            type=openapi.TYPE_STRING, example="Kamila Abdurahmanova"
                                        ),
                                        "phone_number": openapi.Schema(
                                            type=openapi.TYPE_STRING, example="+998994053129"
                                        ),
                                        "profile_photo": openapi.Schema(
                                            type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                                        ),
                                    },
                                ),
                                "updated_time": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                                ),
                                "is_liked": openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN, example=False
                                ),
                            },
                        ),
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📄 Параметры фильтра для Swagger
# ===============================
ad_list_filter_params = [
    openapi.Parameter(
        "price__gte", openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Minimum price"
    ),
    openapi.Parameter(
        "price__lte", openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Maximum price"
    ),
    openapi.Parameter(
        "seller_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Seller ID"
    ),
    openapi.Parameter(
        "district_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Seller district ID"
    ),
    openapi.Parameter(
        "region_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Seller region ID"
    ),
    openapi.Parameter(
        "category_ids",
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description="Comma separated category IDs",
    ),
]

# ===============================
# 📄 FavouriteProduct create
# ===============================
favourite_create_response = openapi.Response(
    description="Created favourite product",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                    "product": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                    "device_id": openapi.Schema(
                        type=openapi.TYPE_STRING, nullable=True, example="abc-123"
                    ),
                    "created_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📄 FavouriteProduct list
# ===============================
favourite_list_response = openapi.Response(
    description="List of favourite products",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                    "next": openapi.Schema(type=openapi.TYPE_STRING, nullable=True, example=None),
                    "previous": openapi.Schema(
                        type=openapi.TYPE_STRING, nullable=True, example=None
                    ),
                    "results": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                                "name": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="iPhone 14 Pro"
                                ),
                                "slug": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="iphone-14-pro"
                                ),
                                "description": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Brand new iPhone 14 Pro"
                                ),
                                "price": openapi.Schema(
                                    type=openapi.TYPE_NUMBER, format="decimal", example=1200.50
                                ),
                                "photo": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                                ),
                                "published_at": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                                ),
                                "address": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Tashkent"
                                ),
                                "seller": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Kamila Abdurahmanova"
                                ),
                                "updated_time": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                                ),
                                "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                            },
                        ),
                    ),
                },
            ),
        },
    ),
)
# ===============================
# 📄 Product image create (POST /store/product-image-create/)
# ===============================
product_image_create_response = openapi.Response(
    description="Created product image",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                    "is_main": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    "product_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                    "created_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📄 Product download (GET /store/product-download/{slug}/)
# ===============================
product_download_response = ad_detail_response  # Используем существующую схему ad_detail_response
# ===============================
# 📄 My Ads list (GET /store/my-ads/)
# ===============================
my_ads_list_response = openapi.Response(
    description="List of user's ads",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                    "next": openapi.Schema(type=openapi.TYPE_STRING, nullable=True, example=None),
                    "previous": openapi.Schema(
                        type=openapi.TYPE_STRING, nullable=True, example=None
                    ),
                    "results": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                                "name": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="iPhone 14 Pro"
                                ),
                                "slug": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="iphone-14-pro"
                                ),
                                "price": openapi.Schema(
                                    type=openapi.TYPE_NUMBER, format="decimal", example=1200.50
                                ),
                                "published_at": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                                ),
                                "address": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Tashkent"
                                ),
                                "status": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="active"
                                ),
                                "view_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=15),
                                "updated_time": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                                ),
                            },
                        ),
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📄 My Ad detail (GET, PUT, PATCH, DELETE /store/my-ads/{id}/)
# ===============================
my_ad_detail_response = openapi.Response(
    description="Detailed user's ad info",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                    "name": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone 14 Pro"),
                    "slug": openapi.Schema(type=openapi.TYPE_STRING, example="iphone-14-pro"),
                    "description": openapi.Schema(
                        type=openapi.TYPE_STRING, example="Brand new iPhone 14 Pro"
                    ),
                    "price": openapi.Schema(
                        type=openapi.TYPE_NUMBER, format="decimal", example=1200.50
                    ),
                    "category": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "photos": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                "image": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                                ),
                                "is_main": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                "product_id": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, example=101
                                ),
                                "created_at": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                                ),
                            },
                        ),
                    ),
                    "published_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                    ),
                    "status": openapi.Schema(type=openapi.TYPE_STRING, example="active"),
                    "view_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=15),
                    "updated_time": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📄 Category + Product Search list
# ===============================
category_product_search_response = openapi.Response(
    description="Search results for categories and products",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                        "name": openapi.Schema(type=openapi.TYPE_STRING, example="Electronics"),
                        "type": openapi.Schema(type=openapi.TYPE_STRING, example="category"),
                        "icon": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format=openapi.FORMAT_URI,
                            example="http://example.com/media/category_icons/electronics.png",
                        ),
                    },
                ),
            ),
        },
    ),
)

# ===============================
# 📄 Search complete results
# ===============================
search_complete_response = openapi.Response(
    description="Autocomplete search results for products",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                        "name": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone 14 Pro"),
                        "icon": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                    },
                ),
            ),
        },
    ),
)

# ===============================
# 📄 Search count increase
# ===============================
search_count_increase_response = openapi.Response(
    description="Increase search count for a product",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                    "category": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                    "search_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                    "updated_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📄 Popular search
# ===============================
popular_search_response = openapi.Response(
    description="List of most searched products",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                        "name": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone 14 Pro"),
                        "icon": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                        "search_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=15),
                    },
                ),
            ),
        },
    ),
)

# ===============================
# 📄 MySearch create
# ===============================
mysearch_create_response = openapi.Response(
    description="Created MySearch entry",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "category": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Electronics"),
                            "icon": openapi.Schema(
                                type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                            ),
                        },
                    ),
                    "search_query": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone 14"),
                    "price_min": openapi.Schema(
                        type=openapi.TYPE_NUMBER, format="decimal", example=500
                    ),
                    "price_max": openapi.Schema(
                        type=openapi.TYPE_NUMBER, format="decimal", example=1500
                    ),
                    "region_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    "created_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📄 MySearch list
# ===============================
mysearch_list_response = openapi.Response(
    description="List of MySearch entries",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        "category": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                                "name": openapi.Schema(
                                    type=openapi.TYPE_STRING, example="Electronics"
                                ),
                                "icon": openapi.Schema(
                                    type=openapi.TYPE_STRING, format=openapi.FORMAT_URI
                                ),
                            },
                        ),
                        "search_query": openapi.Schema(
                            type=openapi.TYPE_STRING, example="iPhone 14"
                        ),
                        "price_min": openapi.Schema(
                            type=openapi.TYPE_NUMBER, format="decimal", example=500
                        ),
                        "price_max": openapi.Schema(
                            type=openapi.TYPE_NUMBER, format="decimal", example=1500
                        ),
                        "region_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                        "created_at": openapi.Schema(
                            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
                        ),
                    },
                ),
            ),
        },
    ),
)

# ===============================
# 📄 MySearch delete
# ===============================
mysearch_delete_response = openapi.Response(
    description="Deleted MySearch entry",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "message": openapi.Schema(
                type=openapi.TYPE_STRING, example="MySearch entry deleted successfully"
            ),
        },
    ),
)
