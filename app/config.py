from os import getenv

from dotenv import load_dotenv

load_dotenv()

AWS_SNS_REPORTAR_RECETA = getenv("AWS_SNS_REPORTAR_RECETA")
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = getenv("AWS_REGION")

POSTGRES_URI = getenv("POSTGRES_URI")
