import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from mailersend import emails
import uvicorn

load_dotenv()

app = FastAPI()

class ContactForm(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    subject: str
    mensagem: str

@app.post("/api/send_email")
async def send_email(form: ContactForm):
    mailer = emails.NewEmail()

    mail_body = {}

    mail_from = {
        "name": form.nome,
        "email": os.getenv("FROM_EMAIL"),
    }

    recipients = [
        {
            "name": "Recipient",
            "email": os.getenv("TO_EMAIL"),
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(form.subject, mail_body)

    html_content = f"""
    <h2>KingdomSys</h2>
    <h3>Nova mensagem do formulário de contato</h3>
    <p><strong>Nome:</strong> {form.nome}</p>
    <p><strong>Email:</strong> {form.email}</p>
    <p><strong>Telefone:</strong> {form.telefone}</p>
    <p><strong>Assunto:</strong> {form.subject}</p>
    <p><strong>Mensagem:</strong></p>
    <p>{form.mensagem}</p>
    """
    mailer.set_html_content(html_content, mail_body)

    try:
        mailer.send(mail_body)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
