from blog.models import Record
from django.views.generic import CreateView, DetailView, ListView, DeleteView, TemplateView, UpdateView
from django.urls import reverse_lazy


class HomeView(ListView):
    model = Record
    template_name = 'blog/home.html'


class CreateRecord(CreateView):
    model = Record
    fields = [
        'name',
        'description',
        'image',
        'is_published',
    ]
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:blog_list')


class RecordListView(ListView):
    model = Record
    template_name = 'blog/record_list.html'

    def get_queryset(self):
        return Record.objects.filter(is_published=True)


class RecordDetailView(DetailView):
    model = Record
    template_name = 'blog/record_detail.html'
    context_object_name = 'record'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.number_of_views += 1
        obj.save(update_fields=['number_of_views'])
        return obj


class RecordUpdateView(UpdateView):
    model = Record
    fields = [
        'name',
        'description',
        'image',
        'is_published'
    ]
    template_name = 'blog/create.html'
    # def get_success_url(self):
    #     return reverse_lazy('blog:record_detail', kwargs={'pk': self.object.pk})

    success_url = '{% url "blog:record_detail" pk=object.pk %}'


class RecordDeleteView(DeleteView):
    model = Record
    template_name = 'blog/record_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
