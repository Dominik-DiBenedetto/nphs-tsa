from django.shortcuts import render
from django.http import HttpResponse
from pypdf import PdfReader
import json

# Create your views here.
def portfolio_scanner(request):
    return render(request, "portfolio_scanner.html")

def process_portfolio(request):
    if request.method == "POST":
        if "pdfFile" not in request.FILES:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        portfolio = request.FILES["portfolio"]
        portfolio_reader = PdfReader(portfolio)

        num_portfolio_pages = len(portfolio_reader.pages)

        # To extract text from all pages:
        full_portfolio_text = ""
        for page_num in range(num_portfolio_pages):
            page = portfolio_reader.pages[page_num]
            full_portfolio_text += page.extract_text() + "\n" # Add a newline for readability between pages
        
        # Get ceg
        ceg = request.FILES["ceg"]
        ceg_reader = PdfReader(ceg)

        num_ceg_pages = len(ceg_reader.pages)

        # To extract text from all pages:
        full_ceg_text = ""
        for page_num in range(num_ceg_pages):
            page = ceg_reader.pages[page_num]
            full_ceg_text += page.extract_text() + "\n"

        return HttpResponse("Good")