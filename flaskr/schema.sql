drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null
);


drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username string not null unique,
  password string not null
);

/*
このスキーマでは、テーブル（entries）を作成し、 id 、 title 、 text のカラムがあります。
id カラムはPrimaryKeyが自動で付加されます。 title 、 text は空白はNGです。
#sqlite3 /tmp/flaskr.db < schema.sql
*/
