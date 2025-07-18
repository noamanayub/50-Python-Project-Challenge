from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
import csv
import io
import json
from .models import Professor
from .forms import ProfessorForm, CSVUploadForm

class ProfessorListView(ListView):
    model = Professor
    template_name = 'professors/professor_list.html'
    context_object_name = 'professors'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Professor.objects.all()
        search_query = self.request.GET.get('search')
        university_filter = self.request.GET.get('university')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(research_interests__icontains=search_query)
            )
        
        if university_filter:
            queryset = queryset.filter(university__icontains=university_filter)
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['csv_form'] = CSVUploadForm()
        context['search_query'] = self.request.GET.get('search', '')
        
        # Get all universities for dropdown
        context['universities'] = Professor.objects.values_list('university', flat=True).distinct().order_by('university')
        
        # Statistics
        total_professors = Professor.objects.count()
        avg_h_index = Professor.objects.aggregate(avg_h=Avg('h_index'))['avg_h'] or 0
        total_universities = Professor.objects.values('university').distinct().count()
        
        # Count unique research fields
        all_interests = Professor.objects.values_list('research_interests', flat=True)
        unique_fields = set()
        for interests in all_interests:
            fields = [field.strip() for field in interests.split(',')]
            unique_fields.update(fields)
        
        context['statistics'] = {
            'total_professors': total_professors,
            'avg_h_index': round(avg_h_index, 1),
            'total_universities': total_universities,
            'total_fields': len(unique_fields)
        }
        
        return context

class ProfessorDetailView(DetailView):
    model = Professor
    template_name = 'professors/professor_detail.html'
    context_object_name = 'professor'

class ProfessorCreateView(CreateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'professors/professor_form.html'
    success_url = reverse_lazy('professor_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Professor created successfully!')
        return super().form_valid(form)

class ProfessorUpdateView(UpdateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'professors/professor_form.html'
    success_url = reverse_lazy('professor_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Professor updated successfully!')
        return super().form_valid(form)

class ProfessorDeleteView(DeleteView):
    model = Professor
    template_name = 'professors/professor_confirm_delete.html'
    success_url = reverse_lazy('professor_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Professor deleted successfully!')
        return super().delete(request, *args, **kwargs)

class CSVImportView(View):
    def post(self, request):
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a valid CSV file.')
                return redirect('professor_list')
            
            try:
                # Read CSV file
                file_data = csv_file.read().decode('utf-8')
                csv_data = csv.DictReader(io.StringIO(file_data))
                
                created_count = 0
                for row in csv_data:
                    try:
                        Professor.objects.create(
                            name=row.get('name', ''),
                            university=row.get('university', ''),
                            research_interests=row.get('research_interests', ''),
                            email=row.get('email', ''),
                            h_index=int(row.get('h_index', 0)),
                            famous_articles=row.get('famous_articles', ''),
                            google_scholar_url=row.get('google_scholar_url', ''),
                            researchgate_url=row.get('researchgate_url', ''),
                        )
                        created_count += 1
                    except (ValueError, TypeError) as e:
                        messages.warning(request, f'Error importing row: {row.get("name", "Unknown")} - {str(e)}')
                        continue
                
                messages.success(request, f'Successfully imported {created_count} professors from CSV.')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
        
        return redirect('professor_list')

class CSVExportView(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="professors.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['name', 'university', 'research_interests', 'email', 'h_index', 
                        'famous_articles', 'google_scholar_url', 'researchgate_url'])
        
        professors = Professor.objects.all()
        for professor in professors:
            writer.writerow([
                professor.name,
                professor.university,
                professor.research_interests,
                professor.email,
                professor.h_index,
                professor.famous_articles,
                professor.google_scholar_url,
                professor.researchgate_url,
            ])
        
        return response
