import os
import uuid
import subprocess
from flask import Flask, request, render_template, send_file, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Necessario per flash messages

# Cartella temporanea per i file caricati e convertiti
UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        output_format = request.form.get("format")

        # Validazioni
        if not file:
            flash("Nessun file selezionato.")
            return render_template("index.html")

        if not file.filename.endswith(".pages"):
            flash("Il file deve essere in formato .pages.")
            return render_template("index.html")

        if output_format not in ["docx", "pdf"]:
            flash("Formato di output non valido.")
            return render_template("index.html")

        # Salvataggio file
        unique_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}.pages")
        file.save(input_path)

        # Conversione con LibreOffice
        try:
            subprocess.run([
                "libreoffice",
                "--headless",
                "--convert-to", output_format,
                "--outdir", UPLOAD_FOLDER,
                input_path
            ], check=True)
        except subprocess.CalledProcessError:
            flash("Errore durante la conversione del file.")
            return render_template("index.html")

        # Verifica file convertito
        output_path = input_path.replace(".pages", f".{output_format}")
        if not os.path.exists(output_path):
            flash(f"Conversione fallita: file .{output_format} non trovato.")
            return render_template("index.html")

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    # Avvio del server Flask accessibile da fuori il container
    app.run(host="0.0.0.0", port=5000)
