# FİNAL PROJESİ

**Proje Adı:** Cyber Gate CRM (Müşteri Takip ve Atama Uygulaması)
**Proje Türü:** Final Ödevi
**Geliştirici:** Oğuz Kağan ALTUNBAŞ
**Öğrenci Numarası:** 25380102005

---

## 1. Projenin Amacı ve Ne İşe Yaradığı
Cyber Gate CRM, operasyonel müşteri süreçlerini dijitalleştirmek, veri bütünlüğünü güvence altına almak ve ekip içi hiyerarşiyi (Kurucu, Yönetici, Arayıcı) güvenli bir şekilde yönetmek amacıyla geliştirilmiş yüksek performanslı bir Müşteri İlişkileri Yönetimi platformudur. Bu sistem, sadece temel veri okuma/yazma (CRUD) işlemleri yapan standart bir uygulamanın ötesine geçerek; dinamik sayfalandırma, anlık istatistik takibi, görüşme durumu loglama ve çok katmanlı yetkilendirme (RBAC) özellikleriyle satış ve destek ekipleri için merkezi bir "Komuta Merkezi" (Command Center) işlevi görmektedir.

## 2. Mimari Özet - Klasör Yapısı ve Ana Akışlar
Proje, Flask'ın "Application Factory" (Uygulama Fabrikası) deseni ve "Blueprint" mimarisi kullanılarak modüler bir yapıda inşa edilmiştir. Veri katmanında SQLAlchemy 2.x ORM yapısı, arayüz katmanında ise Jinja2, Tailwind CSS (Dark Tech teması) ve Alpine.js kullanılmıştır. 

**Klasör Yapısı:**
```text
cybergate-crm/
├── app/
│   ├── __init__.py          # Application Factory ve eklenti (db, login) tanımları
│   ├── main/                # Ana ekran (Hub), ayarlar ve admin paneli blueprint'i
│   ├── auth/                # Kimlik doğrulama, kayıt ve çıkış blueprint'i
│   ├── crm/                 # Müşteri yönetimi, listeleme ve sayfalandırma blueprint'i
│   ├── models.py            # User ve Customer veritabanı modelleri
│   └── templates/           # Şablon hiyerarşisi (base.html ve alt sayfalar)
├── migrations/              # Flask-Migrate veritabanı göç dosyaları
├── docs/                    # Rapor, AI günlüğü, img, plans 
├── config.py                # Ortam değişkenleri ve veritabanı ayarları
├── requirements.txt         # Proje bağımlılıkları
└── run.py                   # Uygulama başlatıcı
```
**Ana Akışlar (Diyagram Özeti):**
Kullanıcı sisteme giriş yaptığında (auth.login), rolüne göre yetkilendirilir. Eğer yetkisi yeterliyse main.index (Hub) üzerinden gerçek zamanlı aktif müşteri sayısını görüntüler. crm.dashboard rotasında dinamik URL parametreleriyle (Örn: ?per_page=20&page=2) Müşteri tablosunu yönetir. Kritik işlemlerde (örn. kullanıcı silme) sistem target_user.role kontrolü yapar ve işlemi başlatan yöneticiden şifre doğrulaması (MFA) ister.

**3. Vibe Coding Deneyimi:**
Ne işe yaradı: Projenin iskeletini kurmak, Tailwind CSS ile karmaşık ve şık arayüzler (Glassmorphism, karanlık tema) tasarlamak ve SQLAlchemy modelleri arasındaki temel ilişkileri (One-to-Many) kurmak çok hızlı ve verimli oldu. Ajan, benim doğal dildeki niyetimi hızlıca teknik bir şablona dönüştürebildi.
Nerede zorlandım: Ajan, projenin büyüyen bağlamını (context) bazen gözden kaçırdı. Özellikle veritabanına yeni bir Foreign Key eklediğimizde veya yetki hiyerarşisine yeni bir rol (super_admin) tanımladığımızda, eski kod bloklarındaki katı koşulları (strict checks) kendi kendine güncellemeyi akıl edemedi. Bu noktalarda ajana inisiyatif bırakmak yerine, sorunun kaynağını tespit edip spesifik komutlarla (örneğin "eski şablonlardaki koşulları in ['admin', 'super_admin'] olarak güncelle" diyerek) doğrudan müdahale etmem gerekti.

