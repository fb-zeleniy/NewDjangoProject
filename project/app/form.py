from django.forms import *
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View

from .models import *


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ['rubric','title','content','price']

class ContactForm(forms.Form):
    name=CharField(label="Имя",max_length=100)
    email=EmailField(label="Email")
    text=CharField(label="Сообщение",max_length=500,widget=Textarea)

class RubricForm(ModelForm):
    class Meta:
        model = Rubric
        fields = ['name']
        labels = {
            'name' : "Название рубрики"
        }
        help_texts = {
            'name' : 'Введите название рубрики'
        }
        widgets = {
            'name' : TextInput(attrs={'placeholder' : 'Название рубрики'})
        }

RubricFormSet = modelformset_factory(
    Rubric,
    form=RubricForm,
    can_delete=True,
    extra=2
)

class RubricSetView(View):
    template_name = 'rubric_formset.html'
    def get(self, request):
        formset=RubricFormSet(queryset=Rubric.objects.all())
        context = {"formset" : formset}
        return render(request, self.template_name, context)


    def post(self, request):
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse("app:all_class"))
        else:
            context = {"formset":formset}
            return render(request, self.template_name, context)

class RubricBaseFormSet(BaseFormSet):
    def clean(self):
        self().clean()
        names=[form.cleaned_data('name') for form in self.forms if 'name' in form.cleaned_data]
        if('Недвижимость' not in names) or ("Авто" not in names):
            raise ValidationError("Добавьте рубрики 'Недвижимость' или 'Авто' в список рубрик ")

            RubricFormSet = modelformset_factory(
                Rubric,
                fields=('name'),
                can_delete=True,
                formset=RubricBaseFormSet
            )
            context = {"formset":formset}
            return render(request, self.template_name, context)

        def post(self, request):
            formset = RubricFormSet(request.POST)
            if formset.is_valid():
                formset.save()


class QuestionInLine(BaseInlineFormSet):
    MIN_QUESTIONS = 2
    MAX_QUESTIONS = 10

    def clean(self):
        super().clean()

        alive=len(self.forms) - len(self.deleted_forms)
        if alive < self.MIN_QUESTIONS:
            raise ValidationError(f"Минимальное колличество воппросов: {self.MIN_QUESTIONS}")

        if alive > self.MAX_QUESTIONS:
            raise ValidationError(f"Максимальное колличество воппросов: {self.MAX_QUESTIONS}")

QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    fields=("text"),
    formset=QuestionInLine,
    extra=3,
    can_delete=True
)


#dz-26
BbForm =  modelform_factory(Bb, fields=['title', 'author','rubric','price','content','published'])
