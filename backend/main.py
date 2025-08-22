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

    email = (EmailBuilder()
         .from_email(os.getenv("FROM_EMAIL"), form.nome)
         .to_many([{"email": os.getenv("TO_EMAIL"), "name": "Administrador"}])
         .template("0r83ql3opy0lzw1j")
         .subject("Mensagem de KingdomSys")
         .personalize_many([{
             "email": os.getenv("TO_EMAIL"),
             "data": {
                 "user":{
                     "mail":form.email,
                     "phone":form.telefone,
                     "message":form.mensagem,
                     "subject":form.subject
                 },
                 "comment":{
                     "date":datetime.now().strftime("%d/%m/%Y %H:%M")
                 },
                 "account_name":"KingdomSys"
             }
         }])
         .build())


    try:
        response = ms.emails.send(email)
        return {"message": "Email sent successfully", "status_code": status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
