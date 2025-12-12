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
