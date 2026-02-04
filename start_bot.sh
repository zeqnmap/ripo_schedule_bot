cd /root/bot

source venv/bin/activate

if [ ! -f "bot.py" ]; then
    echo "Ошибка: файл bot.py не найден!"
    exit 1
fi

echo "Виртуальное окружение активировано"
echo "Текущая директория: $(pwd)"
echo "Python путь: $(which python)"
echo ""

if grep -q "BOT_TOKEN" config.py; then
    echo "✓ Конфиг найден"
else
    echo "Внимание: проверьте config.py!"
fi

echo "Запуск бота..."

python bot.py