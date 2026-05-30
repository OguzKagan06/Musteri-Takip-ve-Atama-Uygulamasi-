# Tam Çalışan Güvenli Kimlik Doğrulama Akışı (Auth Flow) Planı

Bu plan, istenen kayıt olma (register) ile giriş/çıkış (login/logout) akışının Flask-Login ve Flask-WTF kullanılarak projeye entegre edilmesini açıklar.

## User Review Required

Aşağıdaki planlanan tasarımları, özellikle `base.html` üzerindeki navbar yerleşimini ve formların yapısını inceleyin. Eğer her şey tamamsa onayınız ile uygulamaya geçeceğim. 

## Proposed Changes

### 1. Flask-Login Yapılandırması ve Modeller

#### [MODIFY] app/__init__.py
*   `flask_login` modülünden `LoginManager` içeri aktarılacak.
*   `login_manager = LoginManager()` nesnesi oluşturulup, `create_app()` içinde `login_manager.init_app(app)` ile başlatılacak.
*   `login_manager.login_view = 'auth.login'` olarak ayarlanıp yetkisiz giriş denemelerinde `/login` sayfasına yönlendirme yapılacak.
*   `login_manager.login_message = "Lütfen bu sayfaya erişmek için giriş yapın."` gibi Türkçe bir yönlendirme mesajı ayarlanacak.

#### [MODIFY] app/models.py
*   `flask_login` kütüphanesinden `UserMixin` dahil edilecek ve `User` sınıfı `(UserMixin, db.Model)` şeklinde çoklu kalıtım alacak.
*   `from app import login_manager` import edilip, dosyanın sonuna `user_loader` fonksiyonu eklenecek:
    ```python
    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    ```

---

### 2. Formlar (Flask-WTF)

#### [MODIFY] app/auth/forms.py
*   `LoginForm` oluşturulacak: `username` ve `password` alanlarına sahip. `DataRequired()` validatorleri olacak.
*   `RegisterForm` oluşturulacak: `username`, `password`, `confirm_password` alanlarına sahip. `EqualTo` validator'ü eklenecek.
*   Kullanıcı adının daha önce alınıp alınmadığını kontrol etmek için `RegisterForm` içerisinde SQLAlchemy 2.x stiline uygun (db.session.scalar ve db.select ile) özel bir `validate_username` fonksiyonu tanımlanacak.

---

### 3. Rotalar (Routes)

#### [MODIFY] app/auth/routes.py
*   `/login`: Eğer kullanıcı zaten giriş yapmışsa (`current_user.is_authenticated`), anasayfaya (`main.index`) yönlendirilecek. Değilse `LoginForm` oluşturulacak ve doğrulama başarılı ise kullanıcı giriş yaptırılıp `flash` ile Türkçe başarılı mesajı basılacak. Hatalıysa tekrar giriş sayfasına hata mesajı ile yönlendirilecek.
*   `/register`: Eğer kullanıcı giriş yapmışsa anasayfaya yönlendirilecek. `RegisterForm` başarılı bir şekilde submit edilirse, şifre `set_password` ile hashlenecek, DB'ye kaydedilecek ve login sayfasına `flash` mesajı ile yönlendirilecek.
*   `/logout`: `logout_user()` fonksiyonu çağrılıp çıkış yapılacak ve Türkçe `flash` mesajı basılarak anasayfaya yönlendirilecek.

---

### 4. Görüntüler ve Tasarım (Templates)

#### [MODIFY] app/templates/base.html
*   Sayfanın en üstüne Bootstrap 5 Navbar eklenecek.
*   Navbar içinde `{% if current_user.is_authenticated %}` koşulu kurularak giriş yapmışlara "Çıkış Yap", yapmamışlara "Giriş Yap / Kayıt Ol" linkleri sunulacak.
*   Container divinin hemen içine Bootstrap 5 Alert yapılarıyla (dismissible) Flash mesajlarının görüntülenmesini sağlayan `get_flashed_messages()` bloğu eklenecek.

#### [NEW] app/templates/auth/login.html
*   Bootstrap 5'in modern card (kart) bileşeni kullanılarak, form ortalanmış ve mobil uyumlu bir şekilde sunulacak.
*   CSRF koruması için `{{ form.hidden_tag() }}` kullanılacak. Formdaki alanlar Jinja tagları (`form.username(class="form-control")` vs) ile entegre edilecek.
*   Hatalı validasyon durumları için (validator hataları) form alanlarının altında kırmızı uyarı metinleri eklenecek.

#### [NEW] app/templates/auth/register.html
*   `login.html` ile aynı Bootstrap 5 tasarım prensiplerini taşıyacak.
*   CSRF koruması sağlanıp `username`, `password` ve `confirm_password` inputları Jinja üzerinden basılacak.

## Verification Plan
*   Bu planı onayladıktan sonra dosyalar tek tek güncellenecektir.
*   Syntax ve circular import hatası olmaması için dosya içindeki importların sıralarına dikkat edilecektir.
*   Tamamlandıktan sonra yeni formları test edebileceksiniz.
