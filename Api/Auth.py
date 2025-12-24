from sqlite3 import IntegrityError
from Models.UserModel import UserRole
from Repositories.UserRepository import UserRepository
from Services.AuthService import AuthService
from Utilities.exceptions import IncorrectPasswordError, InvalidInputError, StoreError, UserNotFoundError

class Auth:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def add_user(self, username, password, role):
        try:
            user_id = self.auth_service.register(username, password, role)
            return {"success": True, "data": {"user_id": user_id}, "message": "User added !"}
        except InvalidInputError as e:
            return {"success": False, "error_type": "validation", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}

    def change_role(self, username, role):
        try:
            user = self.auth_service.change_role(username, UserRole(role))
            return {"success": True, "data": {"id": user["id"], "username": user["username"], "role": user["role"]}, "message": "User Role Changed !"}
        except InvalidInputError as e:
            return {"success": False, "error_type": "validation", "message": str(e)}
        except UserNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}

    def change_password(self, username, current_password, new_password):
        try:
            self.auth_service.update_password(username, current_password, new_password)
            return {"success": True, "data": {"password_changed": True}, "message": "password Changed !"}
        except InvalidInputError as e:
            return {"success": False, "error_type": "validation", "message": str(e)}
        except UserNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}


    def delete_user(self, username):
        try:
            user_id = self.auth_service.delete_user(username)
            return {"success": True, "data": {"user_id": user_id}, "message": "User Deleted"}
        except InvalidInputError as e:
            return {"success": False, "error_type": "validation", "message": str(e)}
        except UserNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}
    
    def login(self, username, password):
        try:
            user = self.auth_service.login(username, password)
            return {"success": True, "data": {"id": user["id"], "username": user["username"], "role": user["role"]}, "message": "Logged in !"}
        except InvalidInputError as e:
            return {"success": False, "error_type": "validation", "message": str(e)}
        except IncorrectPasswordError as e:
            return {"success": False, "error_type": "missmatch", "message": str(e)}
        except UserNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}

    def logout(self):
        try:
            self.auth_service.logout()
            return {"success": True, "data": {}, "message": "Logged out !"}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}

    def list_users(self):
        try:
            users = self.auth_service.list_users()
            return {"success": True, "data": {'users': users}, "message": "Users fetched !"}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}
