from django.db import models


class NidInfo(models.Model):
    nid_number = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.nid_number


class PhoneList(models.Model):
    nid = models.ForeignKey(NidInfo, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=50)

    def __str__(self):
        return self.mobile_number


class VerifyMobile(models.Model):
    mobile = models.ForeignKey(PhoneList, on_delete=models.CASCADE)
    otp = models.IntegerField()

    def __str__(self):
        return self.mobile.mobile_number
