--Users table
create table if not exists User (
    Id integer primary key autoincrement,
    Name text not null,
    Email text not null,
    Password text not null
);

--Type of event table
create table if not exists EventType (
  Id integer primary key,
  Type text not null
);

--Events table
create table if not exists Event (
    Id integer primary key autoincrement,
    Name text not null,
    EventTypeId integer,
    StartTime integer not null,
    EndTime integer not null,
    Organizer text not null,
    Description text not null,
    LocationId integer,
    foreign key(LocationId) references Location(Id),
    foreign key(EventTypeId) references EventType(Id)
);

--Localization table
create table if not exists Location (
  Id integer primary key autoincrement,
  City text not null,
  AddressLine1 text not null,
  AddressLine2 text not null,
  Latitude real not null,
  Longitude real not null
);

