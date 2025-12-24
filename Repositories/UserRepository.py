from Models.UserModel import UserModel

class UserRepository:

    def add(self, session, user):
        session.add(user)
    
    def get(self, session, user_id):
        return session.get(UserModel, user_id)

    def get_by_username(self, session, username):
        return session.query(UserModel).filter(UserModel.username == username.lower()).first()

    def list_all(self, session):
        return session.query(UserModel).all()

    def delete(self, session, user):
        session.delete(user)