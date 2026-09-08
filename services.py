import httpx
import random


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


async def get_cat_image():
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            response = await client.get(url, timeout=5)
            if response.status_code == 200 and response.text:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0]["url"]
        except Exception as e:
            print(f"Mushuk API xatosi yuz berdi: {e}")
    return "https://thecatapi.com"


async def get_dog_image():
    url = "https://dog.ceo/api/breeds/image/random"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            response = await client.get(url, timeout=5)
            if response.status_code == 200 and response.text:
                data = response.json()
                return data.get("message")
        except Exception as e:
            print(f"Kuchuk API xatosi yuz berdi: {e}")
    return "https://dog.ceo"



async def get_random_number():
    return str(random.randint(1, 1000))


async def get_random_card():
    bin_num = random.choice(["4", "5", "3"])
    card_no = bin_num + "".join(str(random.randint(0, 9)) for _ in range(15))

    expiry = f"{random.randint(1, 12):02d}/{random.randint(26, 31)}"
    cvv = str(random.randint(100, 999))

    card_info = (
        f" **Plastik Karta Ma'lumotlari:**\n\n"
        f" Karta raqami: `{card_no}`\n"
        f" Amal qilish muddati: `{expiry}`\n"
        f" CVV/CVC: `{cvv}`"
    )
    return card_info
