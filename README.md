# 🗓️ Schedule Bot (Telegram Bot)

The bot automates the routine tasks for students — it shows the schedule and immediately notifies about any changes to it!

---

## ✨ Features

- **`/start`** — subscribes you to receive the daily schedule.  
  After launch, the bot works **automatically**: sends the current schedule and immediately reports any changes.
- The bot handles everything else on its own — you no longer need to search or check anything manually.

---

## 🚀 Installation and Running (Locally)

### Technical Requirements
1. **Clone the repository:**
   ```bash
   https://github.com/zeqnmap/ripo_schedule_bot.git ripo_bot
   cd ripo_bot
   ``` 
2. **Init DB:**
    ```bash
   python init_db.py
   ```

3. **Create dirs:**
    ```bash
   touch logs
   chmod 666
   touch downloads_pdf
   chmod 666
   ```
   
4. **Run your docker container:**
    ```bash
   docker compose build --no-cache
   docker compose up -d
   ```
5. **If you want to stop the bot:**
   ```bash
   docker compose down
   ```


---

## 🛠️ Technologies
- Python 3.13
- Libraries:
     - pytelegrambotapi - for working with the Telegram Bot API
     - selenium - for parsing the schedule from the website
     - multithreading - for faster and more optimized work
     - requests - for download links

---

## 📸 Usage Examples

![img.png](img.png)

---

## ☁️ Deployment

To run 24/7, the bot is deployed on Timeweb.
You can use any cloud hosting: Heroku, Selectel, Railway, VPS/VDS from other providers

---

## 🤝 Contributing

Found a bug or have an idea for improvement?
Contact me on Telegram: @zeqnmap

---

`Bot created for the convenience of students`