from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer
from django.http import JsonResponse
from openai import OpenAI
from django.db import connection
from datetime import date
from dateutil.relativedelta import relativedelta


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


def NoteSummary(request):
    client = OpenAI()
    client.embeddings.create(
        model="text-embedding-ada-002",
        input="The food was delicious and the waiter...",
        encoding_format="float"
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "write a haiku about ai"}
        ]
    )
    rows = None
    today = date.today()
    last_month = today - relativedelta(months=1)
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM core_note where created_at > '{str(last_month)}' """)
        rows = cursor.fetchall()
    print(rows)
    items = ""
    for _, value in enumerate(rows):
        items += value[1] + " "
    embeddings = client.embeddings.create(
        model="text-embedding-ada-002",
        input="items",
        encoding_format="float"
    )

    # return JsonResponse({"test": completion.choices[0].message.content})
    return JsonResponse({"test": embeddings.data.__str__()})
