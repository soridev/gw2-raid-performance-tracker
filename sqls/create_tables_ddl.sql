-- ark_core.raid_kill_times definition

-- Drop table

-- DROP TABLE ark_core.raid_kill_times;

CREATE TABLE ark_core.raid_kill_times (
	log_id varchar(100) NOT NULL,
	encounter_name varchar(500) NULL,
	qualifying_date date NOT NULL,
	start_time timestamp NOT NULL,
	end_time timestamp NOT NULL,
	kill_duration_seconds int4 NOT NULL,
	success bool NOT NULL,
	cm bool NOT NULL,
	input_file varchar(1000) NOT NULL,
	CONSTRAINT pk_raid_kill_times PRIMARY KEY (log_id)
);

-- ark_core.players definition

-- Drop table

-- DROP TABLE ark_core.players;

CREATE TABLE ark_core.players (
	log_id varchar(100) NOT NULL,
	account_name varchar(300) NOT NULL,
	character_name varchar(300) NOT NULL,
	profession varchar(300) NOT NULL,
	CONSTRAINT pk_players PRIMARY KEY (log_id, account_name)
);


-- ark_core.players foreign keys

ALTER TABLE ark_core.players ADD CONSTRAINT fk_players_kill_times FOREIGN KEY (log_id) REFERENCES ark_core.raid_kill_times(log_id);

-- ark_core.raid_encounters definition

-- Drop table

-- DROP TABLE ark_core.raid_encounters;

CREATE TABLE ark_core.raid_encounters (
	encounter_name varchar(200) NOT NULL,
	ark_folder_name varchar(200) NOT NULL,
	has_cm bool NOT NULL,
	raid_wing int4 NOT NULL,
	wing_position int4 NULL,
	CONSTRAINT pk_raid_encounters PRIMARY KEY (encounter_name)
);

-- ark_core.guild_members definition

-- Drop table

-- DROP TABLE ark_core.guild_members;

CREATE TABLE ark_core.guild_members (
	guild_name varchar(300) NOT NULL,
	account_name varchar(300) NOT NULL,
	entry_date date NOT NULL,
	exit_date date NULL
);