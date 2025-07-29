import fitz  # PyMuPDF
import requests
from io import BytesIO
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

PDF_URL = "https://raw.githubusercontent.com/digdam200/shia-qa-bot/main/books/10503-fa-naghd-vahabiat-az-daron.pdf"

def extract_text_from_pdf():
    response = requests.get(PDF_URL)
    if response.status_code != 200:
        return "خطا در دریافت فایل"
    text = ""
    with BytesIO(response.content) as f:
        doc = fitz.open(stream=f, filetype="pdf")
        for page in doc:
            text += page.get_text()
    return text

def search_answer(question, full_text):
    for paragraph in full_text.split("\n"):
        if question.strip() in paragraph:
            return paragraph.strip()
    return "پاسخی پیدا نشد."

async def start(update, context):
    await update.message.reply_text("سلام! من ربات پاسخگوی اعتقادی شیعه هستم.")

async def answer(update, context):
    text = extract_text_from_pdf()
    result = search_answer(update.message.text, text)
    await update.message.reply_text(result)

app = ApplicationBuilder().token("8030976175:AAHMGSfXLySJ0YWp6Jw-bGfzuEhnqifKitk").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
app.run_polling()
