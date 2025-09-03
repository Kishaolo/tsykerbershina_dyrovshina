from django.db import models
from django.conf import settings
# Create your models here.


class Profile(models.Model): 
    """
    Профиль содержит дату рождения и фотографию пользывателя
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE) # pole user bydet asotsiirovatsa v profilem usera # on_delete=models.CASCADE ispolzuetsa dla ydalenia objecta Profile pri udalenii objecta User
    date_of_birth = models.DateField(blank=True, 
                                     null=True) # данное поле опционально благодоря blank=True + разрешаем не заполнять его с помощью null=True
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', 
                              blank=True) # pole photo also optional decause blank=True class ImageField manages saveom. He examinate what file its image (valid) save file in catalog indicated in param upload_to and save otnos path in relate field in db 

    def __str__(self): 
        return f'Pforile of {self.user.username}'
