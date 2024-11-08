from django.db import models

class ChanelGroup(models.Model):
    group_name = models.CharField(max_length=100,verbose_name='Channel Is\'mi')
    group_id = models.BigIntegerField(verbose_name='Channel id')
    group_url = models.CharField(max_length=200,verbose_name='Channel url')
    
    def __str__(self) -> str:
        return self.group_name
    
    class Meta:
        verbose_name = 'Channel and Group'
        verbose_name_plural ='Channels and Groups'

class BotToken(models.Model):
    user = models.CharField(max_length=50,unique=True)
    user_id = models.BigIntegerField(verbose_name='Sizning telegram id')
    user_name = models.CharField(max_length=100,verbose_name='I\'smingiz')
    user_url = models.CharField(max_length=100,verbose_name='telegram username')
    token = models.TextField(verbose_name='Bot Token')

    def __str__(self) -> str:
        return self.user
    
    class Meta:
        verbose_name = 'Setting Bot'
        verbose_name_plural ='Settings Bots'

class BotMessage(models.Model):
    command = models.CharField(max_length=50, unique=True)
    text = models.TextField(verbose_name='Malumotlar')
    photo = models.ImageField(upload_to='media/',null=True,blank=True)
    
    def __str__(self) -> str:
        return self.command
    
    class Meta:
        verbose_name = 'Message Bot'
        verbose_name_plural ='Messages Bots'

class BotButtonInline(models.Model):
    message = models.ForeignKey(BotMessage, on_delete=models.CASCADE, related_name='inline',verbose_name='Command')
    text = models.CharField(max_length=100,verbose_name='Knopkanin nomi')
    callback_data = models.CharField(max_length=100)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Inline Knopka'
        verbose_name_plural ='Iniles Knopkalar'

class BotButtonReply(models.Model):
    message = models.ForeignKey(BotMessage, on_delete=models.CASCADE, related_name='reply',verbose_name='Command')
    text = models.CharField(max_length=100,verbose_name='Knopkani nomi')

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Reply Knopka'
        verbose_name_plural ='Replys Knopkalar'

class CreateTest(models.Model):
    subject = models.CharField(max_length=50,null=True,blank=True,verbose_name='Fani nomi')
    test = models.CharField(max_length=100,verbose_name='Test javoblari')
    cod = models.BigIntegerField(unique=True,verbose_name='Test kodi')
    finish_date = models.DateTimeField()
    
    def __str__(self) -> str:
        return f"{self.subject}: {self.test}" if self.subject else self.test
    
    class Meta:
        verbose_name = 'Test'
        verbose_name_plural ='Testlar'

class UserCreate(models.Model):
    telegram_id = models.BigIntegerField(verbose_name='telegram id')
    first_name = models.CharField(max_length=50,verbose_name='I\'sm')
    last_name = models.CharField(max_length=50,verbose_name='Familiya')
    schools = models.CharField(max_length=100,verbose_name='Maktab hududi')
    school = models.CharField(max_length=100,verbose_name='Maktab nomeri')
    teacher_name = models.CharField(max_length=100,verbose_name='Uztozini i\'smi')
    teacher_last = models.CharField(max_length=100,verbose_name='Uztozini familiyasi')
    number = models.CharField(max_length=15,verbose_name='Nomeri')
    male = models.CharField(max_length=10,verbose_name='Pol')
    
    def __str__(self) -> str:
        return self.first_name
    
    class Meta:
        verbose_name = 'User loging'
        verbose_name_plural ='Users logins'

class UserResult(models.Model):
    user = models.ForeignKey(UserCreate,on_delete=models.CASCADE,verbose_name='I\'smi')
    test = models.ForeignKey(CreateTest,on_delete=models.CASCADE,verbose_name='Test')
    count_correct = models.IntegerField(verbose_name='Togri javob soni')
    count_wrong = models.IntegerField(verbose_name='Xato javob soni')
    percent = models.IntegerField(verbose_name='Sfati')
    correct_str = models.CharField(max_length=100,verbose_name='Togri javoblar')
    wrong_str = models.CharField(max_length=100,verbose_name='Xato javoblar')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.user}'
    
    class Meta:
        verbose_name = 'User result'
        verbose_name_plural ='Users results'
