from django.http import HttpResponse

def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Fajar Dwi Rianto | Event Management App</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 flex items-center justify-center min-h-screen text-gray-800">
        <div class="text-center space-y-6">
            <div>
                <h1 class="text-4xl font-bold text-blue-600 mb-2">Welcome to Event Management API</h1>
                <p class="text-gray-600 text-lg">
                    Technical Assessment by <strong>Fajar Dwi Rianto</strong>
                </p>
                <p class="text-gray-500">Built with Django REST Framework & JWT Authentication</p>
            </div>

            <div class="flex justify-center gap-4 mt-8">
                <a href="/api/docs/swagger/" 
                   class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-md transition">
                   Swagger UI
                </a>
                <a href="/api/docs/redoc/" 
                   class="px-6 py-3 bg-gray-800 hover:bg-gray-900 text-white rounded-xl shadow-md transition">
                   Redoc
                </a>
                <a href="/admin" 
                   class="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-xl shadow-md transition">
                   Admin Page
                </a>
            </div>

            <div class="pt-10 text-sm text-gray-500">
                <p>Version 1.0 • Powered by Django 5 + DRF</p>
                <p>&copy; 2025 Fajar Dwi Rianto</p>
            </div>
        </div>
    </body>
    </html>
    """)
