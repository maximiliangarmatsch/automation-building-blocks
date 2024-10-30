import os
from flask import Flask
from flask_cors import CORS
from asgiref.wsgi import WsgiToAsgi
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
asgi_app = WsgiToAsgi(app)
api_cors = {
    "origins": ["*"],
    "methods": ["OPTIONS", "GET", "POST"],
    "allow_headers": ["Content-Type"],
}

MEDIA_FOLDER = "uploads"
if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER)

api_key = os.getenv("GOOGLE_API_KEY")

from api_helpers.auth.auth_api import auth
from api_helpers.create_profile.create_profile_api import create_profile
from api_helpers.create_profile.extract_features_api import extract_features
from api_helpers.create_profile.attractiveness_score_api import attractiveness_score
from api_helpers.get_profile.get_profile_api import get_profile
from api_helpers.match_profile.match_profile_api import match_profile
from api_helpers.match_profile.get_match_profile_api import get_match_profile
from api_helpers.match_profile.get_specific_match_profile_api import (
    get_specific_match_profile,
)
from api_helpers.match_accept.accept_match_api import accept_match
from api_helpers.match_accept.get_match_accepted_api import get_accepted_match
from api_helpers.match_accept.get_specific_accepted_match_api import (
    get_specific_accepted_match,
)
from api_helpers.match_profile.reject_match_api import reject_match
from api_helpers.custom_questions.save_custom_question_api import save_custom_question
from api_helpers.custom_questions.save_custom_answer_api import save_custom_answer
from api_helpers.date_scheduling.schedule_date_api import schedule_date
from api_helpers.date_scheduling.get_schedule_date_api import get_schedule_date
from api_helpers.general_questions.update_general_question_api import (
    update_general_question,
)
from api_helpers.general_questions.delete_general_question_api import (
    delete_general_question,
)

app.register_blueprint(auth)
app.register_blueprint(create_profile)
app.register_blueprint(extract_features)
app.register_blueprint(attractiveness_score)
app.register_blueprint(match_profile)
app.register_blueprint(get_profile)
app.register_blueprint(get_match_profile)
app.register_blueprint(get_specific_match_profile)
app.register_blueprint(accept_match)
app.register_blueprint(get_accepted_match)
app.register_blueprint(get_specific_accepted_match)
app.register_blueprint(reject_match)
app.register_blueprint(save_custom_question)
app.register_blueprint(save_custom_answer)
app.register_blueprint(schedule_date)
app.register_blueprint(get_schedule_date)
app.register_blueprint(update_general_question)
app.register_blueprint(delete_general_question)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
