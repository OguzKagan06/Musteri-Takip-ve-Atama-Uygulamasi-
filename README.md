# Cyber Gate CRM

Modern, güvenli ve yüksek performanslı Müşteri İlişkileri Yönetimi (CRM) platformu. Bu proje, operasyonel süreçleri hızlandırmak ve kullanıcı yetkilendirmelerini kurumsal "Enterprise" standartlarda yönetmek amacıyla geliştirilmiştir.

## 🚀 Öne Çıkan Özellikler

* **Rol Tabanlı Erişim Kontrolü (RBAC):** Katı hiyerarşik yetkilendirme mimarisi. (Kurucu > Yönetici > Arayıcı).
* **Güvenli Kullanıcı Yönetimi:** MFA (Şifre doğrulama) mantığıyla çalışan hesap silme mekanizması ve tam veritabanı bütünlüğü (Database Integrity). Silinen kullanıcılara ait kayıtlar otomatik olarak anonimleştirilir (NULL atanır).
* **Dinamik Müşteri Paneli:** Özelleştirilmiş sayfalandırma (Pagination) altyapısı, anlık veri sayımı ve gelişmiş arama/filtreleme özellikleri.
* **Görüşme Durumu Takibi:** Arayıcıların durum (Ulaşıldı, Tekrar Aranacak vb.) ve işlemi yapan kişi bazlı anlık kayıt tutabilme özelliği.
* **Modern Arayüz (UI/UX):** Dark Tech ve Glassmorphism estetiğiyle tasarlanmış, Alpine.js destekli interaktif ve duyarlı (responsive) tasarım.

## 🛠️ Teknoloji Yığını (Tech Stack)

* **Backend:** Python, Flask, SQLAlchemy 2.x
* **Veritabanı:** SQLite (Development) / PostgreSQL (Production)
* **Frontend:** Tailwind CSS, Alpine.js, Jinja2 Temaları
* **Güvenlik:** Flask-WTF (CSRF Koruması), Werkzeug Security (Şifre Hashleme)

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel ortamınızda (Localhost) çalıştırmak için aşağıdaki adımları izleyin:

**1. Repoyu Klonlayın**
```bash
git clone <repo-url>
cd cybergate-crm

python -m venv venv
# Windows için:
venv\Scripts\activate
# MacOS/Linux için:
source venv/bin/activate

pip install -r requirements.txt

flask db init
flask db migrate -m "İlk kurulum"
flask db upgrade

python run.py
