-- Table: public.apps

-- DROP TABLE public.apps;

CREATE TABLE public.apps
(
    app_id character varying(512) COLLATE pg_catalog."default" NOT NULL,
    app_name character varying(140) COLLATE pg_catalog."default" NOT NULL,
    author character varying(140) COLLATE pg_catalog."default",
    genre character varying(140) COLLATE pg_catalog."default",
    description text[] COLLATE pg_catalog."default",
    downloads integer,
    reviews integer,
    rating double precision,
    price double precision,
    app_version character varying(140) COLLATE pg_catalog."default",
    compability character varying(140) COLLATE pg_catalog."default",
    filesize integer,
    updated date,
    app_products character varying COLLATE pg_catalog."default",
    CONSTRAINT apps_pkey PRIMARY KEY (app_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.apps
    OWNER to postgres;