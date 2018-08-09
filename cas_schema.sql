use cas;

create table application (
    domain varchar(64) primary key,
    name varchar(32) not null,
    available tinyint not null,
    tgt_expire integer not null,
    st_expire integer not null
);

create table application_user (
    username varchar(64) primary key,
    password char(64) not null,
    available tinyint not null
);
