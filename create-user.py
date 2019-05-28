import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

# Create Airflow User
user = PasswordUser(models.User())
user.username = 'airflow'
user.email = 'jensen.yap@groundx.xyz'
user._set_password = 'airflow'
session = settings.Session()
session.add(user)
session.commit()
session.close()
print('New User Created')
