# api/views.py
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SerialValidationSerializer
from authcode_session.models import Authcode


class SerialValidationView(APIView):
    def post(self, request):
        serializer = SerialValidationSerializer(data=request.data)
        if serializer.is_valid():
            serial = serializer.validated_data['serial']
            try:
                authcode = Authcode.objects.get(serial=serial)
                if authcode.expiration_date > timezone.now():
                    request.session['authcode'] = authcode.serial
                    request.session.set_expiry(authcode.expiration_date)
                    return Response({'status': 'success'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'expired'}, status=status.HTTP_400_BAD_REQUEST)
            except Authcode.DoesNotExist:
                return Response({'status': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionValidationView(APIView):
    def get(self, request):
        if 'authcode' in request.session:
            try:
                authcode = Authcode.objects.get(serial=request.session['authcode'])
                if authcode.expiration_date > timezone.now():
                    return Response({'status': 'success'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'expired'}, status=status.HTTP_400_BAD_REQUEST)
            except Authcode.DoesNotExist:
                return Response({'status': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'no session'}, status=status.HTTP_400_BAD_REQUEST)
