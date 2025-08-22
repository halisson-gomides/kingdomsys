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
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style type="text/css">
                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
                body {
                    font-family: 'Poppins', sans-serif;
                }
                .gradient-bg {
                    background: linear-gradient(135deg, #3730A3 0%, #805ad5 100%);
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
