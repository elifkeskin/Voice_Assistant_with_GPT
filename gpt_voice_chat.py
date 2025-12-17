# import libraries
from openai import OpenAI
import sounddevice as sd # mikrofon erişimi için sounddevice modülü
from scipy.io.wavfile import write # ses kaydının wav dosyasına yazma aracı
import os  # dosya işlemleri için os modülü
import uuid # benzersiz kimlik için uuid modülü
import re # zararlı içerik filtreleme
from datetime import datetime # tarih ve saat için datetime modülü
from dotenv import load_dotenv # .env dosyasını yüklemek için
import logging # loglama için logging modülü



# log ayarları
now = datetime.now().strftime("%Y%m%d_%H%M%S") # dosya adı için şuanki zamanı al.
log_file = f"logs/konusma_{now}.log" # log dosyasının adını oluştur.

# "logs" klasörü yoksa oluştur varsa atla
os.makedirs("logs", exist_ok=True)

# log formatını ve seviyesini ayarla: DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(
    level = logging.INFO, # log seviyesi info olarak ayarlandı, , yani info dan sonrası (INFO, WARNING, ERROR, CRITICAL) gözükür.datefmt=
    format = "%(asctime)s - %(levelname)s - %(message)s", # zaman, seviye ve mesaj içeren format
    handlers = [
        logging.FileHandler(log_file, encoding="utf-8"), # log dosyasına yazma işlemi
        logging.StreamHandler() # konsola yazma aracı
    ]
)

logger = logging.getLogger(__name__) # logger nesnesini oluşturur.

load_dotenv() # .env  dosyasını yükle
client = OpenAI() # open_ai istemcisine gidip, .env dosyasından api anahtarını alır.

DURATION = 5 # tek seferde kaç saniye kayıt alacağımızın parametresi
FS = 44100 # ses kaydı için kullanılacak frekans değeri

# zararli sözcük filtrelemesi
BANNED_WORDS = ["zararlı"] # zararlı kelimeleri tanımla

def filter_banned_words(text):
    filtered_text = text
    for word in BANNED_WORDS:
        if re.search(rf"\b{word}\b", text, flags=re.IGNORECASE): # kelime tam eşleşti mi?
             logger.warning(f"Zararlı kelime tespiti bulundu: {word}") # log kaydı
        # bulunan zararlı kelimeleri  *** ile değiştir.
        filtered_text = re.sub(rf"\b{word}\b", "***", filtered_text, flags=re.IGNORECASE) # kelimeyi yerine yıldız koy        
    return filtered_text
  
# filter_banned_words fonksiyonunu test et
# print(filter_banned_words("Merhaba, zararlı bir kelime var mı?"))

# ses kaydi alma ve kaydetme
def record_audio(filename="recorded.wav", duration = DURATION): # mikrofon kaydını alır
     logger.info("Mikrofondan ses kaydı başlatıldı")
     # sd : sounddevice
     recording = sd.rec(int(duration * FS), samplerate=FS, channels=1)
     sd.wait() # kaydın bitmesini bekler
     write(filename, FS, recording) # kayıtı wav dosyasına yazdırır
     logger.info(f"Ses kaydı tamamlandı: {filename}")

# whisper ayarları, sesi metine çevirme
def transcribe_with_whisper(audio_path): # wav dosyasını whisper ile metine çevirir.
    logger.info("Whisper ile ses yazıya çeviriliyor")
    with open(audio_path, "rb") as audio_file: # ses dosyasını aç
        transcript = client.audio.transcriptions.create(
            model="whisper-1", # openai whisper modelini kullan
            file=audio_file, # ses dosyasını yükle
            language="tr" # turkce dil ipucu
        )
    return transcript.text  # metin olarak döndürür.


# gpt 3.5 turbo ayarları, dil modeli oluşturma
# gonderilen mesaja göre cevap veren llm fonksiyonu
def get_gpt_response(messages):
    logger.info("GPT ile cevap veriliyor")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # openai gpt modelini kullan
        messages=messages # mesajlar listesi
    )
    return response.choices[0].message.content # ilk olasıcevabı döner.

# print(f"GPT Yanıt Test:{get_gpt_response([{'role': 'user', 'content': 'merhaba, yapay zeka nedir, kısaca anlat.'}])}")    
    

# hepsini birleştir ve çalıştır

if __name__ == "__main__":
    logger.info("--- GPT Sesli Chatbot Başladı----")
    logger.info(f"Konuşma log dosyası: {log_file}")

    # mesaj geçmişini sistem mesajıyla başlat
    messages = [
        {
            "role": "system", 
            "content": "You are a helpful voice assistant, responding appropriately to conversations."
        }
    ]
    
    # sonsuz döngü
    while True:
        uid = str(uuid.uuid4()) # her kayıt için unique bir id üret.
        audio_file = f"record_{uid}.wav" # geçici wav dosyası ismi

        record_audio(audio_file, DURATION) # mikrofon kaydı yap.
        question = transcribe_with_whisper(audio_file) # sesi metine çevir.
        logger.info(f"Kullanici (raw): {question}")

        filtered_question = filter_banned_words(question) # zararlı kelimeleri filtrele.and
        if filtered_question != question:
             logger.info(f"Kullanici (filtered): {filtered_question}")
        
        exit_commands = ["çık", "çıkış", "kapat", "bitir", "dur"]
        if any(command in filtered_question.lower() for command in exit_commands): # kullanıcı çık derse
            logger.info("Çıkış komutu algılandı, program sonlandırılıyor.")
            break
            
        
        messages.append({"role": "user", "content": filtered_question}) # kullanici mesajını ekle.
        response = get_gpt_response(messages) # gpt cevabı al

        logger.info(f"GPT Yanıt: {response}") # gpt yanıtını logla.and


        os.remove(audio_file) # oluşturduğumuz geçici wav dosyasını sil
    
        logger.info("--- GPT Sesli Chatbot Bitti----")

        