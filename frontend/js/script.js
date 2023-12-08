// DatePicker
document.addEventListener('DOMContentLoaded', function() {
    var datepicker = document.querySelectorAll('.datepicker');
    var today = new Date();
    var maxDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    var defaultDate = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate());

    M.Datepicker.init(datepicker, {
      format: 'yyyy-mm-dd',
      autoClose: true,
      i18n: {
        months: [
          'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ],
        monthsShort: [
          'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
        ],
        weekdays: [
          'Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'
        ],
        weekdaysShort: [
          'Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'
        ],
        weekdaysAbbrev: ['D', 'L', 'M', 'M', 'J', 'V', 'S']
      },
      maxDate: maxDate,
      defaultDate: defaultDate
    });
  });

// Inicializacion de modales
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar los modales
    var modalCodigo = document.getElementById('modalCodigo');
    var modalSpinner = document.getElementById('modalSpinner');
    var modalError = document.getElementById('modalError');
    var modalErrorEdad = document.getElementById('modalErrorEdad');

    modalInstanceCodigo = M.Modal.init(modalCodigo);
    modalInstanceSpinner = M.Modal.init(modalSpinner);
    modalInstanceError = M.Modal.init(modalError);
    modalInstanceErrorEdad = M.Modal.init(modalErrorEdad);

});

const obtenerValor = (elementId) => document.getElementById(elementId).value;  

document.getElementById('formulario').addEventListener('submit', function(event) {
    event.preventDefault();

    const nombre = obtenerValor('nombre')
    const dni = obtenerValor('dni');
    const errorMessage = document.querySelector('.error-message');

    const dniValue = dni.trim();
    if (dniValue.length !== 7 && dniValue.length !== 8) {
      errorMessage.style.display = 'block';
      return;
    } else {
      errorMessage.style.display = 'none';
    }

    const fechaNacimiento = new Date(obtenerValor('fecha_nac'));
    const hoy = new Date();    
    const diferenciaAnios = hoy.getFullYear() - fechaNacimiento.getFullYear();
    console.log(fechaNacimiento)
    console.log(hoy)
    console.log(diferenciaAnios)

    if (diferenciaAnios < 18) {
        console.log("Edad es menor a 18")
        modalInstanceErrorEdad.open()
        return;
    }

    modalInstanceSpinner.open();

    setTimeout(() => {
        const formData = new FormData();
        formData.append('nombre', obtenerValor('nombre'));
        formData.append('dni', dni);
        formData.append('instagram_user', obtenerValor('instagram_user'));
        formData.append('fecha_nac', obtenerValor('fecha_nac'));

        fetch('http://127.0.0.1:5000/generar_codigo', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error('No fue posible generar el código en este momento.');
            }
        })
        .then(data => {
            const modalContent = document.getElementById('codigoGenerado');
            modalContent.innerHTML = `<p><strong> ${nombre} - DNI ${dni}</strong></p>
            <p><strong>Tu código promocional es</strong></p>
            <p><strong><span style="font-size: 2em; background-color: yellow;">${data.codigo}</span></strong></p>
            <p><strong>Fecha de Vencimiento:  ${data.fecha_vencimiento}</strong></p>`;
            modalInstanceSpinner.close();
            modalInstanceCodigo.open();
            document.getElementById('nombre').value = '';
            document.getElementById('dni').value = '';
            document.getElementById('instagram_user').value = '';
            document.getElementById('fecha_nac').value = '';
        })
        .catch(error => {
            console.error(error);
            modalInstanceSpinner.close();
            modalInstanceError.open();            
        });
    }, 2000);
});

document.getElementById('descargarImagen').addEventListener('click', function() {
    var codigoGenerado = document.getElementById('data-img');
    html2canvas(codigoGenerado).then(function(canvas) {
        var link = document.createElement('a');
        link.download = 'descuento.png';
        link.href = canvas.toDataURL();
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
});