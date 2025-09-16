# Link Menuju PWS
https://justin-timothy-footballproject.pbp.cs.ui.ac.id/

## Jawaban atas Pertanyaan
- Cara saya mengimplementasikan step by step,
pertama-tama setting virtual env dulu untuk isolasi dependencies dan mencegah tabrakan versi dan dependensi dengan projek lain. lalu siapkan dependiences yg ingin didownload dan masuk ke venv lalu download. mulai projek dengan startproject. di dalam project ada wsgi,asgi,urls, settings. urls untuk routing level proyek dan settings untuk mengatur banyak hal; mostly saat run server di deployment/production. lalu kita buat aplikasi (main) kalau disimplifikasi mungkin semacam fitur sebutannya, jangan lupa untuk mengaitkan app main di installed_apps di projek. lalu kita rutekan pada urls.py di level proyek untuk  path '' menuju main.urls. Next, di folder main kita rubah file models.py untuk membuat class/ model baru bernama Product. ada category-choices berupa tuple untuk menandakan kategori pilihan. lalu membuat beberapa method untuk return name dan melakukan beberapa perhitungan, buat variable dengan tipe fieldnya, misal name = model.CharField() yang bisa kita passing beberapa argumen. di views.py kita import fungsi render untuk mereturn main.html (yang bisa mengakses variabel dari context berupa dictionary key value di fungsi show_main yg kita buat).

urls.py mengimpor fungsi dari views.py untuk nantinya di eksekusi ketika pengguna menuju path yg didefinisikan di urls.py. lalu add commit dan deploy ke PWS. (Btw saya sempat beberapa kali error, karena SECRET_KEY ku berada di line sebelum production, sehingga SECRET_KEY grebnya dari .env bukan .env.prod)

-![FotoBagan](images/bagankeseluruhan.png). 


- Jadi pertama tama user akan request ke internet, internet akan request ke webserver kita dengan django sebagai backendnya. Lalu akan minta ke urls.py, setelah itu di urls.py, akan dikategorikan berdasarkan urls yang dituju, fungsi manakah dari views.py yang dieksekusi, fungsi show_main misalnya. views ini menjadi business logic layer, menjembatani models dan template, semisal lebih dari sekedar eksekusi html, maka bisa saja mengirim data menuju database atau sesimpel crud operations. anyways dari view bisa read/write data dari models. Jadi, views bisa read/write data tapi yang paling simpelnya itu menerima request http lalu merender main.html, main.html juga bisa mengakses dictionary di views, jadi kalau views greb data dari models lalu dikirm ke diproses dengan forloop di .html lalu dikirim ke user itu sangat memungkinkan.

- Peran settings.py dalam proyek Django itu sangat vital, dimulai dari keamanan, middleware, sampai menjaga env dengan menggunakan dotenv. secara keseluruhan settings itu untuk mengatur jalannya projek django dari keamananan, deployment, production yang meliputi database, timezone, app and extension allowed di app tersebut

- Cara kerja migrasi database di Django adalah: makemigrations untuk membuat berkas migrasi yang berisi perubahan model yang belum ada di basis data, sedangkan migrate adalah untuk mengaplikasikan perubahan yg tercantum di berkas migrasi ke dalam basis data lokal. tanpa dua proses ini maka tidak akan terupdate di database nya.

- Framework django dijadikan permulaan pembelajaran pengembangan perangkat lunak karena sangat mudah dipahami dan easy to read. Secara garis besar jelas sekali yaitu MVT, model view template. Per bagian juga jelas ada urlsnya untuk routing, views untuk menghubungkan model dan template kalau di filenya menghubungkan dengan menerima http respons dan send html. Language menggunakan python, easy dibanding c++. Banyak dokumentasi dan built in yang sudah enak tinggal startapp, startproject.

- Sementara ini belum ada feedback karena asisten dosennya cukup fast respon di grup. Saya sendiri belum bisa menilai banyak karena untuk tutorial cenderung straight forward. Tetapi untuk salah satu asisten dosen yang mengajar di tutorial 0 sangat kompeten menurut saya.


## Jawaban atas Pertanyaan; Tugas 3;
- data delivery secara pengertian adalah cara untuk mengirimkan data antar berbagai bagian dalam arsitektur aplikasi. misal frontend mengambil data ke backend. hal ini penting karena komunikasi menjadi efektif, django orm yang membuka postgre, atau javascript yang meminta data dari django lalu django meminta dari sql. tiga tipe format data yang biasa digunakan dalam fdata delivery adalah html, xml dan json.. hal ini penting karena data delivery memudahkan proses. backend django ini nantinya akan mereturn bukan hanya httpresponse tapi bisa juga jsonresponse. ini sangat penting apalagi ketika nanti dikonek ke api. bahkan nantinya bisa lebih scalability dan memungkinkan adanya ajax.

