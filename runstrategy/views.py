from django.http import HttpResponse
from .models import Dataset



def new(request):
    from importdata.importdataset import df2

    for a in range(0,len(df2)):
        Dataset(Index=df2['Index'][a],Volume=df2['Volume'][a]).save()

    return HttpResponse('Upload_Data')