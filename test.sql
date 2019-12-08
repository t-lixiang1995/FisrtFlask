/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 80011
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 80011
File Encoding         : 65001

Date: 2019-12-05 16:33:50
*/

SET FOREIGN_KEY_CHECKS=0;


-- ----------------------------
-- Records of roletoresource
-- ----------------------------

INSERT INTO `roletoresource` VALUES ('1', '91');
INSERT INTO `roletoresource` VALUES ('1', '92');
INSERT INTO `roletoresource` VALUES ('1', '93');
INSERT INTO `roletoresource` VALUES ('1', '94');
INSERT INTO `roletoresource` VALUES ('1', '95');
INSERT INTO `roletoresource` VALUES ('1', '96');
INSERT INTO `roletoresource` VALUES ('1', '97');
INSERT INTO `roletoresource` VALUES ('1', '98');
INSERT INTO `roletoresource` VALUES ('1', '99');
INSERT INTO `roletoresource` VALUES ('1', '100');
INSERT INTO `roletoresource` VALUES ('1', '101');

-- ----------------------------
-- Records of sys_resource
-- ----------------------------

INSERT INTO `sys_resource` VALUES ('91', '用户管理', '/modules/usermanage', null, '0', '1', 'menu', '19', '1');
INSERT INTO `sys_resource` VALUES ('92', '查看', '', 'modules:usermanage:list', '91', '2', null, '0', '1');
INSERT INTO `sys_resource` VALUES ('93', '新增', null, 'modules:usermanage:save', '91', '2', null, '0', '1');
INSERT INTO `sys_resource` VALUES ('94', '修改', null, 'modules:usermanage:update', '91', '2', null, '0', '1');
INSERT INTO `sys_resource` VALUES ('95', '删除', null, 'modules:usermanage:delete', '91', '2', null, '0', '1');
INSERT INTO `sys_resource` VALUES ('96', '详情', null, 'modules:usermanage:info', '91', '2', null, '0', '1');
INSERT INTO `sys_resource` VALUES ('97', '企业管理', '/modules/enterprise', null, '0', '1', 'menu', '20', '1');
INSERT INTO `sys_resource` VALUES ('98', '查看', null, 'modules:enterprise:list', '97', '2', null, '0', '1');
INSERT INTO `sys_resource` VALUES ('99', '新增', null, 'modules:enterprise:save', '97', '2', null, '0', '1');
INSERT INTO `sys_resource` VALUES ('100', '修改', null, 'modules:enterprise:update', '97', '2', null, '0', '1');
INSERT INTO `sys_resource` VALUES ('101', '删除', null, 'modules:enterprise:delete', '97', '2', null, '0', '1');


-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES ('1', '系统管理员', 'adsadmin', '系统管理员[depoly]', '1', '2019-10-15 11:00:49');


-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES ('admin', 'admin', '管理员', '124@qq.com', '13527567790', '0108745890', '$6$rounds=656000$0m3WbgCQZpmJhoOW$85sg..cANF.9RMwz0fFnnQas8.IeoVuIsocQ7KWMppoCfnsG/b8drplkDW9veAkNvnG1pRvyytga2uQJBBKIZ/', '1', '1', 'ALBB', '阿里巴巴', '达摩院', '2019-11-26 10:38:33', 'admin', null);
