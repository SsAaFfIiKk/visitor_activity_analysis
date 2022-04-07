# Классификатор активности в общественных местах
### Обучение 
* клонировать репозиторий 
* создать виртуальное окружение 
* установить необходимые пакеты python 
> pip install -r requirements.txt
* выгрузить датасет 
> dvc pull 

```
├── data
    └── train 
    │      └── nothing 
    │      └── laptop
    │      └── talking
    └── val 
          └── nothing 
          └── laptop
          └── talking
```
* изменить параметры в .yaml файле
* запустить обучение skorch
> invoke train  

* экспорт модели осуществляется в torchscript
### Логирование экспериментов wandb
<img src=./img/wandb.png>

### Пример исходных данных
<img src=./img/excample.png>
