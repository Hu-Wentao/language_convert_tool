# 转换工具

## 目标

[x] 实现MySQL -> PostgreSQL DDL
[x] 实现 DDL  -> ddl_json

[x] 实现 ddl_json->-> Dart Entity

[x] 实现 ddl_json->-> Dart Dto

## ddl_json 示例

```json
[
    {
        "schema": "public",
        "table": "wms_material",
        "fields": [
            {"field": "id", "type": "varchar(36)"},
            {"field": "updateAt", "type": "timestamp"}
        ],
        "primary": {"field": "id","name": "_material_id"}
    },
    {
        "schema": "public",
        "table": "wms_material",
        "fields": [
            {"field": "id", "type": "varchar(36)"},
        ],
        "primary": {"field": "id","name": "_material_id"}
    },
]
```