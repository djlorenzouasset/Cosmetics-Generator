import colorama 
import time
import glob
import requests
import os
import shutil

from utils.BaseIcon import BaseIcon
from utils.Variants import BaseVar
from utils.newsgen import NewsImage

from math import ceil, sqrt
from colorama import Fore
from PIL import Image

colorama.init(autoreset=True)

class Commands:
    def __init__(self, data):
        self.language = data.language
        self.searchlanguage = data.searchLanguage
        self.twitter = data.twitter
        if self.twitter:
            self.newText = data.newcosmeticsText
            self.pakText = data.newpakText
        self.discord = data.discord
        self.start = data.start_time
        if self.discord:
            self.rpc = data.rpc
        
    def NewVariants(self):
        print(Fore.GREEN + "Generating new variants..")
        try:
            if self.discord:
                self.rpc.update(
                    details=f"Playing v{requests.get('https://benbot.app/api/v1/status').json()['currentFortniteVersion'].replace('++Fortnite+Release-', '').split('-')[0]}",
                    state="Generating new variants",
                    large_image="app_image",
                    large_text="Cosmetic Generator",
                    small_text="User access",
                    start=int(self.start),
                    small_image="user_access",
                    buttons=[{"label": "Download", "url": "https://github.com/djlorenzouasset/Cosmetics-Generator"}]
                )
            res = requests.get(
                'https://benbot.app/api/v1/files/added'
            ).json()
            datas = []
            for x1 in res:
                if x1.startswith('FortniteGame/Content/Athena/Items/CosmeticVariantTokens/'):
                    path = x1
                    image = requests.get(f'https://benbot.app/api/v1/assetProperties?path={path}&lang={self.language}').json()['export_properties'][0]
                    datas.append(BaseVar().main(image))
                    print(Fore.BLUE + f"Generated image for {image['cosmetic_item']}..")
            row_n = len(datas)
            rowslen = ceil(sqrt(row_n))
            columnslen = round(sqrt(row_n))

            mode = "RGB"
            px = 512

            rows = rowslen * px
            columns = columnslen * px
            image = Image.new(mode, (rows, columns))

            i = 0
            for card in datas:
                image.paste(
                    card,
                    ((0 + ((i % rowslen) * card.width)),
                    (0 + ((i // rowslen) * card.height)))
                )

                i += 1

            image.save(f"images/newvariants.png")   
            shutil.rmtree('cache')
            os.makedirs('cache')
        except:
            print(Fore.RED + f"[ERROR] Api down!")
            

    def NewCosmetics(self):
        print(Fore.GREEN + "Generating new cosmetics..")
        res = requests.get(
            f'https://fortnite-api.com/v2/cosmetics/br/new?language={self.language}'
        )
        responce = res.json()
        if res.status_code == 200:
            if self.discord:
                self.rpc.update(
                    details=f"Playing v{requests.get('https://benbot.app/api/v1/status').json()['currentFortniteVersion'].replace('++Fortnite+Release-', '').split('-')[0]}",
                    state="Generating new cosmetics",
                    large_image="app_image",
                    large_text="Cosmetic Generator",
                    small_text="User access",
                    start=int(self.start),
                    small_image="user_access",
                    buttons=[{"label": "Download", "url": "https://github.com/djlorenzouasset/Cosmetics-Generator"}]
                )
            responce = res.json()['data']['items']
            start = time.time()
            count = 1
            datas = []
            for data in responce:
                percentage = (count/len(responce)) * 100
                datas.append(BaseIcon().main(data))
                print(Fore.BLUE + f"Generated image for {data['id']} -" + Fore.YELLOW + f" {count}/{len(responce)} - {round(percentage)}%")
                count += 1
            print(Fore.BLUE + "Merging images...")
                    
            row_n = len(datas)
            rowslen = ceil(sqrt(row_n))
            columnslen = round(sqrt(row_n))

            mode = "RGB"
            px = 512
            rows = rowslen * px
            columns = columnslen * px
            image = Image.new(mode, (rows, columns))
            i = 0
            for card in datas:
                image.paste(
                    card,
                    ((0 + ((i % rowslen) * card.width)),
                    (0 + ((i // rowslen) * card.height)))
                )
                i += 1
            image.save('images/newcosmetics.jpg')
            image.show()
            if self.twitter != False:
                try:
                    self.twitter.update_status_with_media(
                        self.newText,
                        "images/newcosmetics.jpg"
                    )
                except Exception as exception:
                    print(Fore.RED + f"Failed to tweet the newcosmetics image!\n{exception}")
            print(Fore.GREEN + f"Generated in {round(time.time() - start, 2)} seconds")
            shutil.rmtree('cache')
            os.makedirs('cache')
        elif responce['status'] != 200:
            print(Fore.RED + f"[ERROR] The api return a {res['status']} error")


    def SearchCosmetic(self):
        if self.discord:
            self.rpc.update(
                details=f"Playing v{requests.get('https://benbot.app/api/v1/status').json()['currentFortniteVersion'].replace('++Fortnite+Release-', '').split('-')[0]}",
                state="Searching a cosmetic",
                large_image="app_image",
                large_text="Cosmetic Generator",
                small_text="User access",
                start=int(self.start),
                small_image="user_access",
                buttons=[{"label": "Download", "url": "https://github.com/djlorenzouasset/Cosmetics-Generator"}]
            )
        ask = input(Fore.GREEN + 'What cosmetic do you want to grab? ')
        res = requests.get(
            f'https://fortnite-api.com/v2/cosmetics/br/search?name={ask}&language={self.language}&searchLanguage={self.searchlanguage}'
        )
        if res.status_code == 200:
            responce = res.json()['data']
            start = time.time()
            image = BaseIcon().main(responce)
            print(Fore.BLUE + f"Generated image for {responce['id']}")
            print(Fore.GREEN + f"Generated in {round(time.time() - start, 2)} seconds")
            image.show()
        elif res.status_code == 404:
            print(Fore.RED + f"[ERROR] The cosmetic you search doesn't exist")
        else:
            print(Fore.RED + "Api down!")

    def NewsGenerator(self):
        res = requests.get(
            f'https://fortnite-api.com/v2/news/br?language={self.language}'
        )       
        if res.status_code == 200:
            if self.discord:
                self.rpc.update(
                    details=f"Playing v{requests.get('https://benbot.app/api/v1/status').json()['currentFortniteVersion'].replace('++Fortnite+Release-', '').split('-')[0]}",
                    state="Generating news br",
                    large_image="app_image",
                    large_text="Cosmetic Generator",
                    small_text="User access",
                    start=int(self.start),
                    small_image="user_access",
                    buttons=[{"label": "Download", "url": "https://github.com/djlorenzouasset/Cosmetics-Generator"}]
                )
            res = res.json()['data']['motds']
            for data in res:
                NewsImage().generate_image(data)
                print(Fore.BLUE + f"Generated image for {data['title']}")
        elif res.status_code == 404:
            print(Fore.RED + f"[ERROR] No news detected!")  
        else:
            print(Fore.RED + "Api down!")     


    def paksearch(self):
        if self.discord:
            self.rpc.update(
                details=f"Playing v{requests.get('https://benbot.app/api/v1/status').json()['currentFortniteVersion'].replace('++Fortnite+Release-', '').split('-')[0]}",
                state="Searching a pak",
                large_image="app_image",
                large_text="Cosmetic Generator",
                small_text="User access",
                start=int(self.start),
                small_image="user_access",
                buttons=[{"label": "Download", "url": "https://github.com/djlorenzouasset/Cosmetics-Generator"}]
            )    
        ask = input(Fore.GREEN + 'What number pak do you want to grab? ')
        res = requests.get(
            f'https://fortnite-api.com/v2/cosmetics/br/search/all?dynamicPakId={ask}&language={self.language}'
        )    
        if res.status_code == 200:           
            res = res.json()['data']
            start = time.time()
            count = 1
            datas = []
            for data in res:
                percentage = (count/len(res)) * 100
                datas.append(BaseIcon().main(data))
                print(Fore.BLUE + f"Generated image for {data['id']} -" + Fore.YELLOW + f" {count}/{len(res)} - {round(percentage)}%")
                count += 1
            
            print(Fore.BLUE + "Merging images...")
                    
            row_n = len(datas)
            rowslen = ceil(sqrt(row_n))
            columnslen = round(sqrt(row_n))

            mode = "RGB"
            px = 512
            rows = rowslen * px
            columns = columnslen * px
            image = Image.new(mode, (rows, columns))
            i = 0
            for card in datas:
                image.paste(
                    card,
                    ((0 + ((i % rowslen) * card.width)),
                    (0 + ((i // rowslen) * card.height)))
                )
                i += 1
            image.save(f'images/pak {ask}.jpg')
            image.show()
            if self.twitter != False:
                try:
                    self.twitter.update_status_with_media(
                        self.pakText,
                        f"images/pak {ask}.jpg"
                    )
                except Exception as exception:
                    print(Fore.RED + f"Failed to tweet the pak image!\n{exception}")
            print(Fore.GREEN + f"Generated in {round(time.time() - start, 2)} seconds")
            shutil.rmtree('cache')
            os.makedirs('cache')
        elif res.status_code != 200:
            print(Fore.RED + f"[ERROR] The api return a {res.status_code} error")

    
    def merge(self):
        if self.discord:
            self.rpc.update(
                details=f"Playing v{requests.get('https://benbot.app/api/v1/status').json()['currentFortniteVersion'].replace('++Fortnite+Release-', '').split('-')[0]}",
                state="Merging images",
                large_image="app_image",
                large_text="Cosmetic Generator",
                small_text="User access",
                start=int(self.start),
                small_image="user_access",
                buttons=[{"label": "Download", "url": "https://github.com/djlorenzouasset/Cosmetics-Generator"}]
            )
        print(Fore.BLUE + "Merging images..")
        datas = [Image.open(i) for i in glob.glob(f'cache/*.png')]
                
        row_n = len(datas)
        rowslen = ceil(sqrt(row_n))
        columnslen = round(sqrt(row_n))

        mode = "RGB"
        px = 512
        rows = rowslen * px
        columns = columnslen * px
        image = Image.new(mode, (rows, columns))
        i = 0
        for card in datas:
            image.paste(
                card,
                ((0 + ((i % rowslen) * card.width)),
                (0 + ((i // rowslen) * card.height)))
            )
            i += 1
        image.save('images/merge.jpg')
        image.show()
        os.makedirs('cache')

    def set(self):
        ask = input(Fore.GREEN + "What set you want to grab? ")
        resp = requests.get(
            f'https://fortnite-api.com/v2/cosmetics/br/search/all?set={ask}&language={self.language}&searchLanguage={self.searchlanguage}'
        )

        if resp.status_code == 200:
            if self.discord:
                self.rpc.update(
                    details=f"Playing v{requests.get('https://benbot.app/api/v1/status').json()['currentFortniteVersion'].replace('++Fortnite+Release-', '').split('-')[0]}",
                    state="Searching sets",
                    large_image="app_image",
                    large_text="Cosmetic Generator",
                    small_text="User access",
                    start=int(self.start),
                    small_image="user_access",
                    buttons=[{"label": "Download", "url": "https://github.com/djlorenzouasset/Cosmetics-Generator"}]
                )
            res = resp.json()['data']
            count = 1
            datas = []
            for data in res:
                percentage = (count/len(res)) * 100
                datas.append(BaseIcon().main(data))
                print(Fore.BLUE + f"Generated image for {data['id']} -" + Fore.YELLOW + f" {count}/{len(res)} - {round(percentage)}%")
                count += 1
            print(Fore.BLUE + "Merging images...")
                    
            row_n = len(datas)
            rowslen = ceil(sqrt(row_n))
            columnslen = round(sqrt(row_n))

            mode = "RGB"
            px = 512
            rows = rowslen * px
            columns = columnslen * px
            image = Image.new(mode, (rows, columns))
            i = 0
            for card in datas:
                image.paste(
                    card,
                    ((0 + ((i % rowslen) * card.width)),
                    (0 + ((i // rowslen) * card.height)))
                )
                i += 1
            image.save(f'images/{ask}.jpg')
            image.show()
            shutil.rmtree('cache')
            os.makedirs('cache')
        elif resp.status_code == 404:
            print(Fore.RED + f"[ERROR] The cosmetic you search doesn't exist")
        else:
            print(Fore.RED + "Api down!")
