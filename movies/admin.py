from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Movie, Review


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

    def clean_amount_left(self):
        amount_left = self.cleaned_data.get("amount_left")
        # If the movie is already at 0, don’t allow changing it
        if self.instance and self.instance.amount_left == 0:
            raise ValidationError("You cannot modify amount_left once it reaches 0.")
        return amount_left


class MovieAdmin(admin.ModelAdmin):
    form = MovieForm
    ordering = ['name']
    search_fields = ['name']
    list_display = ['name', 'amount_left']
    list_editable = ['amount_left']
    fields = ['name', 'amount_left']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
