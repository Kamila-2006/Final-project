from drf_yasg import openapi

# ===============================
# 📄 Pages list
# ===============================
page_list_response = openapi.Response(
    description="List of pages",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "slug": openapi.Schema(type=openapi.TYPE_STRING, example="about-us"),
                        "title": openapi.Schema(type=openapi.TYPE_STRING, example="О нас"),
                    },
                ),
            ),
        },
    ),
)

# ===============================
# 📄 Page detail
# ===============================
page_detail_response = openapi.Response(
    description="Detailed page info",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "slug": openapi.Schema(type=openapi.TYPE_STRING, example="about-us"),
                    "title": openapi.Schema(type=openapi.TYPE_STRING, example="О нас"),
                    "content": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Мы крупнейший онлайн-рынок в Узбекистане.",
                    ),
                    "created_time": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATETIME,
                        example="2025-08-06T23:19:46.001308+05:00",
                    ),
                    "updated_time": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATETIME,
                        example="2025-08-06T23:19:46.001308+05:00",
                    ),
                },
            ),
        },
    ),
)

# ===============================
# 📍 Regions with districts
# ===============================
regions_with_districts_response = openapi.Response(
    description="List of regions with their districts",
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
                        "name": openapi.Schema(
                            type=openapi.TYPE_STRING, example="Андижанская область"
                        ),
                        "districts": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                    "name": openapi.Schema(
                                        type=openapi.TYPE_STRING, example="Балыкчинский район"
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
        },
    ),
)

# ===============================
# ⚙️ Settings
# ===============================
setting_response = openapi.Response(
    description="Site settings",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "phone": openapi.Schema(type=openapi.TYPE_STRING, example="+998994053129"),
                        "support_email": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format=openapi.FORMAT_EMAIL,
                            example="abdurahmanovakamila.2006@gmail.com",
                        ),
                        "working_hours": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Понедельник-Воскресенье 9:00-21:00",
                        ),
                        "app_version": openapi.Schema(type=openapi.TYPE_STRING, example="v1"),
                        "maintenance_code": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, example=False
                        ),
                    },
                ),
            ),
        },
    ),
)
