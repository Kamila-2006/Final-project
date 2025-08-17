from drf_yasg import openapi

# -----------------------------
# Seller Registration
# -----------------------------
seller_registration_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Karimov Akmal Rustamovich"),
        "project_name": openapi.Schema(
            type=openapi.TYPE_STRING, example="TechnoMart Online Do'koni"
        ),
        "category": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998971234569"),
        "address": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 15-uy",
                ),
                "lat": openapi.Schema(type=openapi.TYPE_NUMBER, example=41.299496),
                "long": openapi.Schema(type=openapi.TYPE_NUMBER, example=69.240073),
            },
        ),
    },
    required=["full_name", "project_name", "category", "phone_number", "address"],
)

seller_registration_response = openapi.Response(
    description="Seller registration response",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=9),
                    "full_name": openapi.Schema(
                        type=openapi.TYPE_STRING, example="Karimov Akmal Rustamovich"
                    ),
                    "project_name": openapi.Schema(
                        type=openapi.TYPE_STRING, example="TechnoMart Online Do'koni"
                    ),
                    "category": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "category_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "phone_number": openapi.Schema(
                        type=openapi.TYPE_STRING, example="+998971234569"
                    ),
                    "status": openapi.Schema(type=openapi.TYPE_STRING, example="pending"),
                    "address": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 15-uy",
                    ),
                },
            ),
        },
    ),
)

# -----------------------------
# Login
# -----------------------------
login_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="998994053129"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, example="secretpassword"),
    },
    required=["phone_number", "password"],
)

login_response = openapi.Response(
    description="Login response",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access_token": openapi.Schema(
                        type=openapi.TYPE_STRING, example="jwt-access-token-here"
                    ),
                    "refresh_token": openapi.Schema(
                        type=openapi.TYPE_STRING, example="jwt-refresh-token-here"
                    ),
                    "user": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            "full_name": openapi.Schema(
                                type=openapi.TYPE_STRING, example="Abdurahmanova Kamila"
                            ),
                            "phone_number": openapi.Schema(
                                type=openapi.TYPE_STRING, example="998994053129"
                            ),
                        },
                    ),
                },
            ),
        },
    ),
)

# -----------------------------
# Token Refresh
# -----------------------------
token_refresh_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "refresh": openapi.Schema(type=openapi.TYPE_STRING, example="jwt-refresh-token-here"),
    },
    required=["refresh"],
)

token_refresh_response = openapi.Response(
    description="Token refresh response",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access": openapi.Schema(
                        type=openapi.TYPE_STRING, example="jwt-new-access-token"
                    ),
                },
            ),
        },
    ),
)

# -----------------------------
# Token Verify
# -----------------------------
token_verify_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "token": openapi.Schema(type=openapi.TYPE_STRING, example="jwt-access-token-here"),
    },
    required=["token"],
)

token_verify_response = openapi.Response(
    description="Token verify response",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "valid": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    "user_id": openapi.Schema(
                        type=openapi.TYPE_STRING, example="9b5badfd-ccc4-4b32-b879-2abd66acda7f"
                    ),
                },
            ),
        },
    ),
)

# -----------------------------
# Me (Profile)
# -----------------------------
me_response = openapi.Response(
    description="Profile info",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "full_name": openapi.Schema(
                        type=openapi.TYPE_STRING, example="Abdurahmanova Kamila"
                    ),
                    "phone_number": openapi.Schema(
                        type=openapi.TYPE_STRING, example="998994053129"
                    ),
                    "profile_photo": openapi.Schema(
                        type=openapi.TYPE_STRING, example=None, nullable=True
                    ),
                    "address": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="Ташкентская область, Паркентский район, улица Нафосат",
                            ),
                            "lat": openapi.Schema(type=openapi.TYPE_NUMBER, example=34599.0),
                            "long": openapi.Schema(type=openapi.TYPE_NUMBER, example=47697.0),
                        },
                    ),
                },
            ),
        },
    ),
)

# -----------------------------
# Edit Profile
# -----------------------------
edit_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Karimov Rustam Akmalovich"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998971234568"),
        "address": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
                ),
                "lat": openapi.Schema(type=openapi.TYPE_NUMBER, example=41.299436),
                "long": openapi.Schema(type=openapi.TYPE_NUMBER, example=69.240072),
            },
        ),
    },
)

edit_response = me_response
