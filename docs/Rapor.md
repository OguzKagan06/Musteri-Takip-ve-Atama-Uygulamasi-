# BİTİRME PROJESİ DEĞERLENDİRME VE MİMARİ RAPORU

**Proje Adı:** Cyber Gate CRM (Müşteri Takip ve Atama Uygulaması)
**Proje Türü:** Final Ödevi
**Geliştirici:** Oğuz Kağan ALTUNBAŞ
**Öğrenci Numarası:** 25380102005

---

## 1. Projenin Amacı ve Kapsamı
Bu proje, operasyonel müşteri süreçlerini dijitalleştirmek, veri güvenliğini sağlamak ve ekip içi hiyerarşiyi yönetmek amacıyla yüksek performanslı bir Müşteri İlişkileri Yönetimi (CRM) platformu olarak tasarlanmıştır. Sistem, modern web standartlarına uygun olarak sıfırdan inşa edilmiş olup, uçtan uca (full-stack) bir web uygulamasının mimari, güvenlik ve veritabanı gereksinimlerini karşılamaktadır.

## 2. Siber Güvenlik ve Hiyerarşik Yetkilendirme (RBAC)
Uygulamanın omurgası, katı güvenlik protokolleri ve Rol Tabanlı Erişim Kontrolü (RBAC) ile güvence altına alınmıştır:
* **Hiyerarşik İzolasyon:** Sistem; Kurucu (Super Admin), Yönetici (Admin) ve Arayıcı (User) olmak üzere üç katmanlı bir yetki yapısına bölünmüştür. Üst düzey yetkililerin (Kurucu), diğer yöneticiler tarafından silinmesi veya manipüle edilmesi kod seviyesinde (Route Protection) engellenmiştir.
* **Kritik İşlem Doğrulaması (MFA Mantığı):** Yetkili hesapların silinmesi işlemi, anlık hataları ve siber riskleri önlemek adına işlemi yapan yöneticinin kendi şifresini doğrulaması kısıtlamasına bağlanmıştır.
* **Form ve Veri Güvenliği:** Tüm POST istekleri ve veri iletim süreçleri CSRF (Cross-Site Request Forgery) token'ları ile korunmuş, form doğrulama süreçleri arka planda loglama mekanizmalarıyla güçlendirilmiştir. Şifreler veritabanında düz metin (plaintext) olarak değil, güvenli hash algoritmalarıyla (Werkzeug Security) saklanmaktadır.

## 3. Veritabanı Bütünlüğü ve Mimarisi
Projenin veri katmanı, Flask-SQLAlchemy (v2.x standartları) kullanılarak ilişkisel veritabanı (RDBMS) mantığıyla kurgulanmıştır.
* **İlişkisel Bütünlük (Referential Integrity):** Sistemden bir kullanıcı silindiğinde, "Sahipsiz Kayıt" (Orphaned Record) hatasını ve uygulamanın çökmesini önlemek amacıyla, o kullanıcıya bağlı olan müşteri kayıtları (Customer) silinmek yerine güvenli bir şekilde anonimleştirilerek (`NULL` ataması yapılarak) veri kaybının önüne geçilmiştir.
* **Çoklu Yabancı Anahtar (Multiple Foreign Key) Yönetimi:** Müşterinin "Sorumlu Arayıcısı" (Assigned User) ile "Son Görüşme Yapan Kişi" (Last Caller) verileri User tablosuna çift yönlü bağlanmış, çakışma (join condition error) olmadan asenkron bir şekilde sorgulanabilir hale getirilmiştir.

## 4. Operasyonel Özellikler ve Dinamik Arayüz (UI/UX)
* **Dinamik Sayfalandırma (Pagination) ve Yönlendirme:** Yoğun veri akışını yönetebilmek için sunucu taraflı (Server-side) sayfalandırma kullanılmış; parametrik URL yapısıyla çalışan dinamik listeleme (5, 10, 20, 50 adet) entegre edilmiştir.
* **Görüşme Durumu Takibi:** Arayıcıların müşteri ile olan temasları (Ulaşıldı, Telefonu Açmadı vb.) kayıt altına alınmakta, işlemi yapan kişinin kimliği Audit Trail (İzleme Kaydı) prensibiyle sisteme işlenmektedir.
* **Kullanıcı Arayüzü:** Tasarım, siber güvenlik vizyonunu yansıtan koyu tema (Dark Tech) ve Glassmorphism prensipleriyle Tailwind CSS ve Alpine.js kullanılarak oluşturulmuştur.

## 5. Sonuç
Geliştirilen bu sistem, sadece veri okuyup yazan temel bir CRUD uygulamasının ötesine geçerek; yetki sınırları net çizilmiş, veritabanı ilişkileri güvenli bir şekilde ayrıştırılmış ve kendi kendini koruyabilen tam teşekküllü bir yazılım ürünü haline getirilmiştir.
