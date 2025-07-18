from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfessorListView.as_view(), name='professor_list'),
    path('professor/<int:pk>/', views.ProfessorDetailView.as_view(), name='professor_detail'),
    path('professor/create/', views.ProfessorCreateView.as_view(), name='professor_create'),
    path('professor/<int:pk>/edit/', views.ProfessorUpdateView.as_view(), name='professor_edit'),
    path('professor/<int:pk>/delete/', views.ProfessorDeleteView.as_view(), name='professor_delete'),
    path('csv/import/', views.CSVImportView.as_view(), name='csv_import'),
    path('csv/export/', views.CSVExportView.as_view(), name='csv_export'),
]
