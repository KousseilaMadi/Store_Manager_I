from datetime import datetime
from Models.UserModel import UserRole, UserModel
from passlib.hash import bcrypt
from Utilities.exceptions import InvalidInputError, UserNotFoundError, IncorrectPasswordError, RequireAdminAccessError, InvalidUsernameError, InvalidPasswordError
from Utilities.Database import session_scope
import re

def hash_password(password):
    return bcrypt.hash(password)

def verify_password(password, password_hash):
    return bcrypt.verify(password, password_hash)


USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,20}$")
class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        self.current_user = None
    

    def register(self, username, password, role:UserRole):
        if not username:
            raise InvalidInputError("Username cannot be empty.")
        username_lower = username.lower()
        if USERNAME_PATTERN.match(username_lower) is None:
            raise InvalidInputError("Username contains unacceptable characters or too short.")
        
        if not password or len(password) < 5:
            raise InvalidInputError("Password is too short minimum 5.")

        
        password_hash = hash_password(password)
        new_user = UserModel(username=username_lower,
                         password_hash=password_hash,
                         role=role,
                         created_at=datetime.now())
        with session_scope() as session:
            user = self.user_repo.get_by_username(session, username_lower)
            if user:
                raise InvalidInputError("Username already exists.")
            self.user_repo.add(session, new_user)
            session.flush()
            user_id = new_user.id
        return user_id
    
    def login(self, username, password):
        if not username:
            raise InvalidUsernameError("Username must be provided.")
        if not password:
            raise InvalidPasswordError("Password must be provided.")

        username_lower = username.lower()
        with session_scope() as session:
            user = self.user_repo.get_by_username(session, username_lower)
            if user is None:
                raise UserNotFoundError(username_lower)
            if verify_password(password=password, password_hash=user.password_hash):
                self.current_user = {"id": user.id,
                                     "username": user.username,
                                     "role": user.role.value}
            else:
                raise IncorrectPasswordError("Password is incorrect.")
        return self.current_user
    
    def logout(self):
        self.current_user = None
    
    def is_admin(self):
        return self.current_user is not None and self.current_user["role"] == UserRole.ADMIN.value

    def require_admin(self):
        if not self.is_admin():
            raise RequireAdminAccessError()
        
    def change_role(self, username, role:UserRole):
        self.require_admin()
        if not username:
            raise InvalidInputError("Username cannot be empty.")
        if not role:
            raise InvalidInputError("Role cannot be empty.")
        username_lower = username.lower()
        with session_scope() as session:
            user = self.user_repo.get_by_username(session, username_lower)
            if user is None:
                raise UserNotFoundError(username_lower)
            user.role = role
            session.add(user)
            user_obj = {
                "id":user.id,
                "username":user.username,
                "role":user.role.value
            }
            print(user.role)
        return user_obj
    
    def update_password(self, username, current_password, new_password):
        if not username:
            raise InvalidInputError("username cannot be empty.")
        if not new_password or not current_password:
            raise InvalidInputError("password cannot be empty.")

        username_lower = username.lower()
        with session_scope() as session:
            user = self.user_repo.get_by_username(session, username_lower)
            if not user:
                raise UserNotFoundError(username_lower)
                
        
            if not verify_password(password=current_password, password_hash=user.password_hash):
                raise InvalidInputError("Current password incorrect.")
            
            new_hash = hash_password(new_password)
            user.password_hash = new_hash
            session.add(user)
        return True

    def delete_user(self, username):
        if not username:
            raise InvalidInputError("Username cannot be empty.")
        username_lower = username.lower()
        with session_scope() as session:
            user = self.user_repo.get_by_username(session, username_lower)
            if user is None:
                raise UserNotFoundError(username_lower)
            self.user_repo.delete(session, user)
            user_id = user.id
        return user_id

    def get_current_user(self):
        return self.current_user

    def list_users(self):
        self.require_admin()
        with session_scope() as session:
            users_list = self.user_repo.list_all(session)
            users = [{'id':user.id,
                      'username':user.username,
                      'role':user.role.value,
                      'created_at':user.created_at.isoformat()} for user in users_list]
            
        return users
    
    def count_users(self):
        with session_scope() as session:
            users_list = self.user_repo.list_all(session)
            user_count = len(users_list)
        return user_count
    
