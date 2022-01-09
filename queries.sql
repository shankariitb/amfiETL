CREATE TABLE `nav_records` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `scheme_id`  int(11) unsigned,
  `isin_div_payout_or_growth` varchar(100) NOT NULL DEFAULT '',
  `isin_div_reinvestment` varchar(100) NOT NULL DEFAULT '',
  `nav` float(10,4) NOT NULL DEFAULT '0.0000',
  `repurchase_price` float(10,4) NOT NULL DEFAULT '0.0000',
  `sale_price` float(10,4) NOT NULL DEFAULT '0.0000',
  `record_date` DATE NOT NULL DEFAULT '0000-00-00',
  `group_id` int(11) unsigned,
  `type_id` int(11) unsigned,
   PRIMARY KEY (`id`),
   KEY `scheme_id`(`scheme_id`),
   KEY `group_id`(`group_id`),
   KEY `type_id`(`type_id`),
);


CREATE TABLE `scheme_table`(
	`id` int (11) unsigned NOT NULL AUTO_INCREMENT,
	`scheme_id` varchar(250) NOT NULL,
	`name` text NOT NULL DEFAULT '',
	PRIMARY KEY(`id`),
	UNIQUE KEY`scheme_id`(`scheme_id`)
);


CREATE TABLE `group_table`(
	`id` int (11) unsigned NOT NULL AUTO_INCREMENT,
	`name` varchar(250) NOT NULL DEFAULT '',
	PRIMARY KEY(`id`),
	UNIQUE KEY`name`(`name`)
);

CREATE TABLE `type_table`(
	`id` int (11) unsigned NOT NULL AUTO_INCREMENT,
	`name` varchar(250) NOT NULL DEFAULT '',
	PRIMARY KEY(`id`),
	UNIQUE KEY`name`(`name`)
);

