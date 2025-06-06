from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification_mail
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

class Vendor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='user')
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE,  related_name='userprofile')
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    @property
    def is_open(self):

        # check current date opening hours
        today_date = date.today()
        today = today_date.isoweekday()

        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now(ZoneInfo("Asia/Kolkata"))
        current_time = now.time()

        is_open = False
        for i in current_opening_hours:
            if not i.is_closed:
                start = datetime.strptime(i.from_hour, "%I:%M %p").time()
                end = datetime.strptime(i.to_hour, "%I:%M %p").time()
                
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False

        return is_open


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


DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]
HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]
class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()

