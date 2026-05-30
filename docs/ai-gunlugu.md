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