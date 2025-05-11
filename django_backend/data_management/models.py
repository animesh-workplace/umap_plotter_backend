from django.db import models

class UMAPEmbedding(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    cell_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.cell_id

    class Meta:
        indexes = [ 
            models.Index(fields=['cell_id']),
        ]


class GeneExpression(models.Model):
    expression_value = models.FloatField()
    cell_id = models.CharField(max_length=255)
    gene_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('gene_name', 'cell_id')
        indexes = [
            models.Index(fields=['gene_name', 'cell_id']),
        ]

class Gene(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name