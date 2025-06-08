from flask import Blueprint, request, jsonify
from . import db
from .models import Submission
from jsonschema import validate, ValidationError
import logging

api = Blueprint('api', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JSON schema for /submit endpoint
submit_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 255},
        "score": {"type": "integer", "minimum": 0, "maximum": 100}
    },
    "required": ["name", "score"],
    "additionalProperties": False
}

@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"}), 200

@api.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
            
        # Validate input
        validate(instance=data, schema=submit_schema)
        
        # Create new submission
        submission = Submission(
            name=data['name'],
            score=data['score']
        )
        
        db.session.add(submission)
        db.session.commit()
        
        logger.info(f"New submission added: name={data['name']}, score={data['score']}")
        return jsonify({"message": "Submission recorded", "id": submission.id}), 201
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@api.route('/results', methods=['GET'])
def results():
    try:
        submissions = Submission.query.all()
        return jsonify([submission.to_dict() for submission in submissions]), 200
    except Exception as e:
        logger.error(f"Error fetching results: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
