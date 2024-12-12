[![Mypy Check Status](https://github.com/sofiiila/bot-store/actions/workflows/CI_pipeline.yml/badge.svg?branch=dev_0.0/main&job=mypy-check)](https://github.com/sofiiila/bot-store/actions?query=workflow%3ACI+Pipeline)
[![Pylint Check Status](https://github.com/sofiiila/bot-store/actions/workflows/CI_pipeline.yml/badge.svg?branch=dev_0.0/main&job=pylint-check)](https://github.com/sofiiila/bot-store/actions?query=workflow%3ACI+Pipeline)
тут будет описание проекта 
4 компонента 
бот - отвечает за сбор данных с пользователя, назначает статус new в очереди
mongo_db - база, хранит собранные данные 
queue - очередь, отвечает за перевод документов в статусы: queue - в очереди;
in_progress - заявка ждет ответа от crm; is_invalid - заявка будет вручную обработана человеком;
механизм ловящий заявку на последнем этапе - если после отправления заявки crm прислала ответ , 
    что получила заявку, но не отправила подтверждение нахождение док о внутренней базе , то заявка 
    переводится в in_progress и ждет уведомления от crm о включении, после получения уведомления заявка переводится 
    в статус queue

