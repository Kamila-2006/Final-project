from drf_yasg import openapi

# --------------------
# Seller Registration
# --------------------
seller_registration_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Test User"),
        "project_name": openapi.Schema(type=openapi.TYPE_STRING, example="Test project"),
        "category": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998123456789"),
        "address": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Test address"),
                "lat": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=41.299496),
                "long": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=69.240073),
            },
            required=["name", "lat", "long"],
        ),
    },
    required=["full_name", "project_name", "category", "phone_number", "address"],
)

seller_registration_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "data": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=4),
                "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Test User"),
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, example="Test project"),
                "category": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "category_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998123456789"),
                "status": openapi.Schema(type=openapi.TYPE_STRING, example="pending"),
                "address": openapi.Schema(type=openapi.TYPE_STRING, example="Test address"),
            },
        ),
    },
)
# --------------------
# Login
# --------------------
login_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998123456789"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, example="testpassword"),
    },
    required=["phone_number", "password"],
)

login_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "data": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access_token": openapi.Schema(
                    type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                ),
                "refresh_token": openapi.Schema(
                    type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                ),
                "user": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=4),
                        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Test User"),
                        "phone_number": openapi.Schema(
                            type=openapi.TYPE_STRING, example="+998123456789"
                        ),
                    },
                ),
            },
        ),
    },
)
# --------------------
# Token Verify
# --------------------
token_verify_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "token": openapi.Schema(
            type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        ),
    },
    required=["token"],
)

token_verify_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "data": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "valid": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                "user_id": openapi.Schema(
                    type=openapi.TYPE_STRING, example="b67b5e98-cc09-48db-8c3b-0a5edcb8b1a1"
                ),
            },
        ),
    },
)
# --------------------
# Token Refresh
# --------------------
token_refresh_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "refresh": openapi.Schema(
            type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        ),
    },
    required=["refresh"],
)

token_refresh_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access": openapi.Schema(
            type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        ),
    },
)
# ---------- /accounts/me/ ----------

me_response = openapi.Response(
    description="User profile data",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=4),
                    "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Test User"),
                    "phone_number": openapi.Schema(
                        type=openapi.TYPE_STRING, example="+998123456789"
                    ),
                    "profile_photo": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        nullable=True,
                        example=None,
                    ),
                    "address": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING, example="Test address"
                            ),
                            "lat": openapi.Schema(
                                type=openapi.TYPE_NUMBER, format="float", example=41.299496
                            ),
                            "long": openapi.Schema(
                                type=openapi.TYPE_NUMBER, format="float", example=69.240073
                            ),
                        },
                    ),
                },
            ),
        },
    ),
)
# ---------- /accounts/edit/ (PUT) ----------
edit_put_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["full_name", "phone_number", "address"],
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Karimov Rustam Akmalovich"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998991234567"),
        "address": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "lat", "long"],
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
                ),
                "lat": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=41.299436),
                "long": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=69.240072),
            },
        ),
    },
)

edit_response = openapi.Response(
    description="User profile successfully updated",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=4),
                    "full_name": openapi.Schema(
                        type=openapi.TYPE_STRING, example="Karimov Rustam Akmalovich"
                    ),
                    "phone_number": openapi.Schema(
                        type=openapi.TYPE_STRING, example="+998991234567"
                    ),
                    "profile_photo": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        nullable=True,
                        example=None,
                    ),
                    "address": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example=(
                                    "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
                                ),
                            ),
                            "lat": openapi.Schema(
                                type=openapi.TYPE_NUMBER, format="float", example=41.299436
                            ),
                            "long": openapi.Schema(
                                type=openapi.TYPE_NUMBER, format="float", example=69.240072
                            ),
                        },
                    ),
                },
            ),
        },
    ),
)

# ---------- /accounts/edit/ (PATCH) ----------
edit_patch_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Karimov Rustam Akmalovich"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998991234567"),
        "address": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
                ),
                "lat": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=41.299436),
                "long": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=69.240072),
            },
        ),
    },
)
