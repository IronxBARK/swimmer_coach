from django.shortcuts import render, redirect  # Added redirect
from django.urls import reverse  # Added reverse for URL resolution
from django.views.generic import TemplateView
from .forms import FileNameForm, SwimmerChoiceForm
from hfpython import swimclub

# Create your views here.

class HomePage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FileNameForm()  # Ensure the form is added to the context
        return context

    def post(self, request, *args, **kwargs):
        form = FileNameForm(request.POST)
        if form.is_valid():
            swimmer_name = form.cleaned_data['swimmer_name']
            # Redirect to DataPage with swimmer_name as a query parameter
            return redirect(reverse('data_page') + f'?swimmer_name={swimmer_name}')
        return self.render_to_response(self.get_context_data(form=form))

    
            
class DataPage(TemplateView):
    template_name = 'data.html'  # Ensure you have a template for DataPage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        swimmer_name = self.request.GET.get('swimmer_name')  # Retrieve swimmer_name from query parameters
        context['swimmer_name'] = swimmer_name  # Pass swimmer_name to the template

        # Dynamically populate choices for SwimmerChoiceForm
        swimmer_data = swimclub.get_data().get(swimmer_name, [])
        age = swimmer_data[0]
        form = SwimmerChoiceForm()
        form.fields['choice'].choices = [('', '--- Select ---')] + [(data, data) for data in swimmer_data[1:]]  # Add default choice
        context['form'] = form  # Add the form to the context
        context['age'] = age  # Add age to the context
        return context
    
    def post(self, request, *args, **kwargs):
        swimmer_name = request.POST.get('swimmer_name')  # Retrieve swimmer_name from POST data
        age = request.POST.get('age')  # Retrieve age from POST data

        # Dynamically populate choices for SwimmerChoiceForm
        swimmer_data = swimclub.get_data().get(swimmer_name, [])  # Retrieve swimmer-specific data
        form = SwimmerChoiceForm(request.POST)
        form.fields['choice'].choices = [('', '--- Select ---')] + [(data, data) for data in swimmer_data]  # Set choices dynamically

        if form.is_valid():
            choice = form.cleaned_data['choice']  # Retrieve the selected choice

            # Make file
            filename = f"{swimmer_name}-{age}-{choice}.txt"
            save_to = swimclub.make_charts(filename)
            print(save_to)
            # Open the file in a new tab
            self.open_file(save_to)
        

        return self.render_to_response(self.get_context_data(form=form))

    
    def open_file(self, file_path):
        '''Opens the corresponding file '''
        from webbrowser import open_new_tab
        import os
        # Check if the file exists
        if os.path.exists(file_path):
            # Open the file in a new tab
            open_new_tab(file_path)
        else:
            print(f"File {file_path} does not exist.")