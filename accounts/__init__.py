from django.contrib.auth.models import User

# monkey patching to make emails unique for users
User._meta.get_field_by_name('email')[0]._unique = True