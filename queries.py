# This file will contain the queries used for this project | similar to program_messages but 
# it's for queries.
get_uid_pwd = "SELECT uid, pwd FROM users;"
get_user_city = "SELECT city from users WHERE uid=?"
insert_into_births = "INSERT INTO births VALUES (?,?,?,?,?,?,?,?,?,?)"
insert_into_persons = "INSERT INTO persons VALUES (?,?,?,?,?,?)"
insert_into_marriages = "INSERT INTO marriages VALUES (?,?,?,?,?,?,?)"
get_first_last_name = 'SELECT fname, lname FROM persons WHERE fname = ? AND lname = ?'
get_reg_num_date = 'SELECT regno, regdate FROM registrations'

get_phone_address = "SELECT p.phone, p.address FROM persons p JOIN births b ON (p.fname, p.lname) = (b.m_fname, b.m_lname) WHERE m_fname = ? AND m_lname = ?"
get_pho_add = "SELECT phone, address FROM persons WHERE m_fname = ? AND m_lname = ?"


update_expiry = 'UPDATE registrations SET expiry = ? WHERE regno = ?'

insert_into_tickets = "INSERT INTO tickets VALUES (?,?,?,?,?)"