--Users table

drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username_field text not null,
    email_address text not null,
    user_password text not null,
    confirm_user_password text not null
);

--Events table
drop table if exists events;
create table events (
    id integer primary key autoincrement,
    event_name text not null,
    event_date_from integer not null,
    event_date_to integer not null,
    organizers text not null,
    description text not null,
    place text not null,
    latitude real not null,
    longitude real not null
);

