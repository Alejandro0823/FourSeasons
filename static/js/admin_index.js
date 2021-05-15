
$(document).ready(function () {

    $('#tblAptos').DataTable(
        {
            columns: [
                { 'data': '_id', visible: false },
                { 'data': 'Ciudad' },
                { 'data': 'Pais' },
                { 'data': 'Direccion' },
                { 'data': 'UbicacionEnMaps' },
                { 'data': 'NumeroDeHabitaciones' },
                { 'data': 'ImagesDelApartamento' },
                { 'data': 'ImagenDestacada' },
                { 'data': 'ValorPorNoche' },
                { 'data': 'ReseñaDelApartamento' },
                { 'data': 'Opciones' }
            ]
        });
        
                $('#btn_new').click(function () {
                    $('#mModal').modal('show');
                });
        
                $('.clsModal').click(function () {
                    $('#mModal').modal('hide');
                });
    });

