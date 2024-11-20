from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

class UserDocumentsCreateAPIView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserDocumentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Request submitted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateStatusAPIView(APIView):
    def post(self, request, *args, **kwargs):
        document_id = kwargs.get('id')  # Document ID from the URL
        user_id = kwargs.get('user_id')  # User ID from the URL

        try:
            # Fetch the document by id and user_id
            document = UserDocuments.objects.get(id=document_id, user_id=user_id)

            # Update the status to True
            serializer = UpdateStatusSerializer(document, data={'status': True}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Status updated successfully."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except UserDocuments.DoesNotExist:
            return Response(
                {"error": "Document not found for the provided ID and User ID."},
                status=status.HTTP_404_NOT_FOUND
            )


class PendingUpdateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pending_documents = UserDocuments.objects.filter(status=False)

        serializer = UserDataSerializer(pending_documents, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)