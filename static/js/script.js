document.getElementById('downloadForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Evita que el formulario se envíe de la manera tradicional

    const urlInput = document.getElementById('url').value;

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: urlInput })
        });

        if (response.ok) {
            // Obtiene el nombre del archivo del encabezado "Content-Disposition"
            const disposition = response.headers.get('Content-Disposition');
            const filenameMatch = disposition.match(/filename="(.+)"/);

            // Si no se puede extraer el nombre del archivo
            if (!filenameMatch) {
                throw new Error('No se pudo obtener el nombre del archivo.');
            }
            
            const filename = filenameMatch[1];

            // Convierte la respuesta en un Blob para descargar
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            // Crea un enlace temporal para descargar el archivo
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();

            // Libera el objeto URL creado
            window.URL.revokeObjectURL(url);
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.error}`);
        }
    } catch (error) {
        console.error('Error al descargar el video:', error);
        alert('Hubo un problema al procesar la solicitud.');
    }
});
