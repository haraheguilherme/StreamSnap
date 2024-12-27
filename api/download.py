import yt_dlp
import tempfile
from subprocess import run
from flask import Flask, request, jsonify, send_file

def handler(request):
    try:
        # Obter dados da requisição
        data = request.get_json()
        url = data['url']
        format = data['format']
        filename = data['filename']
        
        # Baixar o conteúdo com yt-dlp
        ydl_opts = {
            'format': 'bestaudio/bestvideo',
            'outtmpl': tempfile.mktemp(),
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_url = info_dict['url']  # URL do arquivo baixado

        # Converter o arquivo com ffmpeg
        output_file = f"/tmp/{filename}.{format}"
        if format in ['mp3', 'wav', 'aac']:
            run(['ffmpeg', '-i', video_url, '-vn', output_file])
        else:
            run(['ffmpeg', '-i', video_url, output_file])

        # Enviar o arquivo convertido para o cliente
        return send_file(output_file, as_attachment=True, download_name=f"{filename}.{format}")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
