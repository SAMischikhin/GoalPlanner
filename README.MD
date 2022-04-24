goalplanner

python3.8, Django=4.0.1, Postgres

AUTH_USER_MODEL = core.User(AbstractUser)

Fields:

username, email, first_name, last_name, date_joined, is_staff, is_active 
from AbstractUser(AbstractBaseUser, PermissionsMixin)

password, last_login from AbstractBaseUser
    
is_superuser from PermissionsMixin

