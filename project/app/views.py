from django.http import *
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import *
from django.views.generic.detail import SingleObjectTemplateResponseMixin, SingleObjectMixin
from django.conf import settings
import os

from .models import *
from .form import *

def index(request):
    s="Список объявлений\n\n\n\n\n"
    for b in Bb.objects.all():
        s += b.title + "\n"+ b.content+"\n\n\n"
    return HttpResponse(s,content_type="text/plain; charset=utf-8")


def index_html(request):
    bbs=Bb.objects.all()
    rubrics=Rubric.objects.all()
    context={"bbs":bbs,"rubrics":rubrics}
    return render(request,'index.html',context)

def index2(request):
    return HttpResponse("Python Django")

def detail(request,pk):
    rubric=Rubric.objects.get(pk=pk)
    all_bb=Bb.objects.filter(rubric=rubric)
    context={"rubric":rubric,"all_bb":all_bb}
    return render(request,'detail.html',context)

def detail_bb(request,pk):
    bb=Bb.objects.get(pk=pk)
    context={"bb":bb}
    return render(request,'detail_bb.html',context)


def add_bb(request):
    if request.method=="POST":
        bbform=BbForm(request.POST)
        if bbform.is_valid():
            bbform.save()
            return HttpResponseRedirect(
                reverse
                ("app:detail",
                 kwargs={"pk":bbform.cleaned_data["rubric"].pk}
                 ))
        else:
            context={"form":bbform}
            return render(request,'add_bb.html',context)
    else:
        bbform=BbForm()
        context={"form":bbform}
        return render(request,'add_bb.html',context)

def stream(request):
    resp_content=('Здесь ','будет ','отправляться ','текст')
    return StreamingHttpResponse(
        resp_content,
        content_type="text/plain; charset=utf-8")

@require_GET
def file_response(request):
    file_path=r"C:\Users\winge\PycharmProjects\djangoProject1\project\static\picture.jpg"
    return FileResponse(open(file_path, 'rb'), content_type='image/jpg',as_attachment=True)

def our_decorator(func):
    def wrapper(request):
        print("hello")
        return func(request)
    return wrapper

@our_decorator
@require_http_methods(['POST'])
def json_response(request):
    bb=Bb.objects.get(title="Машина")
    dictionary={
        "title":bb.title,
        "content":bb.content,
        "price":bb.price,
        "published":bb.published,
    }
    return JsonResponse(dictionary)


def update_bb(request,pk):
    bb=Bb.objects.get(pk=pk)
    if request.method=="POST":
        form=BbForm(request.POST,instance=bb)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse
                ("app:detail",
                 kwargs={"pk": form.cleaned_data["rubric"].pk}
                 ))
        else:
            context = {"form": form}
            return render(request, 'add_bb.html', context)
    else:
        form = BbForm(instance=bb)
        context = {"form": form}
        return render(request, 'add_bb.html', context)

def delete_bb(request,pk):
    bb=get_object_or_404(Bb,pk=pk)
    if request.method=="POST":
        bb.delete()
        return redirect(reverse("app:index_html"))
    return Http404()



from django.views.generic import *
from django.views.generic.base import *

class BbCreateView(CreateView):
    model = Bb
    fields = ['rubric','title','content','price']
    template_name = "add_bb.html"

class BbByRubricTemplateView(TemplateView):
    template_name = "by_rubric_class.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['bbs']=Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics']=Rubric.objects.all()
        context['current_rubric']=Rubric.objects.get(pk=context['rubric_id'])
        return context

from django.views import View
class RubricDetailView(View):
    def get(self, request, rubric_id):
        current_rubric=get_object_or_404(Rubric,pk=rubric_id)
        bbs=Bb.objects.filter(rubric=current_rubric)
        rubrics=Rubric.objects.all()
        context={
            "current_rubric":current_rubric,
            "bbs":bbs,
            "rubrics":rubrics,
        }
        return render(request,'by_rubric_class.html',context)

class BbDetailView(DetailView):
    model = Bb
    template_name = "detail_bb.html"
    # pk_url_kwarg = "bb_id"


class BbListView(ListView):
    model = Bb
    template_name = "index.html"
    context_object_name = "bbs"
    # allow_empty = False

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['rubrics']=Rubric.objects.all()
        data = ["Test1", "Test2", "Test3"]
        context["data"]= data
        return context


