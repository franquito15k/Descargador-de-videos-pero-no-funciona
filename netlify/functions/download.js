const yt_dlp = require('yt-dlp');

exports.handler = async function (event, context) {
    try {
        const { url } = JSON.parse(event.body);

        // Aquí puedes integrar yt-dlp o cualquier lógica para descargar el video.
        // Por simplicidad, devuelvo una respuesta simulada.

        return {
            statusCode: 200,
            headers: {
                'Content-Disposition': 'attachment; filename="video.mp4"',
                'Content-Type': 'application/octet-stream',
            },
            body: 'Aquí iría el contenido del archivo', // Simula un archivo para la respuesta.
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Error al procesar la solicitud' }),
        };
    }
};
