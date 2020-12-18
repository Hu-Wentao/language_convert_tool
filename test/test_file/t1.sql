DROP TABLE IF EXISTS `sys_dept`;
CREATE TABLE `sys_dept`  (
  `DeptId` bigint(20) NOT NULL,
  `DeptNo` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `DeptName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `IsDel` tinyint(4) NOT NULL COMMENT '1未删除   0删除',
  `Remark` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `CreateBy` bigint(20) NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifiedBy` bigint(20) NULL DEFAULT NULL COMMENT '修改人',
  `ModifiedDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`DeptId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sys_menu_wms
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu_wms`;
CREATE TABLE `sys_menu_wms`  (
  `MenuId` bigint(20) NOT NULL,
  `MenuName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `MenuUrl` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `MenuIcon` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `MenuParent` bigint(20) NULL DEFAULT NULL,
  `Sort` int(11) NULL DEFAULT NULL,
  `Status` tinyint(4) NULL DEFAULT NULL COMMENT '启用1 禁用0',
  `MenuType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'menu btn',
  `IsDel` tinyint(4) NOT NULL COMMENT '1未删除   0删除',
  `Remark` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `CreateBy` bigint(20) NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifiedBy` bigint(20) NULL DEFAULT NULL COMMENT '修改人',
  `ModifiedDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`MenuId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for wms_storagerack
-- ----------------------------
DROP TABLE IF EXISTS `wms_storagerack`;
CREATE TABLE `wms_storagerack`  (
  `StorageRackId` bigint(20) NOT NULL COMMENT '货架Id',
  `StorageRackNo` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '货架编号',
  `StorageRackName` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '货架名称',
  `ReservoirAreaId` bigint(20) NOT NULL COMMENT '所属库区',
  `Remark` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `IsDel` tinyint(4) NULL DEFAULT NULL COMMENT '1 0',
  `CreateBy` bigint(20) NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifiedBy` bigint(20) NULL DEFAULT NULL COMMENT '修改人',
  `ModifiedDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  `WarehouseId` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`StorageRackId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