- json lebih baik untuk banyak usecase. hal ini dikarenakan dibanding xml, json lebih cepat dan ringan, disuppport oleh native js juga karena json sendiri javascriprt object notation, lebih populer di kalangan developer, readable dan biasanya digunakan di rest api. xml biasanya untuk legacy system, atau yang butuh hierarchy, enterprise atau complex schema requirement.

- fungsi dari method is_valid() di Django adalah untuk validasi data form di django. harus sesuai dengan fieldnya, lalu misal panjang character harus berapa, apakah required untuk diisi atau tidak. sebenarnya ini sangat penting karena kalau data dari user gak sesuai dan kita tetap kirim ke database, kemungkinan nanti akan ada invalid datatype dan bahkan sebelum disave itu gabakal kesimpan dengan valid atau kesimpan sama sekali. 

- csrf_token itu dibutuhkan saat membuat form di django untuk mencegah serangan Cross_Site Request Forgery. untuk ngecek bahwa post yang dilakukan ke server itu berasal dari form yang sah dari ketikan kita bukan dari sumber eksternal. Token divalidasi untuk mengecek apakah yang mengirim post request itu pengguna valid atau attacker. 
Jika form kita tidak menyertakan csrf token, maka django bisa menolak dengan respons http 403 forbidden karena tak ada token yang menjamin bahwa kita bukan attacker, lalu jika kita nonaktifkan maka form kita bisa rentan kena csrf dan mengirim sesuatu ke server tanpa sepengetahuan kita mengatasnamakan kita. 
Hal ini dapat dimanfaatkan peyerang. ketika kita telah mempunyai session aktif di dalam django webnya, maka attacker bisa eksekusi script ketika kita install sesuatu atau mengunjungi web mereka, sehingga kita akan secara tanpa sadar mengirimkan post request ke server, bisa membeli sesuatu, atau merubah password, dan hal tersebut akan dianggap tindakan sah oleh server karena dieksekusi oleh browser kita dengan cookie yang valid.

- saya mengimplementasikan checklist diatas seperti ini: pertama yaitu disuruh membuat 4 fungsi views baru untuk melihat objek yang sudah ditambahkan ke database dengan xml,json,json_by_id dan xml_by_id. saya membuat masing masing fungsi, jadi dari model bernama Product saya lakukan grab semua object yang exist dengan Product.objects.all(), lalu saya ubah dengan serializers sesuai data format yang dinginkan dan return httpresponse dengan content_typenya. Kalau show by id maka di filter bukan take all, filter sesuai id dan kalau gak exist, maka return response status 404.
Lalu untuk routingnya saya buat path baru di urls.py misal path json/ eksekusi show_json, kalau json/<str:product_id> itu untuk menjelaskan bahwa product_id akan berupa string dan didalam url kita itu product_id nanti akan disend ke fungsinya. karena ingat fungsinya menerima dua parameter yaitu request dan product_id.

Membuat page yang punya tombol add dan detail product itu cukup simpel juga, kita tambahkan di main.html di halaman utama yaitu elemen elemen html seperti button yang akan referensikan ke fungsi create_product, yaitu yang di urls.py yang kita buat juga, nanti di url tersebut akan dieksekusi fungsi create_product, yang merender create_product.html yaitu sebuah form dengan wajib csrf token, nanti dari situ jika isi formyna valid akan disave dan dikirim ke database. hal ini kita definiskan di fungsi yang ada di views.py. jangan lupa redirect ke menu utama.
untuk bagian yang detail, ingat bahwa di menu utama kita iterasi ke semua product di product_list dan di print semuanya di menu utama. nah, kan ketauan bahwa per row itu ada product yang di print dengan product.thumbnail, product.name, product.featured dsb. salah satunya itu button yang jika dipencet akan mengarah ke app main dan eksekusi show_product, dengan mengirimkan argumen product.id ke si show_product tersebut, sehingga show_product tau harus show product yang mana. sudah deh, di product_item juga memprint per attribute, lalu ada beberapa yang if else juga kalau attribute itu tidak wajib dan required, seperti thumbnail.


- tidak ada feedback, asdos sudah sangat baik dalam penjelasan dan bantuan 

-![FotoPostman](images/postman1.png)

-![FotoPostman](images/postman2.png)

-![FotoPostman](images/postman3.png)

-![FotoPostman](images/postman4.png)