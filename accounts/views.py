from rest_framework import viewsets, status
from .models import Profile, DCCUser
import requests
from rest_framework.response import Response
from .serializers import ProfileSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = DCCUser.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Modify the data here
        for note in data:
            url = "https://leetcode.com/graphql"
            global_data = """
    query userSessionProgress($username: String!) {
  allQuestionsCount {
    difficulty
    count
  }
  matchedUser(username: $username) {
    submitStats {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
      totalSubmissionNum {
        difficulty
        count
        submissions
      }
    }
  }
}
    
"""
            response = requests.get(url=url, json={"query": global_data, "variables": {"username": "MgenGlder23"}, "operationName": "userSessionProgress"}, timeout=10)
            note['leetcode_stats'] = response.json()
        return Response(data)