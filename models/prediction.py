from database import Database
from datetime import datetime
from bson import ObjectId

class Prediction:
    def __init__(self, user_id, prediction_type, input_data, predicted_value, metadata=None, created_at=None, _id=None):
        self.user_id = user_id
        self.prediction_type = prediction_type  # 'house', 'diabetes', etc.
        self.input_data = input_data
        self.predicted_value = predicted_value
        self.metadata = metadata or {}  # Additional data like confidence, probabilities
        self.created_at = created_at or datetime.utcnow()
        self._id = _id
    
    @staticmethod
    def create_prediction(user_id, prediction_type, input_data, predicted_value, metadata=None):
        """Create a new prediction record"""
        prediction = Prediction(
            user_id=user_id,
            prediction_type=prediction_type,
            input_data=input_data,
            predicted_value=predicted_value,
            metadata=metadata or {}
        )
        
        db = Database.get_db()
        result = db.predictions.insert_one({
            'user_id': user_id,
            'prediction_type': prediction_type,
            'input_data': input_data,
            'predicted_value': predicted_value,
            'metadata': prediction.metadata,
            'created_at': prediction.created_at
        })
        prediction._id = result.inserted_id
        return prediction
    
    @staticmethod
    def get_user_predictions(user_id, limit=None, skip=0):
        """Get all predictions for a user"""
        db = Database.get_db()
        query = {'user_id': user_id}
        
        cursor = db.predictions.find(query).sort('created_at', -1)
        
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        
        predictions = []
        for pred_data in cursor:
            predictions.append(Prediction(
                user_id=pred_data['user_id'],
                prediction_type=pred_data['prediction_type'],
                input_data=pred_data['input_data'],
                predicted_value=pred_data['predicted_value'],
                metadata=pred_data.get('metadata', {}),
                created_at=pred_data.get('created_at'),
                _id=pred_data['_id']
            ))
        
        return predictions
    
    @staticmethod
    def get_user_prediction_count(user_id):
        """Get total count of predictions for a user"""
        db = Database.get_db()
        return db.predictions.count_documents({'user_id': user_id})
    
    @staticmethod
    def delete_user_predictions(user_id):
        """Delete all predictions for a user"""
        db = Database.get_db()
        return db.predictions.delete_many({'user_id': user_id})
    
    def to_dict(self):
        """Convert prediction to dictionary"""
        # Ensure proper ISO format with timezone
        created_at_str = None
        if self.created_at:
            # Add 'Z' suffix to indicate UTC time
            created_at_str = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        return {
            'id': str(self._id),
            'user_id': self.user_id,
            'prediction_type': self.prediction_type,
            'input_data': self.input_data,
            'predicted_value': self.predicted_value,
            'metadata': self.metadata,
            'created_at': created_at_str
        }
