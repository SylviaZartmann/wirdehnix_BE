from django.contrib import admin
#from import_export.admin import ImportExportModelAdmin

from filmography.models import Filmography

# class FilmoAdmin(ImportExportModelAdmin):
#     list_display = (
#         "title",
#         "description",
#         "upload_date",
#     )

#     fields = (
#         "title",
#         "description",
#         "video_file",
#         "video_file_480p",
#         "video_file_720p",
#         "video_file_1080p",
#         "thumbnail",
#         "upload_date"
#     )

admin.site.register(Filmography) #, FilmoAdmin