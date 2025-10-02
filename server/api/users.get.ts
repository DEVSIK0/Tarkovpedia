import Database from "better-sqlite3";

export default defineEventHandler(async () => {
  const db = new Database("./data/tarkovpedia.db");
  const users = db.prepare("SELECT * FROM user").all();
  db.close();
  return users;
});
