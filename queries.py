# This file will contain the queries used for this project | similar to program_messages but 
# it's for queries.
get_uid_pwd = "SELECT uid, pwd FROM users;"
get_user_city = "SELECT city from users WHERE uid=?"
insert_into_births = "INSERT INTO births VALUES (?,?,?,?,?,?,?,?,?,?)"
insert_into_persons = "INSERT INTO persons VALUES (?,?,?,?,?,?)"

get_phone_address = "SELECT phone, address FROM persons p JOIN births b ON (p.fname, p.lname) = (b.m_fname, b.m_lname) WHERE m_fname = ? AND m_lname = ?"