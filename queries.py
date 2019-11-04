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



# arthur
get_latest_owner = "select fname, lname, regno from registrations where vin = ? order by regdate desc"
not_current_owner = "That is not the current owner"
update_current = "update registrations set expiry = ? where regno = ?"
new_registrations = "insert into registrations values(?,?,?,?,?,?,?)"

insert_payment = "INSERT into payments values(?,?,?)"
get_fine = "select fine from tickets where tno = ?"
get_sum = "select sum(amount) from payments where tno = ?"


get_demerit = "select count(*), sum(points) from demeritNotices where fname = ? and lname = ?"
get_demerit2 = "select count(*), sum(points) from demeritNotices where fname = ? and lname = ? and ddate>?"

get_regno = "select  t.regno from tickets t , registrations r where r.fname = ? and r.lname = ? and r.regno = t.regno"
get_regno_ordered = "select  t.regno from tickets t , registrations r where r.fname = ? and r.lname = ? and r.regno = t.regno order by t.vdate desc "

get_regno_dis = "select distinct t.regno from tickets t , registrations r where r.fname = ? and r.lname = ? and r.regno = t.regno"
get_regno_ordered_dis = "select distinct t.regno from tickets t , registrations r where r.fname = ? and r.lname = ? and r.regno = t.regno order by t.vdate desc "


get_tickets = "select count(*) from tickets where regno = ?"
get_tickets2 = "select count(*) from tickets where regno = ? and vdate > ?"
get_ticket_desc = "select distinct t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model from tickets t, vehicles v, registrations r where t.regno = ? and r.vin =v.vin and r.regno = t.regno"
get_ticket_desc2 = "select distinct t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model from tickets t, vehicles v, registrations r where t.regno = ? and r.vin =v.vin and r.regno = t.regno and t.vdate > ?"
