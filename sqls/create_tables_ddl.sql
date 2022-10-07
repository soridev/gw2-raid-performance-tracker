-- public.auth_group definition

-- Drop table

-- DROP TABLE public.auth_group;

CREATE TABLE public.auth_group (
	id serial4 NOT NULL,
	"name" varchar(150) NOT NULL,
	CONSTRAINT auth_group_name_key UNIQUE (name),
	CONSTRAINT auth_group_pkey PRIMARY KEY (id)
);
CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


-- public.auth_user definition

-- Drop table

-- DROP TABLE public.auth_user;

CREATE TABLE public.auth_user (
	id serial4 NOT NULL,
	"password" varchar(128) NOT NULL,
	last_login timestamptz NULL,
	is_superuser bool NOT NULL,
	username varchar(150) NOT NULL,
	first_name varchar(150) NOT NULL,
	last_name varchar(150) NOT NULL,
	email varchar(254) NOT NULL,
	is_staff bool NOT NULL,
	is_active bool NOT NULL,
	date_joined timestamptz NOT NULL,
	CONSTRAINT auth_user_pkey PRIMARY KEY (id),
	CONSTRAINT auth_user_username_key UNIQUE (username)
);
CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


-- public.django_content_type definition

-- Drop table

-- DROP TABLE public.django_content_type;

CREATE TABLE public.django_content_type (
	id serial4 NOT NULL,
	app_label varchar(100) NOT NULL,
	model varchar(100) NOT NULL,
	CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model),
	CONSTRAINT django_content_type_pkey PRIMARY KEY (id)
);


-- public.django_migrations definition

-- Drop table

-- DROP TABLE public.django_migrations;

CREATE TABLE public.django_migrations (
	id bigserial NOT NULL,
	app varchar(255) NOT NULL,
	"name" varchar(255) NOT NULL,
	applied timestamptz NOT NULL,
	CONSTRAINT django_migrations_pkey PRIMARY KEY (id)
);


-- public.django_session definition

-- Drop table

-- DROP TABLE public.django_session;

CREATE TABLE public.django_session (
	session_key varchar(40) NOT NULL,
	session_data text NOT NULL,
	expire_date timestamptz NOT NULL,
	CONSTRAINT django_session_pkey PRIMARY KEY (session_key)
);
CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


-- public.guild_members definition

-- Drop table

-- DROP TABLE public.guild_members;

CREATE TABLE public.guild_members (
	id int8 NOT NULL DEFAULT nextval('elite_insider_api_guildmembers_id_seq'::regclass),
	guild_name varchar(300) NOT NULL,
	account_name varchar(300) NOT NULL,
	CONSTRAINT elite_insider_api_guildmembers_pkey PRIMARY KEY (id),
	CONSTRAINT unique_active_guildmembers UNIQUE (guild_name, account_name)
);


-- public.mechanic_info definition

-- Drop table

-- DROP TABLE public.mechanic_info;

CREATE TABLE public.mechanic_info (
	id int8 NOT NULL DEFAULT nextval('elite_insider_api_mechanicinfo_id_seq'::regclass),
	log_id varchar(100) NOT NULL,
	encounter_name varchar(500) NOT NULL,
	mechanic_name varchar(1000) NOT NULL,
	mechanic_description varchar(1000) NOT NULL,
	time_info float8 NOT NULL,
	actor varchar(300) NOT NULL,
	CONSTRAINT elite_insider_api_mechanicinfo_pkey PRIMARY KEY (id)
);


-- public.player_info definition

-- Drop table

-- DROP TABLE public.player_info;

CREATE TABLE public.player_info (
	id int8 NOT NULL DEFAULT nextval('elite_insider_api_playerinfo_id_seq'::regclass),
	log_id varchar(100) NOT NULL,
	account_name varchar(300) NOT NULL,
	character_name varchar(300) NOT NULL,
	profession varchar(300) NOT NULL,
	target_dps int4 NOT NULL,
	total_cc int4 NOT NULL,
	downstates int4 NOT NULL,
	died bool NOT NULL,
	CONSTRAINT elite_insider_api_playerinfo_pkey PRIMARY KEY (id)
);


-- public.raid_encounters definition

-- Drop table

-- DROP TABLE public.raid_encounters;

CREATE TABLE public.raid_encounters (
	encounter_name varchar(200) NOT NULL,
	arc_folder_name varchar(200) NOT NULL,
	has_cm bool NOT NULL,
	raid_wing int4 NOT NULL,
	boss_position int4 NOT NULL,
	relevant_boss bool NOT NULL,
	wing_name varchar(100) NOT NULL,
	CONSTRAINT raid_encounters_pkey PRIMARY KEY (encounter_name)
);
CREATE INDEX raid_encounters_encounter_name_462f9f03_like ON public.raid_encounters USING btree (encounter_name varchar_pattern_ops);


