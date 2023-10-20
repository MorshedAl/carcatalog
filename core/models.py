from django.db import models
from django.urls import reverse, reverse_lazy


class Car(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='cars')
    title = models.CharField(("Title"), max_length=250)
    slug = models.SlugField(("Slug"),null=True)
    brand = models.CharField(("Brand"), max_length=50)
    modal = models.CharField(("Model"), max_length=50)
    description = models.TextField(("Description"))
    price = models.DecimalField(("Price"), max_digits=12, decimal_places=2)
    image = models.ImageField(("Picture"), upload_to='car/')
    create = models.DateTimeField(("create"), auto_now_add=True)
    update = models.DateTimeField(("update"), auto_now=True)

    def __str__(self) -> str:
        return f'{self.title}--->{self.brand}--->{self.modal}'
    
    def get_absolute_url(self):
        return reverse_lazy("car_detail", kwargs={"pk": self.pk,'slug':self.slug})
    