from django.db import models

# test
class Dataset(models.Model):

    Index = models.IntegerField(primary_key=True)
    Volume = models.IntegerField()

    def __str__(self):
        return self.name


# class Dataset2(models.Model):
#
#     Index = models.IntegerField(primary_key=True)
#     Date_Time = models.DateTimeField(auto_now=False, auto_now_add=False)
#     Last = models.DecimalField(decimal_places=5,max_digits=10)
#     Volume = models.IntegerField()
#     Delta = models.IntegerField()
#
#     def __str__(self):
#         return self.name



