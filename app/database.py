import sqlalchemy
from data.users import User
from data.db_session import create_session, global_init


class DataBase():
    db_name = "db_game.sqlite"
    global_init(db_name)
    def add_user(self, params):
        user = User()
        user.email = params["email"]
        user.name = params["name"]
        user.surname = params["surname"]
        user.hashed_password = params["password"]
        db_sess = create_session()
        db_sess.add(user)
        db_sess.commit()

    def get_inf(self, params):
        db_sess = create_session()
        name1, surname1 = params["name"], params["surname"]
        res = db_sess.query(User).filter(User.email == params["email"].lower())
        print(name1, surname1)
        # res = db_sess.query(User).filter((User.name == name1), (User.surname == surname1))
        # print(type(res))
        # print(res)
        print(res.params())
        el = res.first()
        print(1)
        print(el)
        print(2)
        if el is None:
            self.add_user(params)
        else:
            if el.hashed_password != params["password"]:
                return False
        return True
