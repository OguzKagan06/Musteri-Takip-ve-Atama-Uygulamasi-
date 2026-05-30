## Oturum 1 [30/05/2026]
### Hedef
Proje konusunun belirlenmesi, mimarinin çıkarılması ve Antigravity üzerinde temel Flask 3.x uygulama iskeletinin oluşturulması.

### Kullandığım Model
Model: Gemini 3 Pro

### Verdiğim Promptlar
1. Proje iskeletini oluşturma promptu 

"Bağlam: Meslek Yüksek Okulu öğrencisiyim, İnternet Programcılığı final projesi için Flask 3.x ile modüler bir CRM (Müşteri Takip ve Atama) uygulaması geliştireceğim. Sistemde yetkililer (Admin) ve arayıcılar (Kullanıcı) olacak. Yetkililer müşteri ekleyip atama yapabilecek, arayıcılar ise sadece kendilerine atanan müşterileri filtreleyip not bırakabilecek.

Hedef: Application factory pattern (Uygulama fabrikası) kullanan, blueprint'lere ayrılmış, temiz bir proje iskeleti kur. Klasör yapısı şu şekilde olmalı:
app/
  __init__.py
  main/
    __init__.py
    routes.py
  auth/
    __init__.py
    routes.py
    forms.py
  crm/
    __init__.py
    routes.py
    forms.py
  models.py
  templates/
    base.html
    main/
      dashboard.html
    auth/
      login.html
    crm/
      customer_list.html
  static/
  migrations/
  tests/
config.py
requirements.txt
.env.example
.gitignore
run.py

