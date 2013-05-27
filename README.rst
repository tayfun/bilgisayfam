========================
Bilgi Sayfam Projesi
========================

BilgiSayfam.com adresinin açık kaynak kodu bu git reposunda bulunmaktadır. Temel olarak Django ve arkadaşları (PostgreSQL, Redis, vs.) ve önyüz için de AngularJS kullanılmıştır. 

Proje yapısında `Two Scoops of Django <https://django.2scoops.org/>`_ kitabı örnek alınmıştır, bu vesileyle bu harika kitabı önermekteyim.




=======
Kurulum
=======

Django paketlerinin ve diğer python kütüphanelerinin kurulumu için:

    $ pip install -r requirements.txt

Not: requirements dosyalarındaki django paketlerinin bir çoğu direkt github'tan kurulan en son sürümler. Bundan dolayı, virtualenv kullanmanız durumunda paket kaynak kodları `~/envs/bilgisayfam/src` dizininde olacaktır.

sitenin çalışması için PostgreSQL gereklidir çünkü PostgreSQL ile gelen bazı özellikler (8.4 ile gelen dizi veri yapısı veya 9.2 ile gelen JSON fonksiyonları gibi) kullanılmaktadır. 

===========
Ayarlamalar
===========

PostgreSQL kurulumunu yaptıktan sonra veritabanı ekleyip gerekli kullanıcıyı yaratmanız gerekmektedir. Eğer veritabanınız web sunucunuz ile aynı makine ise varsayılan olarak "ident sameuser" kullanılacağı için sisteme giriş kullanıcı adınız ile bir superuser yarattığınızda tüm veritabanlarına şifresiz giriş yapabilecektir:

::

    $ sudo -u postgres createuser --superuser $USER  
    $ sudo -u postgres psql  
    postgres=# create database bilgisayfam;  

Bu adımlardan sonra sistem kullanıcı adınızla aynı bir veritabanı kullanıcınız yaratılmış olacak ve yarattığınız bilgisayfam veritabanına şifresiz bağlanabilecektir (`pg_hba.conf` dosyasında "ident" olduğu sürece). Django settings dosyalarında başka bir değişiklik yapmanıza gerek yoktur.

Siteyi canlıda çalıştırmayı düşünüyorsanız gerekli olan `SECRET_KEY` değerini değiştirmenizi öneririm. Zaten canlı için olan settings/production.py dosyasında bu değer ortam değişkeni olarak alınmakta, yoksa hata vermektedir. Örnek olarak virtualenv içerisindeki bin/postactivate dosyasına aşağıdaki kod parçası ile yarattığınız değeri ekleyebilirsiniz:

    $ python -c "chars = 'abcdefghijklmnopqrstuvwxyz0123456789\!@#\$%^&*(-_=+)'; from django.utils.crypto import get_random_string; print get_random_string(50, chars);"


===========
Veritabanı
===========

Sözlüğün ilk sürümlerinde `v0.2 örneğin <https://github.com/tayfun/bilgisayfam/tree/0.2>`_ anlık olarak TDK web sitesine bağlanıp veri çekiliyor ve yerel veritabanına ekleniyordu. Ancak bunun bazı sorunlar çıkardığını gördüm. Öncelikle TDK'nin kararlı çalışmadığını (birkaç kez MySQL bağlantı hatası aldım) ve
bazen çok uzun süre beklettiğini farkettim. Her kelime için sadece bir kez TDK'ye gitsem de bu kabul edilebilir değildi. Tüm veritabanının anında elimde olmamasının bir eksisi de bazı işlemleri hızlı yapamamam oldu (örneğin otomatik tamamlama gibi). 

Bu yüzden `Scrapy <http://doc.scrapy.org/en/latest/index.html>`_ ile tüm veritabanı çekme işine giriştim. Scrapy scriptlerini tdk_crawler dizininde bulabilirsiniz. İki tane örümcek var, bir tanesi ilk olarak kelimeleri çekerken ikincisi anlamları veritabanına ekliyor. Kelime listesini çekmek için:

::

    $ scrapy crawl keyword

Tek bir kelimenin anlamını bulmak için:

::

    $ scrapy crawl meaning -a keyword=kamyon

ve veritabanındaki tüm kelimelerin anlamlarını çekmek için:

::

    $ scrapy crawl meaning

kullanılabilir. Bu komutları tdk_crawler dizininde çalıştırmanız gerekmektedir. Veritabanına yazılırken tdk_crawler/tdk_crawler/settings.py dosyasında yazdığı üzere bilgisayfam django projesindeki scrapy.py dosyasını kullanıyorum. scrapy.py dosyasında bulunan veritabanına veriler yazılacaktır. Veritabanına yazılırken Django ORM'yi kullandığım için PYTHONPATH içerisinde bilgisayfam projesinin de yer aldığına dikkat edin.

=============
Gereklilikler
=============

Gerekliliklerin büyük çoğunluğu requirements dosyalarında bulunmaktadır. Kurulum için:

::

    $ pip install -r requirement.txt

Bazı gereklilikler ise pip ile kurulamamakta. Bunları elinizle kurmalısınız. Örneğin, js ve css dosyalarını sıkıştırmak istiyorsanız yuglify gerekiyor. Bunu npm ile kurabilirsiniz:

::

    $ sudo npm -g install yuglify

========
Katkılar
========

GPL lisansı ile kullandığım sözlük ikonu için `Alessandro Rei <http://kde-look.org/usermanager/search.php?username=mentalrey>`_'ye teşekkürler.
