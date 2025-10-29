from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Society(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    established_date = models.DateField(_("Established Date"), blank=True, null=True)
    contact_email = models.EmailField(_("Contact Email"), blank=True, null=True)
    contact_phone = models.CharField(_("Contact Phone"), max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Society")
        verbose_name_plural = _("Societys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Society_detail", kwargs={"pk": self.pk})
