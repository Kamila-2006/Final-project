# 77 UZ


## Common:

## GET/api/v1/common/pages/ - меню страниц

## GET/api/v1/common/pages/ - посмотреть страницу

## GET/api/v1/common/regions-with-districts/ - список всех областей и районов Узбекистана

## GET/api/v1/common/setting/ - настройки


## Accounts:

## POST/api/v1/accounts/seller/registration/ - регистрация продавца

## POST/api/v1/accounts/login/ - логин

## POST/api/v1/accounts/token/refresh/ - обновить токен

## POST/api/v1/accounts/token/verify/ - проверить токен

## GET/api/v1/accounts/me/ - посмотреть свой профиль

## PUT/api/v1/accounts/edit/ - изменить свой профиль

## PATCH/api/v1/accounts/edit/ - частично изменить свой профиль


## Store:

## GET/api/v1/store/category/ - список основных категорий

## GET/api/v1/store/categories-with-children/ - список категорий с подкатегориями

## GET/api/v1/store/sub-category/ - список подкатегорий по id родительской категории

## POST/api/v1/store/ads/ - создать новое объявление

## GET/api/v1/store/ads/{slug}/ - посмотреть объявление

## GET/api/v1/store/ads/ - список объявлений

## GET/api/v1/store/my-ads/ - посмотреть список своих объявлений

## GET/api/v1/store/my-ads/{id}/ - посмотреть оно своё объявление

## PUT/api/v1/store/my-ads/{id}/ - изменить своё объявление

## PATCH/api/v1/store/my-ads/{id}/ - частично изменить своё объявление

## DELETE/api/v1/store/my-ads/{id}/ - удалить своё объявление

## GET/api/v1/store/product-download/{slug}/ - скачать объявление

## POST/api/v1/store/product-image-create/ - создать фото для объявления

## POST/api/v1/store/favourite-product-create/ - добавить товар в избранное (для продавца)

## POST/api/v1/store/favourite-product-create-by-id/ - добавить товар в избранное (для анонимного пользователя)

## GET/api/v1/store/my-favourite-product/ - посмотреть список избранных товаров (для продавца)

## GET/api/v1/store/my-favourite-product-by-id/ - посмотреть список избранных товаров (для анонимного пользователя)

## DELETE/api/v1/store//store/favourite-product/{id}/delete/ - удалить из избранного (для продавца)

## DELETE/api/v1/store//store/favourite-product-by-id/{id}/delete/ - удалить из избранного (для анонимного пользователя)