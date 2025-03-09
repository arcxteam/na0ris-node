# A Completed Guides - Naoris Protocol Run Node DePIN
# 🆘 JNGN BANYAK CINCONG, APALAGI CEPU IRI SIRIK DLL. LU MAU PAKE MAU GK TERSERAH, HILANGKAN RASA PRIMITIF & PKE ROXY MODAL & HARGAI KODE INI ⚠️

![image](https://github.com/user-attachments/assets/4594fa32-8c9e-4e51-9782-319404d2acbd)

## Here We Go...GAS 

**`Is there incentivized?` ![Confirm](https://img.shields.io/badge/confirm-yes-brightgreen)**

> [!IMPORTANT]
> **Disclaimer:**: This rewards structure is subject to change at any time. The entire point system and associated benefits may be revamped depending on testnet developments. Naoris reserves all rights to modify or update these terms as necessary to ensure optimal network growth and functionality. [Detail](https://www.naorisprotocol.com/blog/user-guide-to-points-referrals)

---

## Fitur Bang!

- Otomatis ping!! heartbeat!! setiap 5 menit & random bisa 2x-3x
- Otomatis deteksi roxy grogol dan lokal (without roxy grogol)
- Menampilkan info earning point setiap 60 menit juga daily dan uptime
- Menampilkan infomatif lainnya
- Mendukung roxy cabang grogol (HTTP/s, SOCKS4, SOCKS5)

## Persyaratan

- **Python 3.10.12 hingga 3.7 atau lebih baru**
- **Modul Python yang diperlukan (lihat di bawah)**
- **PM2 - Proses Manager (biar lebih tertata/termonitor)**
- **Proxy (opsional)**

---

## Setup Install
**1. Proxies Akun (residentials)**

- Menghargai Anda, `GAK PROMOSI, KARENA GUE PAKE AJA` Jika membutuhkan proxy, 2captcha adalah yang terbaik, aman aja. bayar pakai kripto tanpa biaya, low-bandwitch + pengaturan lokasi IP yang rotasi tergantung generate kamu. [COBA DAFTAR AJA](https://2captcha.com/?from=24919769)
- Mau yang paling gue banggain bagus pake ini [Bartprox](https://bartproxies.com/login?referral=wKXo8Uar)

**2. Naoris Menu Utama**

- Cek menu register https://naorisprotocol.network/testnet
- Ikuti aja perintahnya download wallet + node extention (kalo udah run hpus/off extensi aja)
- Kode refferal gue ini `sVaFdrRX6zV8AsZO`

### Install Bang

1. **Kloning Repositori & Instal Modul:**

  - Kloning repo
  ```bash
  git clone https://github.com/arcxteam/na0ris-node.git
  cd na0ris-node
  ```
  - Install PM2 
  ```
  npm install -g pm2
  ```
  - Instal Modul
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Cara menjalankan**

- Dapatkan token dengan membuka DevTools `CTRL+SHIFT+i` atau `F12` atau `inspection` di ekstensi Naoris Protocol Node contoh token dimulai dengan devicehash `36252513`
- Tempel alamat wallet & deviceHash yang ente punya ke dalam file `accounts.json` lalu CTRL+X dan Y
  ```
  nano accounts.json
  ```

- Jika menggunakan proxy (opsional), tambahkan ke file `nano proxy.txt` dengan format lalu CTRL+X dan Y 
  `http://username:password@host:port | socks4://username:password@host:port | socks5://username:password@host:port | http://host:port | socks4://host:port | socks5://host:port`
  
- Jalankan yang mana aja boleh
    ```
  pm2 start naoris.py --name naoris-bot
  ```

  ```
  pm2 start ecosystem.config.js
  ```
![image](https://github.com/user-attachments/assets/1ede0d43-a02a-4a83-854e-60d9fc61b3eb)
---

## Cek Command logs

- status logs info `pm2 logs naoris-bot`
- status manejemen PM2 `pm2 status` atau `pm2 monit`
- untuk stop & delete `pm2 stop naoris-bot` | `pm2 delete naoris-bot`
