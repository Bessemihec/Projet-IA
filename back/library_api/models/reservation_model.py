from django.db import models
from datetime import datetime

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('validated', 'Validated'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
    ]
    
    # Relations vers le livre et l'utilisateur (Student)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    student = models.ForeignKey('User', on_delete=models.CASCADE)  # Associer à User, mais ce sera un Student

    # Autres champs
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='En cours')
    date_reservation = models.DateTimeField(default=datetime.now)
    duration = models.CharField(max_length=100)  # Changer en CharField pour une durée sous forme de chaîne
    date_fin_reservation = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Reservation for {self.student.username} on {self.book.title} - Status: {self.status}"
