import pandas as pd

from rest_framework.parsers import MultiPartParser, FormParser


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PriceData
from .serializers import PriceDataSerializer

class PriceListAPIView(APIView):
    """GET all price data + POST new price data"""

    def get(self, request):
        data = PriceData.objects.all().order_by('-time')  # newest first
        serializer = PriceDataSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PriceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriceDetailAPIView(APIView):
    """GET, PUT, DELETE for a single price entry"""

    def get_object(self, pk):
        try:
            return PriceData.objects.get(pk=pk)
        except PriceData.DoesNotExist:
            return None

    def get(self, request, pk):
        price = self.get_object(pk)
        if not price:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PriceDataSerializer(price)
        return Response(serializer.data)

    def put(self, request, pk):
        price = self.get_object(pk)
        if not price:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PriceDataSerializer(price, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        price = self.get_object(pk)
        if not price:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class PriceCSVUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "CSV file is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not file.name.endswith(".csv"):
            return Response(
                {"error": "Only CSV files are allowed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pd.read_csv(file)
        except Exception as e:
            return Response(
                {"error": f"Invalid CSV file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        required_columns = {"time", "open", "high", "low", "close"}
        if not required_columns.issubset(df.columns):
            return Response(
                {
                    "error": "CSV must contain columns: time, open, high, low, close"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        created = 0
        errors = []

        for index, row in df.iterrows():
            serializer = PriceDataSerializer(data=row.to_dict())

            if serializer.is_valid():
                serializer.save()
                created += 1
            else:
                errors.append({
                    "row": index + 1,
                    "errors": serializer.errors
                })

        return Response(
            {
                "message": "CSV processed",
                "rows_created": created,
                "rows_failed": len(errors),
                "errors": errors
            },
            status=status.HTTP_201_CREATED
        )
