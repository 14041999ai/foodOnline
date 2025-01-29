from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification_mail

class Vendor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='user')
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE,  related_name='userprofile')
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        # check if update
        if self.id is not None:
            orig = Vendor.objects.get(id=self.id)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                if self.is_approved == True:
                    #send success mail
                    mail_subject = 'Congratulations! Your restaurent has been approved.'
                    send_notification_mail(mail_subject, mail_template, context)
                else:
                    # send fail mail
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."
                    send_notification_mail(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)
