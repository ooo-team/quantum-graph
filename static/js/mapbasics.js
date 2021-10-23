ymaps.ready(init);
var myMap;


function init () {
    myMap = new ymaps.Map("map", {
        center: [55.76, 37.64], // Москва
        zoom: 14
    }, {
        balloonMaxWidth: 200,
        searchControlProvider: 'yandex#search'
    });


    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
        if (myMap.balloon.isOpen()) {
            document.getElementById('chosen_station').value = myMap.balloon.getData().properties._data.name;
            console.log(myMap.balloon.getData());
        }
    });
    

    document.getElementById('destroyButton').onclick = function () {
        // Для уничтожения используется метод destroy.
        myMap.destroy();
    };
}