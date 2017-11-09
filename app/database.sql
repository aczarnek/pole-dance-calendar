--Users table
drop table if exists User;
create table User (
    Id integer primary key autoincrement,
    Name text not null,
    Email text not null,
    Password text not null
);

--Events table
drop table if exists Event;
create table Event (
    Id integer primary key autoincrement,
    Name text not null,
    Type text not null,
    StartTime integer not null,
    EndTime integer not null,
    Organizer text not null,
    Description text not null,
    foreign key(LocalizationId) references Localization(Id)

);

--Localization table
drop table if exists Localization;
create table Localization (
  Id integer primary key autoincrement,
  City text not null,
  AddressLine1 text not null,
  AddressLine2 text not null,
  Latitude real not null,
  Longitude real not null
)