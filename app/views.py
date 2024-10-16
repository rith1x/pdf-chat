from django.shortcuts import render
from django.http import JsonResponse
from langchain_community.document_loaders import PyPDFLoader
import requests
import os

def showWelcome(request):
    return render(request,"welcome.html")


def handlePdf(request):
    if request.method == "POST":
        pdflink = request.POST.get("link")
        print(f"Received PDF link: {pdflink}")
        info = ""

        pdf_dir = '/tmp'
        pdf_file_path = os.path.join(pdf_dir, 'file.pdf')

        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        try:
            response = requests.get(pdflink)
            if response.status_code == 200:
                with open(pdf_file_path, 'wb') as f:
                    f.write(response.content)
                print("File successfully downloaded and saved")
                info = "File successfully downloaded and saved"
            else:
                print(f"Failed to download the PDF. Status code: {response.status_code}")
                info = f"Failed to download the PDF. Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {str(e)}")
            info = f"Error occurred while downloading the PDF: {str(e)}"

        return render(request, "main.html", {'info': info})
    
    return render(request, "main.html", {'info': "No POST request made."})


def handleQuestion(request):
    if request.method == 'POST':
        qn = request.POST.get('ques')

        loader = PyPDFLoader('/tmp/file.pdf')
        docs = loader.load()

        try:
            result = docs[int(qn)].page_content
        except (IndexError, ValueError):
            result = "Invalid question or page number. Please enter a valid page number."
    
        resp = {'message': result}
        return JsonResponse(resp)
    return JsonResponse({'error':'Error'},status=404)
