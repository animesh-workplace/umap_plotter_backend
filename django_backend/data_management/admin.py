from django.contrib import admin
from .models import UMAPEmbedding, GeneExpression, Gene

# Register your models here.
@admin.register(UMAPEmbedding)
class UMAPEmbeddingAdmin(admin.ModelAdmin):
    list_display = ('cell_id', 'x', 'y')
    search_fields = ('cell_id',)

@admin.register(GeneExpression)
class GeneExpressionAdmin(admin.ModelAdmin):
    list_display = ('gene_name', 'cell_id', 'expression_value')
    search_fields = ('gene_name', 'cell_id')

@admin.register(Gene)
class GeneAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)