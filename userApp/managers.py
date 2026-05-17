from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self, email, firstName, lastName, password=None, **extra_fields):
        if not email:
            raise ValueError("Email zorunludur! ")
        if not password:
            raise ValueError("Şifre zorunludur")
        if not firstName:
            raise ValueError("İsim zorunludur!")
        if not lastName:
            raise ValueError("Soyisim zorunludur!")
        

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            firstName=firstName,
            lastName=lastName,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, firstName, lastName, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, firstName, lastName, password, **extra_fields)