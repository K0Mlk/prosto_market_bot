from src.bot.bot import SupportBot
from src.database.models import UserModel

def main():
    
    UserModel().create_tables()
    
    bot = SupportBot()
    bot.run()

if __name__ == '__main__':
    main()