**4. Antigravity'de En Faydalı Bulduğum 2 Özellik ve Neden**
Plan Modu (Plan Mode): En kritik özellikti. Özellikle veritabanı ilişkileri (modeller) ve hiyerarşik silme mekanizması gibi riskli görevlerde, ajanın koda dokunmadan önce bana ne yapacağını adım adım İngilizce/Türkçe açıklaması, mimari hataları kod yazılmadan önce yakalamamı sağladı. SQLAlchemy 1.x tarzı eski kod yazmasını bu sayede erkenden engelledim.

Manager View (Yönetici Görünümü): Büyük çaplı özelliklerin (Örn: Sisteme görüşme durumunu kaydedecek call_status rozetlerinin baştan uca; model, route ve template olarak entegre edilmesi) planlanmasında çok işlevseldi. Birbirine bağlı 4-5 dosyanın aynı anda senkronize bir şekilde düzenlenmesi sürecini harika yönetti.

**5. Ajanın Yakalayıp Düzelttiğiniz En Kritik 3 Hatası**
Geliştirme sürecinde ajanın yaptığı ve tarafımca analiz edilerek (hata ayıklama ile) çözülen 3 kritik hata şunlardır:

Multiple Foreign Key Çatışması: Customer modeline hem assigned_user_id hem de last_called_by_id olmak üzere iki farklı kullanıcı bağlantısı eklediğimde, ajan User.customers ilişkisinde hangi anahtarı kullanacağını belirtmeyi unuttu. Bu durum InvalidRequestError hatasına yol açtı. Ajana yönlendirme yaparak foreign_keys="Customer.assigned_user_id" parametresini modele manuel olarak eklettim.

Sessiz Form Hatası (Eksik CSRF Token): Ajan, yeni kayıt (Register) sayfasının HTML şablonunu oluştururken {{ form.hidden_tag() }} CSRF token'ını şablona render etmeyi unuttu. Form POST edildiğinde terminalde HTTP 200 dönmesine rağmen kayıt başarısız oluyordu. Terminal loglarını inceleyerek hatayı tespit ettim ve ajana şablonu düzelttirdim.

RBAC Lockout (Yetki Kilidi): Sisteme "Kurucu" (super_admin) rolünü ekleyip kendi rolümü veritabanından güncellediğimde, ajan projedeki eski rotalarda yer alan current_user.role == 'admin' katı eşleşmelerini değiştirmeyi unuttuğu için kendi panellerimden dışlandım. Ajana "Yetki Yayılımı" promptu vererek tüm sistemdeki kontrolleri in ['admin', 'super_admin'] olarak güncelletip sistemi kurtardım.

**6. Projeyi Sıfırdan AI Olmadan Yapsaydım Ne Kadar Sürerdi?**
Güncel python bilgimi göz önünde bulundurursak bu çapta bir projeyi geliştirmek haftalarımı alırdı. Bilmediğim pek çok kütüphaneyi ve altyapı sistemlerini projeyi geliştirme sürecinde aynı anda öğrenmeye çalışmak büyük bir iş yükü ve vakit kaybı oluşmasına sebep olurdu.

**7. Bu Projeyi Sürdürürsem Bir Sonraki Adım Ne Olur?**
Öncelikle kullanıcı deneyimini artıtacak eklemeleri entegre ederdim. Şuanki haliyle de oldukça son kullanıcı dostu bir uygulama olsa bile ufak düzenleme ve eklentilerle bu deneyimi daha üst bir seviyeye çıkarmaya odaklanırdım. Müşteri Yönetim modülünü ve kullanıcı arayüzünü en iyi haline getirdikten sonra bu sefer diğer modülleri geliştirme aşamasına geçerdim. Genel olarak uygulamayı işlevsel bir şirket portalına çevirdikten sonra mobile tam uyum sağlayacak şekilde geliştirdikten sonra uygulamayı yayınlama aşamasına geçerdim.
