import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProfileImageSerializer(serializers.Serializer):
    profile_image = serializers.ImageField()


class ProfileImageAPI(UpdateAPIView):
    serializer_class = ProfileImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    allowed_methods = ["PUT"]

    def put(self, request, *args, **kwargs):
        image_file = request.FILES.get("profile_image")

        if not image_file:
            return Response({"error": "No image Files"}, status=400)

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        random_filename = f"profile_images/user/{uuid.uuid4()}.webp"

        filename = fs.save(random_filename, image_file)

        file_url = fs.url(filename)

        return Response({"file_url": file_url}, status=200)
