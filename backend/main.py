import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from mailersend import MailerSendClient, EmailBuilder
import uvicorn
from datetime import datetime

load_dotenv()

app = FastAPI()

# Configuração de CORS: Essencial para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kingdomsys.com"], # Especifique o domínio do seu frontend
    allow_credentials=True,
    allow_methods=["GET", "POST"], # Permita os métodos que você usa
    allow_headers=["*"], # Permita todos os cabeçalhos, ou especifique-os
)

class ContactForm(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    subject: str
    mensagem: str

@app.post("/api/send_email")
async def send_email(form: ContactForm):
    ms = MailerSendClient()
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nova Mensagem Recebida - KingdomSys</title>
        <style type="text/css">
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f3f4f6;
                color: #111827;
            }
            .gradient-bg {
                background: linear-gradient(135deg, #3730A3 0%, #805ad5 100%);
            }
            .max-w-2xl {
                max-width: 42rem;
            }
            .mx-auto {
                margin-left: auto;
                margin-right: auto;
            }
            .my-8 {
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
            .bg-white {
                background-color: #ffffff;
            }
            .rounded-lg {
                border-radius: 0.5rem;
            }
            .shadow-lg {
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            }
            .overflow-hidden {
                overflow: hidden;
            }
            .px-6 {
                padding-left: 1.5rem;
                padding-right: 1.5rem;
            }
            .py-4 {
                padding-top: 1rem;
                padding-bottom: 1rem;
            }
            .text-white {
                color: #ffffff;
            }
            .flex {
                display: flex;
            }
            .items-center {
                align-items: center;
            }
            .mr-3 {
                margin-right: 0.75rem;
            }
            .h-10 {
                height: 2.5rem;
            }
            .w-10 {
                width: 2.5rem;
            }
            .text-2xl {
                font-size: 1.5rem;
                line-height: 2rem;
            }
            .font-bold {
                font-weight: 700;
            }
            .text-sm {
                font-size: 0.875rem;
                line-height: 1.25rem;
            }
            .opacity-80 {
                opacity: 0.8;
            }
            .text-gray-600 {
                color: #4b5563;
            }
            .mb-6 {
                margin-bottom: 1.5rem;
            }
            .space-y-4 > * + * {
                margin-top: 0.75rem;
            }
            .border-l-4 {
                border-left-width: 4px;
                border-left-style: solid;
            }
            .border-indigo-500 {
                border-color: #6366f1;
            }
            .pl-4 {
                padding-left: 1rem;
            }
            .text-gray-500 {
                color: #6b7280;
            }
            .uppercase {
                text-transform: uppercase;
            }
            .tracking-wider {
                letter-spacing: 0.05em;
            }
            .text-gray-800 {
                color: #1f2937;
            }
            .ms-1 {
                margin-left: 0.25rem;
                margin-top: 0.7rem;
            }
            .text-purple-600 {
                color: #9333ea;
            }
            .hover\:text-purple-800:hover {
                color: #6b21a8;
            }
            .mt-1 {
                margin-top: 0.25rem;
            }
            .border-2 {
                border-width: 2px;
            }
            .border-purple-800 {
                border: 2px solid #805ad5;
            }
            .rounded-md {
                border-radius: 0.375rem;
            }
            .p-4 {
                padding: 1rem;
            }
            .mt-2 {
                margin-top: 0.5rem;
            }
            .bg-gray-50 {
                background-color: #ebeef0;
            }
            .text-gray-700 {
                color: #374151;
            }
            .mt-8 {
                margin-top: 2rem;
            }
            .pt-6 {
                padding-top: 1.5rem;
            }
            .border-t {
                border-top-width: 1px;
            }
            .border-gray-200 {
                border-color: #e5e7eb;
            }
            .text-indigo-600 {
                color: #4f46e5;
            }
            .flex-col {
                flex-direction: column;
            }
            .md\:flex-row {
                flex-direction: row;
            }
            .justify-between {
                justify-content: space-between;
            }
            .mb-4 {
                margin-bottom: 1rem;
            }
            .md\:mb-0 {
                margin-bottom: 0;
            }
            .h-8 {
                height: 2rem;
            }
            .font-medium {
                font-weight: 500;
            }
            .text-xs {
                font-size: 0.75rem;
                line-height: 1rem;
            }
            .text-center {
                text-align: center;
            }
            .md\:text-left {
                text-align: left;
            }
        </style>
    </head>           
        <body class="bg-gray-100">
            <div class="max-w-2xl mx-auto my-8 bg-white rounded-lg shadow-lg overflow-hidden">
                <!-- Header -->
                <div class="gradient-bg px-6 py-4 text-white">
                    <div class="flex items-center">
                        <div class="mr-3">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                        </div>
                        <div>
                            <h1 class="text-2xl font-bold">Nova Mensagem Recebida</h1>
                            <p class="text-sm opacity-80">Formulário de contato - KingdomSys</p>
                        </div>
                    </div>
                </div>"""
    
    html_content += f"""
                <!-- Content -->
                <div class="px-6 py-4">
                    <p class="text-gray-600 mb-6">Você recebeu uma nova mensagem através do formulário de contato do seu site. Aqui estão os detalhes:</p>
                    
                    <div class="space-y-4">
                        <!-- Name -->
                        <div class="border-l-4 border-indigo-500 pl-4 flex">
                            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider">Nome: </h3>
                            <p class="text-gray-800 ms-1">{form.nome}</p>
                        </div>
                        
                        <!-- Email -->
                        <div class="border-l-4 border-indigo-500  pl-4 flex">
                            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider">Email:</h3>
                            <p class="text-gray-800 ms-1">
                                <a href="mailto:{form.email}" class="text-purple-600 hover:text-purple-800">{form.email}</a>
                            </p>
                        </div>
                        
                        <!-- Phone -->
                        <div class="border-l-4 border-indigo-500 pl-4 flex">
                            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider">Telefone:</h3>
                            <p class="text-gray-800 ms-1">
                                <a href="tel:{form.telefone}" class="text-purple-600 hover:text-purple-800">{form.telefone}</a>
                            </p>
                        </div>
                        
                        <!-- Subject -->
                        <div class="border-l-4 border-indigo-500 pl-4">
                            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider">Assunto:</h3>
                            <p class="text-gray-800 mt-1">{form.subject}</p>
                        </div>
                        
                        <!-- Message -->
                        <div class="border-2 rounded-md border-purple-800 p-4">
                            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider">Mensagem</h3>
                            <div class="mt-2 p-4 bg-gray-50 rounded-md text-gray-700">
                                {form.mensagem}
                            </div>
                        </div>
                    </div>"""
    
    html_content += """
                    <div class="mt-8 pt-6 border-t border-gray-200">
                        <p class="text-sm text-gray-500">Esta mensagem foi enviada através do formulário de contato em <a href="https://kingdomsys.com" class="text-indigo-600 hover:text-purple-800">kingdomsys.com</a>.</p>
                    </div>
                </div>
                
                <!-- Footer -->
                <div class="bg-gray-50 px-6 py-4">
                    <div class="flex flex-col md:flex-row justify-between items-center">
                        <div class="flex items-center mb-4 md:mb-0">
                            <img src="https://img1.wsimg.com/isteam/ip/3414b9ec-40fe-4bcb-873a-cf0ef3f81fb1/favicon/1b1ee852-c8c4-48da-85a5-da88b271c600.png/:/rs=w:180,h:180,m" alt="KingdomSys Logo" class="h-8 mr-3">
                            <span class="text-gray-700 font-medium">KingdomSys</span>
                        </div>
                    </div>
                    <p class="text-xs text-gray-500 mt-4 text-center md:text-left">© 2023 KingdomSys. Todos os direitos reservados.</p>
                </div>
            </div>
        </body>
        </html>"""
    
    email = (EmailBuilder()
         .from_email(os.getenv("FROM_EMAIL"), "KingdomSys - Formulário")
         .to_many([{"email": os.getenv("TO_EMAIL"), "name": "Administrador"}])
         .subject("Mensagem de KingdomSys")
         .html(html_content)
         .build())
        #  .template("0r83ql3opy0lzw1j")
        #  .personalize_many([{
        #      "email": os.getenv("TO_EMAIL"),
        #      "data": {
        #          "user":{
        #              "mail":form.email,
        #              "phone":form.telefone,
        #              "message":form.mensagem,
        #              "subject":form.subject
        #          },
        #          "comment":{
        #              "date":datetime.now().strftime("%d/%m/%Y %H:%M")
        #          },
        #          "account_name":"KingdomSys"
        #      }
        #  }])


    try:
        response = ms.emails.send(email)
        return {"message": "Email sent successfully", "status_code": status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
