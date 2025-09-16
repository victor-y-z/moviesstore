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
        # Prevent editing once stock is zero
        if self.instance and self.instance.amount_left == 0:
            raise ValidationError("You cannot modify amount_left once it reaches 0.")
        return amount_left


class MovieAdmin(admin.ModelAdmin):
    form = MovieForm
    ordering = ['name']
    search_fields = ['name']
    list_display = ['name', 'price', 'amount_left']   # show amount_left in list view
    list_editable = ['amount_left']                   # editable inline in list
    fields = ['name', 'price', 'description', 'image', 'amount_left']  # show in form


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
