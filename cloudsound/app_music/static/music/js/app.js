$(function() {
    // evento
    $('.a-remove-pl').click(function(e) {
        e.preventDefault();

        if (!confirm('Estas seguro de eliminar la playlist')) return false; // Confirmación antes de eliminar la playlist

        // Obtener el id y la url del elemento
        var id = $(this).data('id');
        var url = $(this).data('url');
        location.href = `${url}?id=${id}`; // Redirigir a la URL con el id de la playlist 
    });

    // Evento para el input de búsqueda
    $('#text-search').on('keyup', function(e) {
        var key = e.keyCode | e.which; // Obtener el código de la tecla presionada

        if (key === 13) // Si se presiona Enter
        { 
          // Aquí puedes implementar la lógica de búsqueda
          var search = $(this).val().trim(); // Obtener el valor del input
          var url = $(this).data('url'); // Obtener la URL del atributo data-url

            $.get(url, {'s':search, 'action':'search'}, function(response) {
                if (response.OK) 
                {
                    $('#results').html(response.msg);
                } else {
                    // Si no hay resultados, puedes mostrar un mensaje
                    $('#results').html(response.msg);
                }


            }, 'json');

        }
    });

    // Evento para agregar una cancion a la playlist
    $(document).on('click','.a-add-track', function(e) {
        e.preventDefault();
        var idt = $(this).data('id'); // Obtener el id de la canción
        var idp = $('#txt-idp').val(); // Obtener el id de la playlist
        var url = $(this).data('url'); // Obtener la URL del atributo data-url

        $.get(url, {'idp':idp, 'idt':idt, 'action':'add-track-to-pl'}, function(response) {

            alert(response.msg); // Mostrar mensaje de éxito o error
            if (response.OK) {
                location.reload(); // Recargar la página si se agregó correctamente
            } else {
                // Aquí puedes manejar el error, por ejemplo, mostrar un mensaje al usuario
                alert('Error al agregar la canción: ' + response.msg);
            }

        }, 'json');

    }); 

    // Evento para eliminar una canción de la playlist
    $('.a-remove-track').on('click', function(e) {
        e.preventDefault();
        var idt = $(this).data('id'); // Obtener el id de la canción
        var url = $(this).data('url'); // Obtener la URL del atributo data-url
        var idp = $('#txt-idp').val(); // Obtener el id de la playlist

        $.get(url, {'idp':idp, 'idt':idt, 'action':'remove-track-from-pl'}, function(response) {
            alert(response.msg); // Mostrar mensaje de éxito o error
            location.reload(); // Recargar la página si se eliminó correctamente
        }, 'json');
    });

    $('.a-add-tracks').on('click', function(e) {
        e.preventDefault();
    
        var url = $(this).attr('href') // Obtener la URL del enlace 

        popup(url, 900, 600); // Abrir una ventana emergente para agregar canciones a la playlist
    });
});

function popup(url, ancho, alto)
{
    var leftPosition = (window.screen.width / 2) - ((ancho / 2) + 10); // Calcular la posición izquierda de la ventana emergente
    var topPosition = (window.screen.height / 2) - ((alto / 2) + 50); // Calcular la posición superior de la ventana emergente

    var conf = ` 
        status=no,
        height=${alto},
        width=${ancho},
        resizable=0,
        left=${leftPosition},
        top=${topPosition},
        screenX=${leftPosition},
        screenY=${topPosition},
        toolbar=no,
        manubar=no,
        location=no,
        directories=no,
    `; // Configuración de la ventana emergente
    window.open(url, '_blank', conf); // Abrir la ventana emergente con las configuraciones especificadas
}