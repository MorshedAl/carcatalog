from django import forms

from core.models import Car


class CarCreateForm(forms.ModelForm):

    class Meta:
        model = Car
        exclude = ('id','slug','user')

    def __init__(self ,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder':field.title(),
                "class":"bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            })
