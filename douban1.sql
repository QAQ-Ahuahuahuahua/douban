/*
Navicat MySQL Data Transfer

Source Server         : haha
Source Server Version : 50711
Source Host           : localhost:3306
Source Database       : douban1

Target Server Type    : MYSQL
Target Server Version : 50711
File Encoding         : 65001

Date: 2017-01-02 19:13:20
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `username` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL,
  `city` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL,
  `comment_time` varchar(20) DEFAULT NULL,
  `star` varchar(20) DEFAULT NULL,
  `grade` int(10) DEFAULT NULL,
  `comment` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
