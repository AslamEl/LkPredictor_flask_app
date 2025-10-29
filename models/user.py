from werkzeug.security import generate_password_hash, check_password_hash
from database import Database
from datetime import datetime

class User:
    def __init__(self, email, name, password_hash, created_at=None, _id=None):
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.created_at = created_at or datetime.utcnow()
        self._id = _id
    
    @staticmethod
    def create_user(email, name, password):
        """Create a new user with hashed password"""
        password_hash = generate_password_hash(password)
        user = User(email=email, name=name, password_hash=password_hash)
        
        db = Database.get_db()
        result = db.users.insert_one({
            'email': user.email,
            'name': user.name,
            'password_hash': user.password_hash,
            'created_at': user.created_at
        })
        user._id = result.inserted_id
        return user
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        db = Database.get_db()
        user_data = db.users.find_one({'email': email})
        
        if user_data:
            return User(
                email=user_data['email'],
                name=user_data['name'],
                password_hash=user_data['password_hash'],
                created_at=user_data.get('created_at'),
                _id=user_data['_id']
            )
        return None
    
    @staticmethod
    def verify_password(email, password):
        """Verify user password"""
        user = User.find_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
    
    def update_name(self, new_name):
        """Update user's name"""
        db = Database.get_db()
        db.users.update_one(
            {'_id': self._id},
            {'$set': {'name': new_name}}
        )
        self.name = new_name
        return True
    
    @staticmethod
    def delete_user(user_id):
        """Delete user account"""
        db = Database.get_db()
        # Delete user
        result = db.users.delete_one({'_id': user_id})
        return result.deleted_count > 0
    
    def to_dict(self):
        """Convert user to dictionary (excluding password)"""
        return {
            'id': str(self._id),
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
