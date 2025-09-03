from django.contrib.auth.models import User


class EmailAuthBackend: 
    """
    аутентифицировать посредством адреса электронной почты. 
    """
    def authenticate(self, request, username=None, password=None): 
        """
        извлекается юзер с эл.почтой, а пароль проверяется методом check_password() модели User
        """
        try: 
            user = User.objects.get(email=username)
            if user.check_password(password): 
                # xeshiruet password i sravnivaet s parolem kotorii xronitsa v db
                return user 
            return None 
        except (User.DoesNotExist, User.MultipleObjctsReturned): 
            #oshibka DoesNotExist voznikaet kogda user s takim email ne naiden
            #oshibka MultipleObjctsReturned voznikaet esli naideno neskolko polzivatelei s odnoi pochtoi
            return None 

    def get_user(self, user_id): 
        #User izvlekaitsa po id 
        #pk-sokrashenie ot primary key(ynikalnii indentifikator kashdoi ychetnoi zapisi v db). По умолчанию primary key генерируется полем id 
        try: 
            return User.objects.get(pk=user_id)
        except User.DoesNotExist: 
            return None 
