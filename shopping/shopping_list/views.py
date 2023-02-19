from django.shortcuts import render

# Create your views here.
def main_shopping_list(request):
	return render(request, 'shopping_list/list.html')