class BbUpdateView(UpdateView):
    # form_class = BbForm
    model = Bb
    fields = ['rubric','title','content','price']
    success_url = "app/all/class/"
    template_name = "add_bb.html"


class BbDeleteView(DeleteView):
    model = Bb
    success_url = reverse_lazy("app:all_class")
    template_name = "delete_bb.html"
    context_object_name = "bb"


class BbIndexArchiveView(ArchiveIndexView):
    model = Bb
    date_field = "published"
    template_name = "date.html"
    context_object_name = "latest"

class BbYearArchiveView(YearArchiveView):
    model = Bb
    template_name = "date.html"
    context_object_name = "latest"
    date_field = "published"
    make_object_list = True

class BbMonthArchiveView(MonthArchiveView):
    model = Bb
    date_field = "published"
    template_name = "date.html"
    context_object_name = "latest"
    make_object_list = True
    month_format = "%m"

class BbWeekArchiveView(WeekArchiveView):
    model = Bb
    date_field = "published"
    template_name = "date.html"
    context_object_name = "latest"
    make_object_list = True
    weekday_format = "%W"

class BbDayArchiveView(DayArchiveView):
    model = Bb
    date_field = "published"
    template_name = "date.html"
    context_object_name = "latest"
    make_object_list = True
    month_format = "%m"

class BbTodayArchiveView(TodayArchiveView):
    model = Bb
    date_field = "published"
    template_name = "date.html"
    context_object_name = "latest"
    make_object_list = True

class BbRedirectView(RedirectView):
    url = reverse_lazy("app:all_class")
    permanent = True


class MergeBbRubricView(SingleObjectMixin, ListView):
    template_name = "by_rubric_class.html"
    pk_url_kwarg = "rubric_id"

    def get(self, request,*args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['rubrics']=Rubric.objects.all()
        context['current_rubric']=self.object
        context['bbs']=context['object_list']
        return context

    def get_queryset(self):
        return self.object.bb_set.all()


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = "contact.html"
    success_url = reverse_lazy("app:all_class")

    def form_valid(self, form):
        print("Полученный данные",form.cleaned_data)
        return super().form_valid(form)


class TemplateAllBboard(ListView):
    model = Bb
    template_name = "all_bboard.html"
    context_object_name = "bbs"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['email']="test@gmail.com"
        context['phone']=""
        context['html_code']="<i>Hello</i>"
        return context

class TestView(TemplateView):
    template_name = "test.html"


from django.core.paginator import Paginator

def  bb_paginator(request):
    bbs = Bb.object.all().order_by('-published')
    per_page = request.GET.eget('per_page', 3)
    paginator = Paginator(bbs.per_page, orphans=2)
    page_number = request.GET.het('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj' : page_obj,
        'paginator' : paginator,

    }
    return render(request, 'bb_paginator.html', context)


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)


class Quiz(models.Model):
    title = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return (self.text)

class QuizFormsetView(View):
    template_name = "quiz_formset.html"

    def get(self,request,pk):
        quiz=get_object_or_404(Quiz,pk=pk)
        formset=QuestionFormSet(instance=quiz)
        context={"formset":formset,"quiz":quiz}
        return render(request,self.template_name,context)

    def post(self,request,pk):
        quiz=get_object_or_404(Quiz,pk=pk)
        formset=QuestionFormSet(request.POST,instance=quiz)

        if formset.is_valid():
            formset.save()
            return redirect(reverse("app:quiz_formset", args=(quiz.pk,)))

        context={"formset":formset,"quiz":quiz}
        return render(request,self.template_name,context)

#dz-17
class Book(models.Model):
    def book_detail_json(request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            data = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'year': book.year
            }
            return JsonResponse(data)
        except Book.DoesNotExist:
            raise Http404("Книга не найдена")


class Example(models.Model):
    def download_example_txt(request):
        file_path = os.path.join(settings.BASE_DIR, 'example.txt')
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'),as_attachement=True, filename='example.txt')
        else:
            raise Http404("File does not exists")

#dz-26

def create_bb(request):
    BbForm = modelform_factory(Bb, fields=['title', 'author', 'rubric', 'price', 'content', 'published'])
    if request.method == 'POST':
        form = BbForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_bb')
    else:
        form = BbForm()

    return render(request, 'bb_form.html', {'form': form})
