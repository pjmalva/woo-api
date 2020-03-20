from app.controller import WooMi

print('INIT WOOMI')

migrate = WooMi()
# migrate.makeConnection()
migrate.makeMigration()
