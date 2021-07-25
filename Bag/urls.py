from App import views
from django.urls import path

urlpatterns = [
    path('',views.index),
    path('signup/',views.signup),
    path('login/',views.login_view),
    path('add_item/',views.add_item),
    path('show_items/',views.show_items),
    path('update_item/<item_id>',views.update_item),
    path('delete_item/<item_id>',views.delete_item),
    path('logout/', views.logout_view),
]
