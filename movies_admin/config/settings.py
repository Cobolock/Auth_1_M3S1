from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    "components/application.py",
    "components/environment.py",
    "components/database.py",
    "components/security.py",
    "components/i18n.py",
    "components/logging.py",
    "components/corsheaders.py",
)
