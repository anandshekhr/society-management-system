from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class TowerOrBlock(models.Model):
    society = models.ForeignKey("society.Society", verbose_name=_("Society"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    no_of_floors = models.PositiveIntegerField(_("Number of Floors"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("TowerOrBlock")
        verbose_name_plural = _("TowerOrBlocks")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("TowerOrBlock_detail", kwargs={"pk": self.pk})

class FloorDescription(models.Model):
    tower_or_block = models.ForeignKey(TowerOrBlock, verbose_name=_("Tower or Block"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=255)  
    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("FloorDescription")
        verbose_name_plural = _("FloorDescriptions")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("FloorDescription_detail", kwargs={"pk": self.pk})


class Flat(models.Model):
    class FlatType(models.TextChoices):
        STUDIO = "ST", _("Studio")
        ONE_BHK = "1BHK", _("1 BHK")
        TWO_BHK = "2BHK", _("2 BHK")
        THREE_BHK = "3BHK", _("3 BHK")
        FOUR_BHK = "4BHK", _("4 BHK")
        PENTHOUSE = "PH", _("Penthouse")
        DUPLEX = "DP", _("Duplex")
    society = models.ForeignKey("society.Society", verbose_name=_(""), on_delete=models.CASCADE)
    tower_or_block = models.ForeignKey(TowerOrBlock, verbose_name=_("Tower or Block"), on_delete=models.CASCADE)
    flat_type = models.CharField(_("Flat Type"), max_length=5, choices=FlatType.choices)
    flat_number = models.CharField(_("Flat Number"), max_length=50)
    owner_name = models.CharField(_("Owner Name"), max_length=255)
    contact_email = models.EmailField(_("Contact Email"), blank=True, null=True)
    contact_phone = models.CharField(_("Contact Phone"), max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Flat")
        verbose_name_plural = _("Flats")

    def __str__(self):
        return self.flat_number

    def get_absolute_url(self):
        return reverse("Flat_detail", kwargs={"pk": self.pk})
