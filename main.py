from dotenv import load_dotenv
import os


load_dotenv()

print(os.getenv("OPENAI_API_KEY"))
print(os.getenv("DISCORD_TOKEN"))
print(os.getenv("DATABASE_URL"))