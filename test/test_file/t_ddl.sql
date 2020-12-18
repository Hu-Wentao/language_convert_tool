
-- public.wms_material definition

-- Drop table

-- DROP TABLE public.wms_material;

CREATE TABLE public.wms_material (
	id varchar(36) NOT NULL,
	"materialNo" varchar(20) NULL,
	"materialName" varchar(60) NULL,
	"materialType" varchar(36) NULL,
	unit varchar(36) NULL,
	"rackId" varchar(36) NULL,
	"stockAreaId" varchar(36) NULL,
	"warehouseId" varchar(36) NULL,
	qty numeric NULL,
	"expiryAt" numeric NULL,
	"isDel" bool NULL,
	remark varchar(255) NULL,
	"createBy" varchar(36) NULL,
	"createAt" timestamp NULL,
	"updateBy" varchar(36) NULL,
	"updateAt" timestamp NULL,
	CONSTRAINT "_material_id" PRIMARY KEY (id)
);


-- public.wms_menu definition

-- Drop table

-- DROP TABLE public.wms_menu;

CREATE TABLE public.wms_menu (
	id varchar(36) NOT NULL,
	"menuName" varchar(50) NULL,
	"menuUrl" varchar(50) NULL,
	"menuIcon" varchar(50) NULL,
	"menuParent" varchar(36) NULL,
	sort int4 NULL,
	status bool NULL,
	"menuType" varchar(10) NULL,
	"isDel" bool NOT NULL,
	remark varchar(255) NULL,
	"createBy" varchar(36) NULL,
	"createAt" timestamp NULL,
	"updateBy" varchar(36) NULL,
	"updateAt" timestamp NULL,
	CONSTRAINT "_menu_id" PRIMARY KEY (id)
);

