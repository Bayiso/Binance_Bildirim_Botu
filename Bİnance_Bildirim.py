import asyncio
import time
from binance import AsyncClient, BinanceSocketManager
#from binance.websockets import binance socketmanager
import requests
import json
import nest_asyncio
nest_asyncio.apply()


bildirim_orani = 0.001 #istediğiniz bildirim oranı
bot_token = "Telegram_bot_tokeniniz"
chat_idler = ["Id niz(telegram)"]
now_price = None
coin = "LRCUSDT"

def telegram_bot_sendtext(bot_message,chat_id):
    try:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&text=' + bot_message
        response = requests.get(send_text)
        return response.json()
    except Exception as error:
        print(str(error))

async def main():
    global now_price
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket(coin)
    # then start receiving messages
    async with ts as tscm:
        
        while True:
            res = await tscm.recv()
            if now_price is not None:
                        sayacup=0
                        sayacdown=0
                        while (now_price * (1 + bildirim_orani) < float(res['p'])):
                            sayacup+=1
                            if (sayacup==2): 
                                for chat_id in chat_idler:
                                    print('Bildirim atıldı')
                                    telegram_bot_sendtext(f'(deneme)Allooooo Koş {coin} yükseliyor',chat_id)
                                now_price = float(res['p'])
                                print(now_price * (1 + bildirim_orani))
                        while (float(res['p']) * (1 + bildirim_orani) < now_price):
                            sayacdown+=1
                            if(sayacdown==2):
                                for chat_id in chat_idler:
                                    print('Bildirim atıldı')
                                    telegram_bot_sendtext(f'(deneme)Allooooo Koş {coin} düşüyor',chat_id)
                                now_price = float(res['p'])
                                print(now_price * (1 + bildirim_orani))
            else:
                now_price = float(res['p'])
                print(now_price, '-->' ,now_price * (1 + bildirim_orani))
                print(now_price, '-->' ,now_price * (1 - bildirim_orani))


    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
