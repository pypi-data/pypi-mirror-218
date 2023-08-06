# Most Popular News CNN Indonesia
This package will get the most popular news in CNN Indonesia

## HOW IT WORK?
This package will scrape from [CNN Indonesia](https://www.cnnindonesia.com/) to get most popular news in CNN Indonesia 

This package uses beatifulsoup4 and requests then produces output in the form of json which can be used in web and mobile applications

'''
if __name__ == '__main__':
    most_popular_news_cnn_id = Mostpopularnewscnn('https://www.cnnindonesia.com/')
    print('Description class news cnn id', most_popular_news_cnn_id.description)
    most_popular_news_cnn_id.run()
'''
