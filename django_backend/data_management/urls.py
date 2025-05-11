from django.urls import path
from .views import UMAPEmbeddingFileUploadView, GeneExpressionUploadView, UniqueGeneNamesView

urlpatterns = [
    path('umap-gene/', UniqueGeneNamesView.as_view(), name='umap-gene'),
    path('umap-geneexp/', GeneExpressionUploadView.as_view(), name='umap-geneexp'),
    path('umap-embeddings/', UMAPEmbeddingFileUploadView.as_view(), name='umap-embeddings'),
]
