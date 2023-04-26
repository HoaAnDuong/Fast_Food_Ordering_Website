from foodapp.settings import MEDIA_ROOT
import os
import datetime


def avatar_change(subfolders,instance,file):
    if file.size > 5e+7: raise ImportError("Kích thước hình ảnh quá lớn")
    dir = ""
    file_name = file.__str__().split(".")
    file_name[0] += " " + datetime.datetime.now().__str__().split(".")[0].replace(":","-")
    file_name = file_name[0]+"."+file_name[1]
    print(file_name)
    f"{dir}{file_name}"
    if type(subfolders) in [tuple,list]:
        with open(os.path.join(MEDIA_ROOT, *subfolders, file_name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        for i in subfolders:
            dir += f"{i}/"
    else:
        with open(os.path.join(MEDIA_ROOT, subfolders, file_name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        dir = f"{subfolders}/"
    os.remove(os.path.join(MEDIA_ROOT, instance.avatar.__str__().replace("/","//")))
    instance.avatar = f"{dir}/{file_name}"
    instance.save()

def image_upload(subfolders,instance,file):
    if file.size > 5e+7: raise ImportError("Kích thước hình ảnh quá lớn")
    dir = ""
    file_name = file.__str__().split(".")
    file_name[0] += " " + datetime.datetime.now().__str__().split(".")[0].replace(":","-")
    file_name = file_name[0]+"."+file_name[1]
    print(file_name)
    f"{dir}{file_name}"
    if type(subfolders) in [tuple,list]:
        with open(os.path.join(MEDIA_ROOT, *subfolders, file_name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        for i in subfolders:
            dir += f"{i}/"
    else:
        with open(os.path.join(MEDIA_ROOT, subfolders, file_name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        dir = f"{subfolders}/"
    os.remove(os.path.join(MEDIA_ROOT, instance.image.__str__().replace("/","//")))
    instance.image = f"{dir}/{file_name}"
    instance.save()