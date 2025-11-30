import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from googleapiclient.discovery import build

# -- التوكن والمفتاح هنا --
TELEGRAM_BOT_TOKEN = "8482473599:AAEiKjuU3xCP6KT8htF7zjUecfc_jiVKiWs"
YOUTUBE_API_KEY = "AIzaSyAEwyyRQwqKb_bsxSalsJHEhDkb3zEptFY"  # المفتاح الجديد

# إعداد تسجيل الدخول لعرض الأخطاء
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# دالة للبحث عن أحدث الفيديوهات
def search_youtube():
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        part="snippet",
        q="اخبار اليوم",
        order="date",
        type="video",
        maxResults=5
    )
    response = request.execute()
    
    videos = []
    for item in response.get('items', []):
        video_title = item['snippet']['title']
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append(f"{video_title}\n{video_url}")
        
    return videos

# دالة الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"مرحباً {user.mention_html()}! أنا بوت رادار الترند. استخدم الأمر /check للبحث عن أحدث الفيديوهات.",
    )

# دالة الأمر /check
async def check_trends(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("جاري البحث عن أحدث الفيديوهات، يرجى الانتظار...")
    
    try:
        videos = search_youtube()
        if videos:
            message = "إليك أحدث 5 فيديوهات تم نشرها:\n\n" + "\n\n".join(videos)
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("لم أتمكن من العثور على فيديوهات حالياً.")
    except Exception as e:
        logger.error(f"حدث خطأ أثناء البحث في يوتيوب: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء محاولة الاتصال بيوتيوب.")

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check_trends))

    logger.info("البوت قيد التشغيل...")
    application.run_polling()

if __name__ == "__main__":
    main()