Kısıtlar:
1. Flask 3.x sürümünü temel al.
2. Sadece şu paketleri requirements.txt dosyasına ekle: flask, flask-sqlalchemy, flask-migrate, flask-login, flask-wtf, python-dotenv. (Excel/CSV işlemleri için harici paket ekleme, Python'ın gömülü 'csv' modülünü kullanacağız).
3. Henüz hiçbir veritabanı modeli, detaylı route veya template içeriği yazma. Sadece klasörleri ve boş/iskelet __init__.py ile config dosyalarını oluştur.
4. Arayüz modüler (Stitch bileşen mantığında) olacak ancak dökümandaki rubrik gereği temel CSS çatısı olarak Bootstrap 5 import edilecek.
5. .env dosyasını .gitignore içerisine ekle.
6. Plan modunda ilerle. Önce yapacağın adımları ve planı göster, ben onayladıktan sonra dosyaları oluşturmaya başla."

### Ajanın Önerdiği Plan
Ajan, application factory pattern ve blueprint yapısına uygun, Flask 3.x ve Bootstrap 5 gereksinimlerini karşılayan detaylı bir klasör/dosya planı sundu.

### Plan'da Sorguladıklarım
Plan beklentilerimi tam olarak karşıladığı ve gereksiz hiçbir harici paket (örneğin excel okumak için pandas vs.) eklemediği için doğrudan onay verdim.

### Karşılaştığım Hatalar ve Çözümler
- Herhangi bir hata ile karşılaşılmadı. Arayüz güncellendiği için fiziksel bir "Plan" butonu bulamadım, ancak prompt mühendisliği ile ajana doğrudan 'Plan modunda ilerle ve onayımı bekle' komutunu vererek dökümandaki kuralı uyguladım.

### Bu Oturumdan Öğrendiğim
Vibe coding sürecinde ajana bağlamı (context) ve kısıtları (constraints) net verdiğimizde, ajanın mimari kararları bizim yerimize en uygun şekilde, hatasız alabildiğini gördüm.

## Oturum 2 [30/05/2026]
"Her promptta aynı şeyleri tekrar etmemek ve ajanın tipik hatalar yapmasını önlemek adına, Antigravity'nin Workspace Rules özelliğini kullanarak projenin teknik kısıtlarını (SQLAlchemy 2.x kullanımı, şifre hashleme zorunluluğu) sisteme global kural olarak tanımladım." ![Agent Rules](docs/img/Agent-Rules.png)

### Karşılaştığım Hatalar ve Çözümler
- **Hata:** Terminalde `flask db init` komutunu çalıştırdığımda `Error: No such command 'db'` hatası aldım.
- **Çözüm:** Hatanın nedenini analiz ettiğimde, iskelet kurulumunda `app/__init__.py` dosyasının boş bırakıldığını ve Flask-Migrate eklentisinin uygulamaya tanıtılmadığını fark ettim. Ajana, `config.py` içine veritabanı URI'sini eklemesi ve `__init__.py` içinde `db.init_app(app)` ile `migrate.init_app(app, db)` yapılandırmalarını kurması için yeni bir görev (prompt) verdim. Ayrıca `.env` dosyasında `FLASK_APP=run.py` tanımlamasını yaparak Flask'a uygulamanın giriş yolunu gösterdim. Düzeltmelerden sonra migrasyon komutları sorunsuz çalıştı.

## Oturum 3 [30/05/2026]
### Hedef
Kullanıcıların sisteme güvenle kayıt olabilmesi ve giriş yapabilmesi için Flask-Login ve Flask-WTF kullanarak Auth akışının kurulması.

### Verdiğim Promptlar
1. Bağlam: Veritabanı modelleri hazır, app/auth/ blueprint'i kuruldu ancak içi boş.

Hedef: Tam çalışan güvenli bir kayıt (register) ile giriş/çıkış (login/logout) akışı kur.

Adımlar:
1. app/models.py: `User` modeline Flask-Login'in `UserMixin` sınıfını kalıtım olarak ekle. Ayrıca `user_loader` fonksiyonunu yaz.
2. app/auth/forms.py: `RegisterForm` ve `LoginForm` oluştur. (Flask-WTF ve gerekli validator'ler dahil edilsin).
3. app/auth/routes.py: `/register`, `/login`, `/logout` rotalarını yaz.
4. app/templates/auth/register.html ve login.html: Bu sayfaları Bootstrap 5 kullanarak, mobil uyumlu ve temiz bir tasarımla oluştur. Form elemanlarını Jinja ile render et.
5. app/__init__.py: Flask-Login'i yapılandır (login_manager nesnesini oluştur, init_app ile bağla ve login_view = 'auth.login' olarak ayarla).
6. app/templates/base.html: Navbar (üst menü) kısmına kullanıcı giriş yapmamışsa "Giriş Yap" / "Kayıt Ol", giriş yapmışsa "Çıkış Yap" bağlantılarını koşullu (if current_user.is_authenticated) olarak ekle.

Kısıtlar:
- Kayıt (Register) ekranında 'username'in daha önce alınıp alınmadığını veritabanından kontrol et (Custom validator).
- Kullanıcı zaten giriş yapmışsa ve /login veya /register sayfasına girmeye çalışırsa anasayfaya yönlendir.
- Başarılı/başarısız girişler için flash() mesajlarını tamamen Türkçe kullan.
- CSRF korumasını asla atlama (form.hidden_tag() kullan).
- Plan modunda ilerle. Önce değiştireceğin/oluşturacağın dosyaların planını göster, onayımı bekle.

### Ajanın Önerdiği Plan
Ajan, `UserMixin` kalıtımını, `User_loader` fonksiyonunu ve CSRF korumalı formları içeren detaylı bir plan sundu. Formlarda Bootstrap 5 kullanmayı planladı. [Kayıt Sayfası](docs/img/kayıt-sayfası.png)

### Plan'da Sorguladıklarım
Plan, projenin güvenlik kısıtlarını (şifre hashleme, eşsiz kullanıcı adı kontrolü, CSRF) ve UI kısıtlarını (Türkçe flash mesajları) tam olarak karşıladığı için doğrudan onay verdim.

### Bu Oturumdan Öğrendiğim
Kimlik doğrulama gibi karmaşık ve birden fazla dosyaya dokunan (models, routes, forms, templates, init) görevlerde, ajana adım adım hangi dosyalara ne eklemesi gerektiğini söylemek, sürecin hatasız ve tek seferde tamamlanmasını sağlıyor.

### Karşılaştığım Hatalar ve Çözümler
- **Hata 1:** Kayıt formunu doldurup gönderdiğimde `OperationalError: no such table: users` hatası ile karşılaştım. [Kayıt Hatası](docs/img/kayıt-hatası.png)
- **Çözüm 1:** Sorunun, tabloları fiziksel olarak yaratan `flask db upgrade` komutunun eksik kalmasından kaynaklandığını tespit ettim.
- **Hata 2:** `flask db upgrade` komutunu çalıştırdığımda bu kez `ImportError: Can't find Python file migrations\env.py` hatası aldım.
- **Çözüm 2:** Ajanın ilk iskelet kurulumunda oluşturduğu boş `migrations` klasörünün Flask-Migrate altyapısını bozduğunu fark ettim. Manuel olarak bu boş klasörü sildim ve `flask db init`, `migrate`, `upgrade` komutlarını sıfırdan, temiz bir şekilde çalıştırarak tabloları başarıyla oluşturdum.
[migrates](docs/img/migrates.png)

## Oturum 4 [30/05/2026]
### Hedef
Uygulamanın ana işlevi olan CRM (Müşteri ve Not Yönetimi) modülünün oluşturulması ve sisteme Rol Bazlı Yetkilendirme (RBAC - Admin/Arayıcı) güvenlik katmanının entegre edilmesi.

### Verdiğim Promptlar
1. Bağlam: Auth altyapımız çalışıyor ancak sisteme yetkilendirme (RBAC) ve asıl işlevimiz olan CRM modülünü eklememiz gerekiyor. app/crm/ blueprint'ini dolduracak ve app/auth/ tarafını güvenli hale getireceğiz.

Hedef: Sadece adminlerin yeni kullanıcı açabildiği, müşterilerin atanabildiği ve arayıcıların sadece kendi müşterilerine not düşebildiği güvenli bir CRM paneli oluştur.

Adımlar:
1. İlk Admini Oluşturmak (CLI): app/__init__.py veya app/cli.py içine `flask create-admin` adında bir CLI komutu yaz. Bu komut çalıştırıldığında veritabanına username='admin', password='123', role='admin' olan bir yetkili eklesin.
2. app/auth/routes.py (Güvenlik): `/register` rotasını sadece giriş yapmış ve `current_user.role == 'admin'` olan kullanıcıların erişebileceği şekilde kısıtla. Başkası denerse yetki hatası (flash) verip anasayfaya yönlendir.
3. app/crm/forms.py:
   - `CustomerForm`: Müşteri eklemek/düzenlemek için oluştur. İçine `assigned_user_id` adında bir `SelectField` ekle (Seçenekleri veritabanındaki arayıcılardan dinamik olarak almalı).
   - `NoteForm`: Görüşme notu eklemek için oluştur.
4. app/crm/routes.py (CRM Rotaları - Hepsi @login_required olmalı):
   - `/dashboard`: Adminler *tüm* müşterileri listelesin, arayıcılar sadece *kendilerine atanan* müşterileri listelesin.
   - `/customer/new`: Müşteri ekleme rotası. Eğer ekleyen `admin` ise formdaki `assigned_user_id` değerini baz al. Eğer ekleyen `arayıcı` ise formdaki atamayı yoksay ve müşteriyi mecburi olarak `current_user.id`'ye ata.
   - `/customer/<int:id>`: Müşteri detay ve not ekleme sayfası. Eğer bir arayıcı başkasının müşterisine girmeye çalışırsa (`customer.assigned_user_id != current_user.id` ve rolü admin değilse) erişimi engelle. Bu sayfada `NoteForm` ile müşteriye not eklenebilsin.
5. app/templates/: Bootstrap 5 ile `dashboard.html`, `add_customer.html` ve `customer_detail.html` oluştur. Navbar'ı (base.html) güncelle: "Kayıt Ol" linkini sadece adminler görebilsin, herkes "Dashboard" linkini görebilsin.

Kısıtlar:
- Veritabanı sorgularında kesinlikle SQLAlchemy 2.x stilini kullan (Örn: `db.session.scalars(db.select(User)).all()`).
- Formlarda CSRF (hidden_tag) kullan. Tüm UI ve Flash mesajları Türkçe olsun.
- Plan modunda ilerle ve onayımı bekle.

### Ajanın Önerdiği Plan
Ajan, sistemdeki mantıksal açığı (herkesin kayıt olabilmesi) kapatmak için CLI üzerinden ilk admini oluşturacak bir komut (`flask create-admin`) tasarladı. `CustomerForm` içerisine sadece adminlerin görebileceği dinamik bir "Atanacak Arayıcı" (`SelectField`) alanı ekledi ve yetki kısıtlamalarını (`current_user.role == 'admin'`) içeren güvenli bir CRM rota planı sundu.

### Plan'da Sorguladıklarım
Sıradan arayıcıların başkalarına müşteri atamasını engellemek için arka planda zorunlu olarak `customer.assigned_user_id = current_user.id` atamasının yapılması mantığını inceledim ve kurumsal işleyişe tam uygun bulduğum için onayladım.

### Bu Oturumdan Öğrendiğim
Yazılım mimarisinde "business logic" (iş mantığı) açıklarını -örneğin herkesin kendine hesap açabilmesi gibi- erkenden fark edip sistemi ona göre kısıtlamanın (RBAC) uygulamanın güvenliği için ne kadar hayati olduğunu kavradım. Ayrıca veritabanına doğrudan müdahale etmem gerektiğinde `flask shell` kullanımının hayat kurtarıcı bir araç olduğunu deneyimledim.

### Karşılaştığım Hatalar ve Çözümler
- **Hata:** Sisteme kendi oluşturduğum "admin" hesabımla girmeme rağmen, Müşteri Ekleme sayfasında "Atanacak Arayıcı" alanını göremedim ve arayüzde yetkisiz kullanıcı gibi sınırlandırıldım.
- **Çözüm:** Sorunu analiz ettiğimde, RBAC (Yetkilendirme) sistemini kurmadan önceki aşamada oluşturduğum bu "admin" kullanıcısının, veritabanına varsayılan olarak "arayıcı" rolüyle kaydedildiğini fark ettim. Terminalden `flask shell` komutunu başlatarak SQLAlchemy üzerinden bu kullanıcının profilini çektim (`db.session.scalar`) ve rolünü doğrudan `'admin'` olarak güncelleyip veritabanına işleyerek (`db.session.commit()`) yetkilendirme sorununu çözdüm.