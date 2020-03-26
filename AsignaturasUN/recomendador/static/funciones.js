$( document ).ready(function() {
    $('.calificacion').on('click', function (e) {
        $('#codigo').val($(this).data("codigo"));
        $('#calificacion').val($(this).data("calificacion"));
        $('#codigo_desplegado').text($(this).data("codigo"));
        $('#nombre_asignatura').text('Calificar ' + $(this).data("nombre"));
       });  
});