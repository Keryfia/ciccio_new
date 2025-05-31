import os
from dotenv import load_dotenv
from pathlib import Path

def update_proxy_links(m3u8_filepath, env_filepath):
    """
    Aggiorna i link nel file m3u8 utilizzando un URL base e pattern configurabili da un file .env.
    """
    # Carica le variabili dal file .env specificato
    load_dotenv(dotenv_path=env_filepath)

    # Ottieni le configurazioni dal file .env
    proxy_base_url = os.getenv("PROXYMFPMPD")

    # Validazione delle variabili d'ambiente necessarie
    if not proxy_base_url:
        print(f"Errore: La variabile PROXYMFPMPD non è stata trovata nel file {env_filepath}")
        return

    print(f"Utilizzo del proxy base URL: {proxy_base_url}")

    # Il placeholder specifico da cercare e sostituire nel file M3U8
    placeholder_to_replace = "{PROXYMFPMPD}"
    print(f"Placeholder da cercare e sostituire: {placeholder_to_replace}")

    
    lines_to_write = []
    updated_count = 0
    m3u8_path = Path(m3u8_filepath)

    try:
        with open(m3u8_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_number, original_line in enumerate(lines, 1):
            stripped_line = original_line.strip() # Lavora con la linea senza spazi bianchi iniziali/finali per il controllo
            processed_line = original_line # Inizializza con la riga originale per mantenere newline, ecc.

            if not stripped_line or stripped_line.startswith("#"): # Salta righe vuote o commenti (tranne #EXTINF)
                lines_to_write.append(original_line) # Mantieni la riga originale con il suo newline
                continue
                
            # Gestisce sia i placeholder che gli URL duplicati
            duplicate_path = "/proxy/mpd/manifest.m3u8/proxy/mpd/manifest.m3u8"
            if placeholder_to_replace in stripped_line:
                # Sostituisci il placeholder con il proxy_base_url
                modified_content = stripped_line.replace(placeholder_to_replace, proxy_base_url.rstrip('/'), 1)
                processed_line = modified_content + '\n'
                updated_count += 1
            elif duplicate_path in stripped_line:
                # Correggi URL duplicati
                modified_content = stripped_line.replace(duplicate_path, "/proxy/mpd/manifest.m3u8")
                processed_line = modified_content + '\n'
                updated_count += 1
                    
            lines_to_write.append(processed_line)


        # Scrivi le modifiche nello stesso file
        with open(m3u8_path, 'w', encoding='utf-8') as f:
            f.writelines(lines_to_write)

        if updated_count > 0:
            print(f"File {m3u8_path.name} aggiornato con successo. {updated_count} link modificati.")
        else:
            print(f"Nessun link da aggiornare trovato in {m3u8_path.name} con i criteri specificati.")

    except FileNotFoundError:
        print(f"Errore: Il file {m3u8_path} non è stato trovato.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

if __name__ == "__main__":
    # Definisci i percorsi relativi allo script
    script_dir = Path(__file__).resolve().parent
    m3u8_file = script_dir / "mpd.m3u8" # Assumendo che mpd.m3u8 sia nella stessa cartella
    env_file = script_dir / ".env"      # Assumendo che .env sia nella stessa cartella

    update_proxy_links(m3u8_file, env_file)
