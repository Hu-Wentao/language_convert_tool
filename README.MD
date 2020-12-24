# 转换工具

## 功能

[x] 实现 MySQL -> DDL

[x] 实现 DDL  -> ddl_json


[x] 实现 ddl_json -> Dart Entity

[x] 实现 ddl_json -> Dart Dto

[x] 实现 ddl_json -> DDL

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
            {"field": "id", "type": "varchar(36)"}
        ],
        "primary": {"field": "id","name": "_material_id"}
    }
]
```