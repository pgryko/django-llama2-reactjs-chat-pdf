from django.urls import path
from chat.views import chat as chat_views, room_list as room_list_views

urlpatterns = [
    path("room/<uuid:room_uuid>/", chat_views.chat_page, name="chat_room"),
    path("rooms/", room_list_views.chatroom_list, name="chatroom_list"),
    path(
        "room/delete/<uuid:chatroom_uuid>/",
        room_list_views.chatroom_delete,
        name="chatroom_delete",
    ),
    path("room/create/", room_list_views.chatroom_create, name="chatroom_create"),
    path("files/<uuid:chatroom_uuid>/", room_list_views.files_list, name="files_list"),
    path(
        "file/delete/<uuid:chatroom_uuid>/<uuid:file_uuid>",
        room_list_views.file_delete,
        name="file_delete",
    ),
    path(
        "files/upload/<uuid:chatroom_uuid>/",
        room_list_views.upload_file,
        name="upload_file",
    ),
    path(
        "<uuid:room_uuid>/file/<uuid:file_uuid>/",
        chat_views.file_view,
        name="file_view",
    ),
    path("file/<uuid:file_uuid>/", chat_views.serve_file, name="serve_file"),
]
