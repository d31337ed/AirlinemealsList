import requests
from math import ceil


class MyPosts:
    @staticmethod
    def get_all_posts(batch_size, public, token, author_id):
        """Итеративно получаем все посты в паблике.
        Метод возвращает только батчи по 100 штук, поэтому в цикле запрашиваем все"""
        method_way = 'https://api.vk.com/method/wall.get'
        # узнать число постов и сколько будет батчей
        num_of_posts_request = method_way+'?domain='+public+'&access_token='+token+'&v=5.131&count=0'
        total_posts = requests.get(num_of_posts_request).json()['response']['count']
        # итеративно запрашивать и аппендить результат в файл
        for batch_number in range(ceil(total_posts/batch_size)):
            current_shift = batch_number*batch_size
            batch_posts_request = method_way+'?domain='+public+'&access_token='+token+'&v=5.131&count='+str(batch_size)+'&offset='+str(current_shift)
            response = requests.get(batch_posts_request).json()['response']['items']
            print(author_id)
            for item in response:
                if 'signer_id' in item.keys() and item['signer_id'] == author_id:
                    print(item['text'])
                    last_strings = item['text'].split('\n')[-3:]
                    print(last_strings)
                    with open('raw_posts.txt', 'a') as result_file:
                        result_file.write(' '.join(last_strings)+' #Антон_и_БортовоеПитание'+
                                          ' https://vk.com/airlinemeals?w=wall-141742284_'+str(item['id'])+'\n')


with open('access.token', 'r') as file:
    token = file.read()

batch_size = 100
public = 'airlinemeals'
author_id = int(140349039)

MyPosts().get_all_posts(batch_size, public, token, author_id)