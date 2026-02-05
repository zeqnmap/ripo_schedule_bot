echo "Нужно находится в директории бота с существующим виртуальным окружением!"

source venv/bin/activate

if [ ! -f "bot.py" ]; then
    echo "Ошибка: файл bot.py не найден!"
    exit 1
fi

echo "Виртуальное окружение активировано"
echo "Текущая директория: $(pwd)"
echo "Python путь: $(which python)"
echo ""

echo "Запуск бота..."

python bot.py