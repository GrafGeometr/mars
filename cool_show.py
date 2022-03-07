import sys
from data import db_session
from data.users import User

db_name = input()

db_session.global_init(db_name)
db_sess = db_session.create_session()
for colonist in db_sess.query(User).filter((User.address == "module_1"),
                                           (User.speciality.not_like("%engineer%")),
                                           (User.position.not_like("%engineer%"))):
    print(colonist.id)
