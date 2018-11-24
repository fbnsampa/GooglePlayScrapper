-- Table: apps

-- DROP TABLE apps;

CREATE TABLE apps
(
    app_id character varying(512) NOT NULL,
    app_name character varying(140) NOT NULL,
    author character varying(140),
    genre character varying(140),
    description text[] COLLATE pg_catalog."default",
    downloads character varying(140),
    reviews character varying(140),
    rating character varying(140),
    price character varying(140),
    app_version character varying(140),
    compability character varying(140),
    filesize character varying(140),
    updated character varying(140),
    CONSTRAINT apps_pkey PRIMARY KEY (app_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE apps
    OWNER to postgres;