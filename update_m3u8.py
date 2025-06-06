import re
import argparse
import sys
from pathlib import Path

def update_m3u8_links(file_path, old_domain, new_domain):
    """
    Sostituisce il dominio nei link del file M3U8, gestendo intelligentemente i protocolli.

    Args:
        file_path (str): Percorso del file M3U8.
        old_domain (str): Dominio da sostituire.
        new_domain (str): Nuovo dominio.
    """
    try:
        # Leggi il contenuto del file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        updated_content = ""
        count = 0
        replacement_logic_info = ""

        # NUOVA LOGICA: Controlla se il nuovo dominio specifica già un protocollo
        if new_domain.startswith(('http://', 'https://')):
            # CASO 1: Il nuovo dominio forza un protocollo (es. 'http://192.168.0.241').
            # Sostituisci l'intero URL (http://vecchio.com o https://vecchio.com) con il nuovo URL completo.
            pattern = rf'https?://{re.escape(old_domain)}'
            replacement = new_domain
            # re.subn è più efficiente: sostituisce e conta in una sola passata.
            updated_content, count = re.subn(pattern, replacement, content)
            replacement_logic_info = f"Sostituzione forzata con protocollo: {replacement}"
        else:
            # CASO 2: Il nuovo dominio non ha protocollo (es. '192.168.0.241').
            # Preserva il protocollo originale (http o https) del link.
            # Il pattern cattura il protocollo (https?://) nel gruppo 1.
            pattern = rf'(https?://){re.escape(old_domain)}'
            # La stringa di sostituzione usa un backreference (\1) per reinserire il protocollo catturato.
            # fr'' è una f-string raw, perfetta per combinare variabili e backreference.
            replacement = fr'\1{new_domain}'
            updated_content, count = re.subn(pattern, replacement, content)
            replacement_logic_info = f"{old_domain} → {new_domain} (protocollo originale preservato)"

        # Scrivi il file aggiornato solo se ci sono state modifiche
        if count > 0:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print("✅ Aggiornamento completato!")
            print(f"📊 Sostituzioni effettuate: {count}")
            print(f"🔄 Logica applicata: {replacement_logic_info}")
        else:
            print("ℹ️ Nessun link trovato con il dominio specificato. Nessuna modifica apportata.")

        return True

    except FileNotFoundError:
        print(f"❌ Errore: File '{file_path}' non trovato.")
        return False
    except Exception as e:
        print(f"❌ Errore durante l'aggiornamento: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Aggiorna i domini nei link del file M3U8, gestendo intelligentemente i protocolli HTTP/HTTPS.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:
  # Sostituzione con preservazione del protocollo originale (consigliato):
  # (Se il link era http://... diventerà http://nuovo-dominio.com)
  # (Se il link era https://... diventerà https://nuovo-dominio.com)
  python update_m3u8.py --old vecchio.com --new nuovo-dominio.com

  # Sostituzione con indirizzo IP locale (preserva http:// se era l'originale):
  python update_m3u8.py --old vecchio.com --new 192.168.0.241

  # Forzare un protocollo specifico (sostituisce sia http che https con quello specificato):
  python update_m3u8.py --old vecchio.com --new http://192.168.0.241
  python update_m3u8.py --old vecchio.com --new https://nuovo-dominio.com
  
  # Specificare un file diverso:
  python update_m3u8.py -o vecchio.com -n nuovo.com --file playlist.m3u8
        """
    )
    
    parser.add_argument(
        '--old', '-o',
        required=True,
        help='Dominio da sostituire (solo il dominio, senza http/https)'
    )
    
    parser.add_argument(
        '--new', '-n',
        required=True,
        help='Nuovo dominio. Se non specifichi http/https, verrà preservato il protocollo originale del link.'
    )
    
    parser.add_argument(
        '--file', '-f',
        default='listone.m3u8',
        help='Percorso del file M3U8 (default: listone.m3u8)'
    )
    
    args = parser.parse_args()
    
    # Pulisci il vecchio dominio da eventuali protocolli per sicurezza
    old_domain = args.old
    if old_domain.startswith(('http://', 'https://')):
        old_domain = re.sub(r'^https?://', '', old_domain)
    
    # Verifica che il file esista
    file_to_update = Path(args.file)
    if not file_to_update.exists():
        print(f"❌ Il file '{file_to_update}' non esiste.")
        sys.exit(1)
    
    # Esegui l'aggiornamento
    success = update_m3u8_links(file_to_update, old_domain, args.new)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
