from django.urls import path
from . import api

urlpatterns = [
    path('analisys-domain', api.domain_analysis, name='domain-analisys'),
    path('callback/<int:pk>', api.Callback.as_view({'post': 'post'}), name="callback"),
    path('report/<int:pk>/<str:token>', api.report, name="report")
]