========================
Bilgi Sayfam Projesi
========================

BilgiSayfam.com adresinin açık kaynak kodu bu git reposunda bulunmaktadır. Temel olarak Django ve arkadaşları (PostgreSQL, Redis, vs.) ve önyüz için de AngularJS kullanılmıştır. 

Proje yapısında [Two Scoops of Django](https://django.2scoops.org/) kitabı örnek alınmıştır, bu vesileyle bu harika kitabı önermekteyim.


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

    $ sudo -u postgres createuser --superuser $USER
    $ sudo -u postgres psql
    postgres=# create database bilgisayfam;

Bu adımlardan sonra sistem kullanıcı adınızla aynı bir veritabanı kullanıcınız yaratılmış olacak ve yarattığınız bilgisayfam veritabanına şifresiz bağlanabilecektir (`pg_hba.conf` dosyasında "ident" olduğu sürece). Django settings dosyalarında başka bir değişiklik yapmanıza gerek yoktur.

Siteyi canlıda çalıştırmayı düşünüyorsanız gerekli olan `SECRET_KEY` değerini değiştirmenizi öneririm. Zaten canlı için olan settings/production.py dosyasında bu değer ortam değişkeni olarak alınmakta, yoksa hata vermektedir. Örnek olarak virtualenv içerisindeki bin/postactivate dosyasına aşağıdaki kod parçası ile yarattığınız değeri ekleyebilirsiniz:

    $ python -c "chars = 'abcdefghijklmnopqrstuvwxyz0123456789\!@#\$%^&*(-_=+)'; from django.utils.crypto import get_random_string; print get_random_string(50, chars);"
