from audioop import reverse
from django.shortcuts import render, get_object_or_404, reverse, redirect
from antarmuka.models import Antarmuka
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.views import View
from django.core.paginator import Paginator
from .forms import AntarmukaForm
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactForm
# Create your views here.

def index(request):
    antarmukas = Antarmuka.objects.all().order_by('-id')
    paginator = Paginator(Antarmuka, 2)
    page = request.GET.get('page')
    antarmukas = paginator.get_page(page)
    context = {
        'antarmukas': antarmukas
    }

    return render(request, 'antarmuka/index.html', context)


class SearchAntarmuka(View):
    def get(self, request):
        query = self.request.GET.get('q')

        query_list = Antarmuka.objects.filter(
            Q(judul__icontains=query) |
            Q(konten__icontains=query)
        )

        context = {
            'query_list': query_list,
        }

        return render(request, 'antarmuka/search.html', context )

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class DetailAntarmuka(generic.DetailView):
    model = Antarmuka
    template_name = 'antarmuka/detail.html'

# Membuat postingan
class AddPost(LoginRequiredMixin,generic.CreateView):
    model = Antarmuka
    fields = ['judul', 'penulis', 'date', 'image', 'konten']
    template_name = 'antarmuka/addpost.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk':self.object.pk})


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Antarmuka
    form_class = AntarmukaForm
    template_name = 'antarmuka/addpost.html'

    def form_valid(self, form):
        post = self.get_object()

        if self.request.user != post.penulis:
            messages.error(self.request, 'Anda tidak berhak melakukan update!')
            return redirect('/')

        messages.success(self.request, "Post berhasil diupdate!")
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = Antarmuka
    template_name = 'antarmuka/deletepost.html'
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        post = self.get_object()

        if self.request.user != post.penulis:
            messages.error(self.request, 'Anda tidak berhak menghapus posting ini!')
            return redirect('/')

        messages.success(self.request, "Postingan berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


# Contact us function
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                'Contact Form Message',  # subject
                f'From: {full_name}, <{email}>\n\nMessage:\n{message}',  # message
                email,  # from email
                ['naylayuda436@gmail.com'],  # to email
            )
            return render(request, 'success.html')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})