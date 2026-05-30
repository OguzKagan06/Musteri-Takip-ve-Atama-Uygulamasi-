---
trigger: always_on
---

1. Daima Flask 3.x ve SQLAlchemy 2.x standartlarını (Mapped, mapped_column) kullan[cite: 117]. Asla db.Column gibi eski 1.x stillerini kullanma.
2. Şifreleri kesinlikle düz metin olarak saklama; daima werkzeug.security ile hashle (generate_password_hash)[cite: 117, 199].
3. Hiçbir API anahtarını veya gizli bilgiyi (SECRET_KEY vb.) koda doğrudan yazma; daima ortam değişkenlerinden (.env) oku[cite: 57, 252].
4. Tüm formlarda Flask-WTF kullanarak CSRF koruması sağla[cite: 30, 117].
5. Kullanıcı arayüzündeki (UI) tüm metinler ve flash mesajları Türkçe olmalıdır[cite: 204].
6. Karmaşık görevlerde (örneğin yeni bir model veya route eklerken) doğrudan kodu dosyaya yazmak yerine, önce bana yapacaklarının bir taslağını (Plan) sun ve onayımı bekle[cite: 74, 101].