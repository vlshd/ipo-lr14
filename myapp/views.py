from django.shortcuts import render
import json
import os
from django.conf import settings
from django.http import JsonResponse

def get_dump(request):
    file_path = os.path.join(settings.BASE_DIR, 'dump.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        return Jsonresponse({"error": "File not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

def hello_world(request):
    return render(request,'myapp/index.html')

def about(request):
    return render(request, 'myapp/aboutAuthor.html')

def aboutShop(request):
    return render(request, 'myapp/aboutShop.html')
    
def load_qualifications(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    
    qualifications = [
        {
            "id": item["pk"],
            "name": item["fields"]["title"],
        }
        for item in data if item.get("model") == "data.specialty"
    ]

    return qualifications

qualifications = load_qualifications("dump.json")

def get_qualification_by_id(q_id):
    for qualification in qualifications:
        if qualification.get("id") == q_id:
            return qualification
    return None

def spec(request):

    return render(request, "myapp/spec_list.html", {"qualifications": qualifications,
        'title': 'Список квалификаций'})

def specs(request, q_id: int):
    qualification = get_qualification_by_id(q_id)
    return render(request, "myapp/spec_detail.html", {"qualification": qualification,
    'title': f"Квалификация № {q_id}" }) if qualification else HttpResponse("Квалификация не найдена")