-- public.raid_kill_times definition

-- Drop table

-- DROP TABLE public.raid_kill_times;

CREATE TABLE public.raid_kill_times (
	log_id varchar(100) NOT NULL,
	encounter_name varchar(500) NOT NULL,
	qualifying_date date NOT NULL,
	start_time timestamptz NOT NULL,
	end_time timestamptz NOT NULL,
	kill_duration_seconds float8 NOT NULL,
	success bool NOT NULL,
	cm bool NOT NULL,
	input_file varchar(1000) NOT NULL,
	link_to_upload varchar(500) NULL,
	CONSTRAINT elite_insider_api_raidkilltimes_log_id_9f34f30c_pk PRIMARY KEY (log_id),
	CONSTRAINT elite_insider_api_raidkilltimes_log_id_9f34f30c_uniq UNIQUE (log_id)
);
CREATE INDEX elite_insider_api_raidkilltimes_log_id_9f34f30c_like ON public.raid_kill_times USING btree (log_id varchar_pattern_ops);


-- public.auth_permission definition

-- Drop table

-- DROP TABLE public.auth_permission;

CREATE TABLE public.auth_permission (
	id serial4 NOT NULL,
	"name" varchar(255) NOT NULL,
	content_type_id int4 NOT NULL,
	codename varchar(100) NOT NULL,
	CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename),
	CONSTRAINT auth_permission_pkey PRIMARY KEY (id),
	CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


-- public.auth_user_groups definition

-- Drop table

-- DROP TABLE public.auth_user_groups;

CREATE TABLE public.auth_user_groups (
	id bigserial NOT NULL,
	user_id int4 NOT NULL,
	group_id int4 NOT NULL,
	CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id),
	CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id),
	CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


-- public.auth_user_user_permissions definition

-- Drop table

-- DROP TABLE public.auth_user_user_permissions;

CREATE TABLE public.auth_user_user_permissions (
	id bigserial NOT NULL,
	user_id int4 NOT NULL,
	permission_id int4 NOT NULL,
	CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id),
	CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id),
	CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


-- public.django_admin_log definition

-- Drop table

-- DROP TABLE public.django_admin_log;

CREATE TABLE public.django_admin_log (
	id serial4 NOT NULL,
	action_time timestamptz NOT NULL,
	object_id text NULL,
	object_repr varchar(200) NOT NULL,
	action_flag int2 NOT NULL,
	change_message text NOT NULL,
	content_type_id int4 NULL,
	user_id int4 NOT NULL,
	CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0)),
	CONSTRAINT django_admin_log_pkey PRIMARY KEY (id),
	CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


-- public.auth_group_permissions definition

-- Drop table

-- DROP TABLE public.auth_group_permissions;

CREATE TABLE public.auth_group_permissions (
	id bigserial NOT NULL,
	group_id int4 NOT NULL,
	permission_id int4 NOT NULL,
	CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id),
	CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id),
	CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


-- public.guild_logs source

CREATE OR REPLACE VIEW public.guild_logs
AS SELECT gi.log_id,
    gi.guild_name,
    gi.encounter_name,
    gi.qualifying_date,
    gi.start_time,
    gi.end_time,
    gi.kill_duration_seconds,
    gi.success,
    gi.cm,
    gi.link_to_upload
   FROM ( SELECT rkt.log_id,
            rkt.qualifying_date,
            rkt.start_time,
            rkt.end_time,
            rkt.kill_duration_seconds,
            rkt.success,
            rkt.cm,
            rkt.link_to_upload,
            rkt.encounter_name,
            gm.guild_name,
            count(gm.account_name) AS "GUILD_COUNT"
           FROM raid_kill_times rkt
             JOIN player_info p ON rkt.log_id::text = p.log_id::text
             LEFT JOIN guild_members gm ON p.account_name::text = gm.account_name::text
             JOIN raid_encounters re ON replace(rkt.encounter_name::text, ' CM'::text, ''::text) = re.encounter_name::text
          WHERE p.account_name::text ~~ '%.____'::text
          GROUP BY rkt.log_id, rkt.qualifying_date, rkt.start_time, rkt.end_time, rkt.kill_duration_seconds, rkt.success, rkt.cm, rkt.link_to_upload, rkt.encounter_name, gm.guild_name) gi
  WHERE gi."GUILD_COUNT" >= 6;