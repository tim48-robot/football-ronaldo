from django.shortcuts import render
# Create your views here.
def show_main(request):
    context = {
        'nama_aplikasi': 'football_project',
        'nama' : 'Justin Timothy Wirawan',
        'kelas': 'PBP D'
    }

    return render(request, "main.html", context)