from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from 六十四卦.models import 六十四卦, 卦爻辭
from django.urls import reverse

class 卜數(View):
	def post(self, request):
		hexaNum=eval(request.body)['hexaNum']
		#hexaQueryset=六十四卦.objects.all()#filter(id__isnull=False)
		卦=六十四卦.objects.filter(本卦數=hexaNum).get()
		hexaURL=reverse("卦名", kwargs={'hid':卦.id})
		return JsonResponse({'本卦組合':卦.本卦組合, 'hexaURL':hexaURL})
		#latest_blogs=[Post.objects.get(id=pid) for pid in range(latestID-idRange, latestID)]

class 卜卦(View):
	def get(self, request):
		#hexaQueryset=六十四卦.objects.all()#filter(id__isnull=False)
		六四卦=六十四卦.objects.all()#filter(id__isnull=False)
		return render(request, '卜卦.html', {'六十四卦':六四卦})
		#latest_blogs=[Post.objects.get(id=pid) for pid in range(latestID-idRange, latestID)]

class 六十四全(View):
	def get(self, request):
		#hexaQueryset=六十四卦.objects.all()#filter(id__isnull=False)
		六四卦=六十四卦.objects.all()#filter(id__isnull=False)
		return render(request, '六十四卦.html', {'六十四卦':六四卦})
		#latest_blogs=[Post.objects.get(id=pid) for pid in range(latestID-idRange, latestID)]

class 卦名(View):
	def get(self, request, hid=None):
		卦=六十四卦.objects.get(id=hid)
		卦爻=卦爻辭.objects.get(id=hid)
		錯卦=六十四卦.objects.get(本卦名=卦.錯卦名)
		錯卦爻=卦爻辭.objects.get(id=錯卦.id)
		綜卦=六十四卦.objects.get(本卦名=卦.綜卦名)
		綜卦爻=卦爻辭.objects.get(id=綜卦.id)
		複卦=六十四卦.objects.get(本卦名=卦.複卦名)
		複卦爻=卦爻辭.objects.get(id=複卦.id)
		雜卦=六十四卦.objects.get(本卦名=卦.雜卦名)
		雜卦爻=卦爻辭.objects.get(id=雜卦.id)
		return render(request, 'HEXA.html', {'卦':卦, '卦爻':卦爻, '錯卦爻':錯卦爻, '綜卦爻':綜卦爻, '複卦爻':複卦爻, '雜卦爻':雜卦爻})

class 卦爻Lounge(View):
	def get(self, request, hid=None):
		卦爻lounge=卦爻辭.objects.get(id=hid)
		return render(request, '卦爻辭.html', {'卦爻lounge':卦爻lounge})
