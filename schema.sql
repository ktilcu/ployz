drop table if exists ployz;
create table ployz (
  id integer primary key autoincrement,
  message string not null,
  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);