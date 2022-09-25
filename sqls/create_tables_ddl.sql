-- public.fullclear_settings definition

-- Drop table

-- DROP TABLE public.fullclear_settings;

CREATE TABLE public.fullclear_settings (
	guild_name varchar NOT NULL,
	raid_weekday int4 NOT NULL,
	number_of_players_treshhold int4 NOT NULL,
	CONSTRAINT pk_fullclear_settings PRIMARY KEY (guild_name, raid_weekday)
);

-- public.guild_members definition

-- Drop table

-- DROP TABLE public.guild_members;

CREATE TABLE public.guild_members (
	guild_name varchar(300) NOT NULL,
	account_name varchar(300) NOT NULL,
	entry_date date NOT NULL,
	exit_date date NULL,
	CONSTRAINT pk_guild_members PRIMARY KEY (guild_name, account_name)
);


-- public.raid_encounters definition

-- Drop table

-- DROP TABLE public.raid_encounters;

CREATE TABLE public.raid_encounters (
	encounter_name varchar(200) NOT NULL,
	ark_folder_name varchar(200) NOT NULL,
	has_cm bool NOT NULL,
	raid_wing int4 NOT NULL,
	wing_position int4 NULL,
	relevant_boss bool NOT NULL DEFAULT true,
	CONSTRAINT pk_raid_encounters PRIMARY KEY (encounter_name)
);

-- public.raid_kill_times definition

-- Drop table

-- DROP TABLE public.raid_kill_times;

CREATE TABLE public.raid_kill_times (
	log_id varchar(100) NOT NULL,
	encounter_name varchar(500) NULL,
	qualifying_date date NOT NULL,
	start_time timestamp NOT NULL,
	end_time timestamp NOT NULL,
	kill_duration_seconds float4 NOT NULL,
	success bool NOT NULL,
	cm bool NOT NULL,
	input_file varchar(1000) NOT NULL,
	CONSTRAINT pk_raid_kill_times PRIMARY KEY (log_id)
);


-- public.player_info definition

-- Drop table

-- DROP TABLE public.player_info;

CREATE TABLE public.player_info (
	log_id varchar(100) NOT NULL,
	account_name varchar(300) NOT NULL,
	character_name varchar(300) NOT NULL,
	profession varchar(300) NOT NULL,
	target_dps int4 NOT NULL,
	total_cc int4 NOT NULL,
	downstates int4 NOT NULL,
	died bool NOT NULL,
	CONSTRAINT pk_players PRIMARY KEY (log_id, account_name)
);


-- public.player_info foreign keys

ALTER TABLE public.player_info ADD CONSTRAINT fk_players_kill_times FOREIGN KEY (log_id) REFERENCES public.raid_kill_times(log_id);


-- public.log_mapping definition

-- Drop table

-- DROP TABLE public.log_mapping;

CREATE TABLE public.log_mapping (
	log_id varchar(100) NOT NULL,
	clear_id varchar(100) NOT NULL,
	CONSTRAINT pk_log_mapping PRIMARY KEY (log_id, clear_id)
);


-- public.log_mapping foreign keys

ALTER TABLE public.log_mapping ADD CONSTRAINT fk_log_mapping_raid_kill_times FOREIGN KEY (log_id) REFERENCES public.raid_kill_times(log_id);