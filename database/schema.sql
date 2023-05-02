CREATE TABLE IF NOT EXISTS `blacklist` (
  `user_id` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `zones` (
  `name` varchar(255) NOT NULL,
  `continent` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `url_name` varchar(255) NOT NULL,
  `friendly_name` varchar(255),
  `name_in_who` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `above_45` BOOLEAN NOT NULL,
  `key_required` BOOLEAN NOT NULL,
  `firepot_port` BOOLEAN NOT NULL,
  `shaman_port` BOOLEAN NOT NULL,
  `druid_port` BOOLEAN NOT NULL,
  `wizard_port` BOOLEAN NOT NULL,
  `level_of_monsters` varchar(255) NOT NULL,
  `zem_value` varchar(255) NOT NULL,
  `succor_evac` varchar(255) NOT NULL,
  `zone_spawn_timer` varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `connections` (
  `zone` varchar(255) NOT NULL,
  `connected_to` varchar(255) NOT NULL,
  `ocean_connection` BOOLEAN NOT NULL,
  `one_way_connection` BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS `links` (
  `zone` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,# monster, npc, item, quests, guilds, city_races, tradeskill facilities, guides
  `url` varchar(255) NOT NULL
);