import logging
from django.db.models import Q
from django.db import connection
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import UMAPEmbedding, GeneExpression, Gene
from .serializers import UMAPEmbeddingSerializer, GeneExpressionSerializer

import psycopg2

conn = psycopg2.connect(
    port=5432,
    password='',
    user='animesh',
    host='localhost',
    dbname='GeneEchelon',
)

logger = logging.getLogger(__name__)

class UMAPEmbeddingFileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        import fireducks.pandas as pd
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        try:
            df = pd.read_csv(file, sep='\t')
            required_columns = {'cell.id', 'umapcca_1', 'umapcca_2'}
            if not required_columns.issubset(df.columns):
                return Response({'error': f'Missing required columns: {required_columns - set(df.columns)}'}, status=status.HTTP_400_BAD_REQUEST)

            records = df.rename(columns={'cell.id': 'cell_id', 'umapcca_1': 'x', 'umapcca_2': 'y'}).to_dict(orient='records')
            serializer = UMAPEmbeddingSerializer(data=records, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'Success', 'count': len(records)}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request, *args, **kwargs):
        embeddings = UMAPEmbedding.objects.all().order_by('cell_id')
        serializer = UMAPEmbeddingSerializer(embeddings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class GeneExpressionUploadView(APIView):
    parser_classes = [MultiPartParser]

    # def post(self, request, *args, **kwargs):
    #     import fireducks.pandas as pd
    #     if 'file' not in request.FILES:
    #         return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    #     file = request.FILES['file']
    #     try:
    #         df = pd.read_feather(file)
    #         required_columns = {'cell_id', 'gene_name', 'expression_value'}
    #         if not required_columns.issubset(df.columns):
    #             return Response({'error': f'Missing required columns: {required_columns - set(df.columns)}'}, status=status.HTTP_400_BAD_REQUEST)            
    #         records = df.to_dict(orient='records')
    #         serializer = GeneExpressionSerializer(data=records, many=True)

    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({'status': 'Success', 'inserted': len(records)}, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def get(self, request, *args, **kwargs):
        gene_name = request.query_params.get('gene_name')
        if not gene_name:
            return Response({'error': 'gene_name parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # print('Raeached here1')
        # with conn.cursor() as cursor:
        #     print('Raeached here1a')
        #     cursor.execute("""
        #         SELECT expression_value
        #         FROM data_management_geneexpression
        #         WHERE gene_name = %s
        #         ORDER BY cell_id
        #     """, [gene_name])
        #     print('Raeached here1b')
        #     result = [row[0] for row in cursor.fetchall()]
        # print('Raeached here2', result)

        # expressions = (
        #     GeneExpression.objects
        #     .filter(gene_name=gene_name)
        #     .only('expression_value', 'cell_id')
        #     .order_by('cell_id')
        #     .values_list('expression_value', flat=True)
        # )

        expressions = (
            GeneExpression.objects
            .filter(gene_name=gene_name)
            .order_by('cell_id')
            .values_list('expression_value', 'cell_id')  # Return both
        )

        result = [expr for expr, _ in expressions]
        return Response(result, status=status.HTTP_200_OK)


class UniqueGeneNamesView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('gene', '').strip()
        
        gene_names = (
            Gene.objects
            .filter(name__icontains=query) if query else Gene.objects.all()
        )
        gene_names = (
            gene_names
            .order_by('name')
            .values_list('name', flat=True)
            .distinct()[:50]
        )

        return Response(list(gene_names), status=status.HTTP_200_OK)