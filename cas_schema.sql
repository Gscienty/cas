use cas;

create table application (
    domain varchar(64) primary key,
    name varchar(32) not null,
    callback_url varchar(128) not null,
    available tinyint not null,
    tgt_expire integer not null,
    st_expire integer not null
);

create table user_principal (
    username varchar(64) primary key,
    password char(64) not null,
    available tinyint not null,
    profile TEXT
);

create table ticket_grant_ticket (
    token varchar(64) primary key,
    username varchar(64) not null,
    create_time TIMESTAMP not null,
    expire TIMESTAMP not null
);

create table server_ticket (
    token varchar(64) primary key,
    username varchar(64) not null,
    domain varchar(64) not null,
    create_time TIMESTAMP not null,
    expire TIMESTAMP not null
);

create table user_permission (
    username varchar(64) primary key,
    domain varchar(64) not null,
    tag varchar(32) not null,
    available tinyint not null
);
