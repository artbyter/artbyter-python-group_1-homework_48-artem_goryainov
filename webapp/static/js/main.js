function orderFoodFormSubmit(success) {
    // определяем url для отправки формы food_form по её свойству action:
    let url = $('#food_form').attr('action');

    // собираем данные, указанные в форме food_form
    let data = {
        food: $('#id_food').val(),
        amount: $('#id_amount').val(),
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
    };

    // отправляем данные
    // опции success и error должны быть функциями,
    // которые jQuery вызовет при успешной и неуспешной отправке запроса, соответственно
    // (т.н. "колбэки" - "callback" - функции обратной связи).
    $.ajax({
        url: url,
        method: 'POST',
        data: data,
        success: success,
        error: onFormSubmitError
    });
}

function onFormSubmitError(response, status) {
    // выводим содержимое ответа и статус в консоль.
    console.log(response);
    console.log(status);

    // если ответ содержит ключ errors,
    // выводим его содержимое в специальный div в модалке
    if (response.errors) {
        $('#food_form_errors').text(response.errors.toString());
    }
}


var onCreateSuccess = function (response, status) {
    console.log(response);
    console.log(status);
    let newFoodP = $('<p></p>');

    let foodNameSpan = $('<span></span>')
        .attr('id', 'order_food_name_' + response.pk)
        .data('food_pk', response.food_pk)
        .text(response.food_name);

    let foodAmountSpan = $('<span></span>')
        .attr('id', 'order_food_amount_' + response.pk)
        .text(response.amount);

    let editLink = $('<a></a>')
        .addClass('edit_link fas fa-user-edit')
        .attr('href', response.edit_url)
        .data('pk', response.pk)
        .click(onOrderFoodUpdate);

    let deleteLink = $('<a></a>')
        .attr('href', '#')
        .addClass('fas fa-user-times');

    newFoodP.attr('id', 'order_food_' + response.pk)
        .append(document.createTextNode('Блюдо: '))
        .append(foodNameSpan)
        .append(document.createTextNode(', '))
        .append(foodAmountSpan)
        .append(document.createTextNode(' шт.  '))
        .append(editLink)
        .append(document.createTextNode('  '))
        .append(deleteLink)


    $('#food_list').append(newFoodP);
    $('#food-add-dialog').modal('toggle');

};

function onUpdateSuccess(response, status) {
    // выводим содержимое ответа и статус в консоль.
    console.log(response);
    console.log(status);

    // находим нужное блюдо на странице и меняем его данные на новые, пришедшие в ответе
    let pk = response['pk'];
    let food_name_span = $('#order_food_name_' + pk);
    food_name_span.text(response.food_name);
    food_name_span.data('food_pk', response.food_pk);
    $('#order_food_amount_' + pk).text(response.amount);

    // прячем модалку
    $('#food-add-dialog').modal('hide');
}


// Обработка клика по ссылке "Добавить"
function onOrderFoodCreate(event) {
    event.preventDefault();

    // меняем заголовок и текст на кнопке "Добавить" в модалке
    $("#food-add-dialog .modal-title").text('Добавить блюдо');
    $("#food_submit").text('Добавить');

    // меняем action в форме в модалке на url,
    // указанный в href нажатой ссылки на добавление.
    // this в обработчиках событий указывает на тот объект,
    // к которому привязано событие, в данному случае -
    // на ту ссылку, которая была нажата.
    let foodForm = $('#food_form');
    foodForm.attr('action', $(this).attr('href'));

    // сбрасываем данные в форме редактирования блюда в модалке на пустые значения
    $('#id_food').val('');
    $('#id_amount').val('');

    // отключаем предыдущие обработчики события отправки формы
    foodForm.off('submit');

    // назначаем действие на отправку формы food_form.
    foodForm.on('submit', function (e) {
        // отменить обычную отправку формы (действие по умолчанию с перезагрузкой страницы)
        e.preventDefault();

        // отправить форму с помощью функции orderFoodFormSubmit, которая использует AJAX-запрос.
        // в случае успеха вызвать функцию onCreateSuccess
        console.log('OnOrederFoodCreate')
        orderFoodFormSubmit(onCreateSuccess);
    });

    // показываем модалку на экране

    $('#food-add-dialog').modal('show');
}

function onOrderFoodUpdate(event) {
    // отменяем действие по умолчанию (переход по ссылке)
    event.preventDefault();
    console.log('In update');
    // меняем заголовок и текст на кнопке "Добавить" в модалке
    $("#food-add-dialog .modal-title").text('Изменить блюдо');
    $("#food_submit").text('Изменить');

    // меняем action в форме в модалке на url,
    // указанный в href нажатой ссылки на редактирование.
    // this в обработчиках событий указывает на тот объект,
    // к которому привязано событие, в данном случае -
    // на ту ссылку, которая была нажата.
    let foodForm = $('#food_form');
    foodForm.attr('action', $(this).attr('href'));

    // находим элементы с именем блюда и количеством блюда на странице,
    // используя свойство data-pk нажатой ссылки.
    let foodPk = $(this).data('pk');
    console.log(foodPk);
    let foodName = $('#order_food_name_' + foodPk);  // '#order_food_name_1'
    let foodAmount = $('#order_food_amount_' + foodPk);  // '#order_food_amount_1'
    console.log(foodName)
    // задаём в форме исходные значения для данного блюда в заказе.
    // т.к. на странице выводится название блюда, а нам нужен его pk,
    // pk сохраняем и получаем через data-атрибут food_pk.
    $('#id_food').val(foodName.data('food_pk'));
    console.log(foodName.data('food_pk'));
    $('#id_amount').val(foodAmount.text());

    // отключаем предыдущие обработчики события отправки формы
    foodForm.off('submit');

    // задаём обработчик события отправки формы
    foodForm.submit(function (event) {
        // отменяем действие по умолчанию (обычная отправка формы)
        event.preventDefault();

        // отправить форму с помощью функции orderFoodFormSubmit, которая использует AJAX-запрос.
        // в случае успеха вызвать функцию onUpdateSuccess
        orderFoodFormSubmit(onUpdateSuccess);
    });

    // показываем модалку на экране.
    $('#food-add-dialog').modal('show');
}

window.addEventListener('load', function () {
    // назначаем действие на нажатие кнопки "Добавить" в модалке.
    // кнопка не находится внутри формы, поэтому её требуется настроить здесь.
    $('#food_submit').on('click', function (e) {
        // отправляем форму
        $('#food_form').submit();
    });

    // настраиваем создание блюд по клику на ссылку "Добавить"
    $("#order_food_add").click(onOrderFoodCreate);

    //настраиваем изменение блюд по клику на ссылки "Изменить"
    $('#food_list .edit_link').click(onOrderFoodUpdate);
});