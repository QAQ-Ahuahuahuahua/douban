/*
Navicat MySQL Data Transfer

Source Server         : haha
Source Server Version : 50711
Source Host           : localhost:3306
Source Database       : douban

Target Server Type    : MYSQL
Target Server Version : 50711
File Encoding         : 65001

Date: 2017-01-02 18:58:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for doing_comment
-- ----------------------------
DROP TABLE IF EXISTS `doing_comment`;
CREATE TABLE `doing_comment` (
  `userName` varchar(20) DEFAULT NULL,
  `credit` varchar(10) DEFAULT NULL,
  `grade` int(5) DEFAULT NULL,
  `time` varchar(20) DEFAULT NULL,
  `comment` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
