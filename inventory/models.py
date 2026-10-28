"""
BloodStock model for tracking inventory of blood units.

# BBMS-F-020: Real-time stock count per blood group and component.
"""

from django.db import models


class BloodStock(models.Model):
    """
    Inventory record for a specific blood group and component combination.
    """

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    COMPONENT_CHOICES = [
        ('whole_blood', 'Whole Blood'),
        ('red_cells', 'Red Cells'),
        ('plasma', 'Plasma'),
        ('platelets', 'Platelets'),
    ]

    # BBMS-F-020
    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        help_text='Blood group (A+, A-, B+, B-, AB+, AB-, O+, O-).'
    )
    component = models.CharField(
        max_length=20,
        choices=COMPONENT_CHOICES,
        help_text='Blood component type.'
    )
    units_available = models.PositiveIntegerField(
        default=0,
        help_text='Number of units available in stock.'
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp when stock was last updated.'
    )

    class Meta:
        unique_together = ('blood_group', 'component')
        ordering = ['blood_group', 'component']

    def __str__(self):
        return f"{self.blood_group} - {self.get_component_display()}: {self.units_available} units"
