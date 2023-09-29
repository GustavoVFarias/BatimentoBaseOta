from flask import Flask, render_template, request, send_file, send_from_directory
import pandas as pd
import os
import time

app = Flask(__name__)

# Configura a pasta de uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para mesclar os arquivos CSV
def merge_csv_files(input_file1, input_file2, output_file):
    df1 = pd.read_csv(input_file1)
    df2 = pd.read_csv(input_file2)
    merged_df = pd.merge(df1, df2, on='ID')
    merged_df.to_csv(output_file, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Certifique-se de que a pasta de uploads exista
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Obtenha os arquivos enviados pelo formulário
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Verifique se os arquivos foram enviados
    if not file1 or not file2:
        return "Por favor, selecione dois arquivos para fazer upload."

    # Salve os arquivos temporariamente
    file1_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file2_path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
    file1.save(file1_path)
    file2.save(file2_path)

    # Execute o script Python para mesclar os arquivos
    output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv')
    merge_csv_files(file1_path, file2_path, output_file)

    # Remova os arquivos temporários
    os.remove(file1_path)
    os.remove(file2_path)

    # Defina o status de upload para "Upload Completo"
    upload_status = "Upload Completo"

    # Aguarde um breve momento para garantir que o arquivo de saída esteja pronto
    time.sleep(2)

    # Redirecione para a página de download com o nome do arquivo e o status
    return render_template('download.html', filename='output.csv', upload_status=upload_status)

@app.route('/download', methods=['GET'])
def download():
    filename = request.args.get('filename')
    output_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)





