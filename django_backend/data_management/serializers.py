from rest_framework import serializers
from .models import UMAPEmbedding, GeneExpression

class UMAPEmbeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UMAPEmbedding
        fields = '__all__'


class GeneExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneExpression
        fields = '__all__'