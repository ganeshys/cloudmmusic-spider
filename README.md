# cloudmmusic-spider
网易云音乐歌词爬虫。。。专门爬取hiphop版本，并作词频分析。。。jieba

## 此次爬虫一共爬取511rap歌手的所有歌曲，下图是hiphop歌手的词频。。 

![Image text](https://github.com/ganeshys/cloudmmusic-spider/blob/master/%E7%88%AC%E5%8F%96%E7%9A%84%E6%AD%8C%E8%AF%8D%E7%9A%84%E6%88%AA%E5%9B%BE.jpg)

之前参考的一些文章，有个关于artists的崩了(http://music.163.com/api/artist/{id}），所以我们不能很舒服的从这个api中获得歌手人们歌曲的值

要换个新思路来解决问题，先从一个大歌单中获得各个艺人的id，在通过艺人的id进入艺人的界面，拿到艺人人们歌曲的songid,通过songid去访问各个界面，最后拿到我们想要的歌词。

当然频繁的请求api接口，会返回503.。。

这是需要设置随机时间并设置相应代理ip或者随机UserAgent，，，当然啦我这里都没写。。。哈哈哈哈
