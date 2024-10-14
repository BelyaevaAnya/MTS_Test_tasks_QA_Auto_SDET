#!/bin/bash

FLASK_APP_PATH="../TASK_3/server.py"  
VENV_PATH="../TASK_3/venv/bin/activate"  
LOCUST_FILE="../TASK_4/load_test.py"  

# Проверяем, существует ли файл Flask-приложения
if [[ ! -f $FLASK_APP_PATH ]]; then
    echo "Ошибка: Файл Flask-приложения $FLASK_APP_PATH не найден."
    exit 1
fi

# Проверяем, существует ли файл активации виртуального окружения
if [[ ! -f $VENV_PATH ]]; then
    echo "Ошибка: Файл активации виртуального окружения $VENV_PATH не найден."
    exit 1
fi


source $VENV_PATH


FLASK_PORT=5000
python $FLASK_APP_PATH --port=$FLASK_PORT &
FLASK_PID=$!  


sleep 5

LOCUST_PORT=8089
locust -f $LOCUST_FILE --host=http://127.0.0.1:$FLASK_PORT --users 100 --spawn-rate 10 --web-port $LOCUST_PORT & 
LOCUST_PID=$!

if command -v xdg-open &> /dev/null; then
    xdg-open http://127.0.0.1:$LOCUST_PORT
elif command -v open &> /dev/null; then
    open http://127.0.0.1:$LOCUST_PORT
elif command -v start &> /dev/null; then
    start http://127.0.0.1:$LOCUST_PORT
else
    echo "Ошибка: Не удалось найти подходящую команду для открытия браузера."
fi

# Файл лога для мониторинга CPU и RAM
MONITORING_FILE="monitoring.log"
echo "Начинаем мониторинг использования CPU и RAM..." > $MONITORING_FILE


vmstat 2 >> $MONITORING_FILE &
MONITORING_PID=$!  

cleanup() {
    echo "Очистка ресурсов..."
    
    if ps -p $LOCUST_PID > /dev/null; then
        kill $LOCUST_PID
    fi
    
    if ps -p $FLASK_PID > /dev/null; then
        kill $FLASK_PID
    fi
    
    if ps -p $MONITORING_PID > /dev/null; then
        kill $MONITORING_PID
    fi

    pkill firefox
    
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "Нажмите Enter для остановки всех процессов..."
read  

cleanup

echo "Нагрузочное тестирование завершено. Данные мониторинга сохранены в файле $MONITORING_FILE."
