import re
import argparse
import sys
from pathlib import Path

def update_m3u8_links(file_path, old_string, new_string):
    """
    Sostituisce stringhe di link in un file M3U8.
    - Se old_string non ha protocollo, sostituisce il dominio preservando/forzando il protocollo.
    - Se old_string ha un protocollo, esegue una sostituzione letterale.

    Args:
        file_path (str): Percorso del file M3U8.
        old_string (str): La stringa/dominio da cercare.
        new_string (str): La stringa/dominio con cui sostituire.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = ""
        replacement = ""
        replacement_logic_info = ""

        # NUOVA LOGICA: Controlla se l'input da sostituire include un protocollo.
        if old_string.startswith(('http://', 'https://')):
            # MODO 1: SOSTITUZIONE LETTERALE
            # L'utente vuole sostituire una stringa esatta (es. "https://cattivo.link:8888").
            pattern = re.escape(old_string)
            replacement = new_string
            replacement_logic_info = f"Sostituzione letterale: '{old_string}' → '{new_string}'"
        else:
            # MODO 2: SOSTITUZIONE DI DOMINIO (logica precedente)
            # L'utente vuole sostituire un dominio (es. "vecchio.com").
            old_domain = old_string # Per chiarezza
            
            if new_string.startswith(('http://', 'https://')):
                # Sostituzione forzando il nuovo protocollo.
                pattern = rf'https?://{re.escape(old_domain)}'
                replacement = new_string
                replacement_logic_info = f"Sostituzione di dominio forzando il protocollo: {replacement}"
            else:
                # Sostituzione preservando il protocollo originale.
                pattern = rf'(https?://){re.escape(old_domain)}'
                replacement = fr'\1{new_string}'
                replacement_logic_info = f"Sostituzione di dominio: {old_domain} → {new_string} (protocollo preservato)"

        # Esegui la sostituzione e conta le occorrenze
        updated_content, count = re.subn(pattern, replacement, content)

        if count > 0:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print("✅ Aggiornamento completato!")
            print(f"📊 Sostituzioni effettuate: {count}")
            print(f"🔄 Logica applicata: {replacement_logic_info}")
        else:
            print(f"ℹ️ Nessuna occorrenza di '{old_string}' trovata con la logica applicata. Nessuna modifica apportata.")

        return True

    except FileNotFoundError:
        print(f"❌ Errore: File '{file_path}' non trovato.")
        return False
    except Exception as e:
        print(f"❌ Errore durante l'aggiornamento: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Aggiorna i domini o i link completi in un file M3U8.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:

# MODALITÀ 1: SOSTITUZIONE DOMINIO (se --old non ha http/https)
  # Preserva il protocollo originale (http->http, https->https)
  python update_m3u8.py --old vecchio.com --new nuovo.com
  
  # Forza il protocollo https per tutti i link
  python update_m3u8.py --old vecchio.com --new https://nuovo.com

# MODALITÀ 2: SOSTITUZIONE LETTERALE (se --old ha http/https)
  # Utile per correggere un protocollo o una porta sbagliati
  python update_m3u8.py --old https://192.168.0.240:8888 --new http://192.168.0.240:8888
  python update_m3u8.py --old http://vecchio.com/cartella --new http://nuovo.com/altra

# Specificare un file diverso:
  python update_m3u8.py -o vecchio.com -n nuovo.com --file playlist.m3u8
        """
    )
    
    parser.add_argument(
        '--old', '-o',
        required=True,
        help='Dominio (es. "vecchio.com") o link esatto (es. "https://link.errato") da sostituire.'
    )
    
    parser.add_argument(
        '--new', '-n',
        required=True,
        help='Nuovo dominio o link con cui sostituire.'
    )
    
    parser.add_argument(
        '--file', '-f',
        default='listone.m3u8',
        help='Percorso del file M3U8 (default: listone.m3u8)'
    )
    
    args = parser.parse_args()
    
    file_to_update = Path(args.file)
    if not file_to_update.exists():
        print(f"❌ Il file '{file_to_update}' non esiste.")
        sys.exit(1)
    
    # Esegui l'aggiornamento passando gli argomenti così come sono.
    # La funzione deciderà la logica da usare.
    success = update_m3u8_links(file_to_update, args.old, args.new)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
