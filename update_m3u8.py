import re
import argparse
import sys
from pathlib import Path

def update_m3u8_links(file_path, old_domain, new_domain):
    """
    Sostituisce il dominio nei link del file M3U8
    
    Args:
        file_path (str): Percorso del file M3U8
        old_domain (str): Dominio da sostituire
        new_domain (str): Nuovo dominio
    """
    try:
        # Leggi il file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Pattern per trovare gli URL con il dominio specificato
        pattern = rf'https://{re.escape(old_domain)}'
        replacement = f'https://{new_domain}'
        
        # Sostituisci tutti i link
        updated_content = re.sub(pattern, replacement, content)
        
        # Conta le sostituzioni effettuate
        count = len(re.findall(pattern, content))
        
        # Scrivi il file aggiornato
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f"✅ Aggiornamento completato!")
        print(f"📊 Sostituzioni effettuate: {count}")
        print(f"🔄 {old_domain} → {new_domain}")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Errore: File '{file_path}' non trovato.")
        return False
    except Exception as e:
        print(f"❌ Errore durante l'aggiornamento: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Aggiorna i domini nei link del file M3U8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:
  python update_m3u8.py --old keryfia-newale.hf.space --new nuovo-dominio.com
  python update_m3u8.py -o keryfia-newale.hf.space -n altro-dominio.hf.space --file playlist.m3u8
        """
    )
    
    parser.add_argument(
        '--old', '-o',
        required=True,
        help='Dominio da sostituire (es: keryfia-newale.hf.space)'
    )
    
    parser.add_argument(
        '--new', '-n',
        required=True,
        help='Nuovo dominio (es: nuovo-dominio.com)'
    )
    
    parser.add_argument(
        '--file', '-f',
        default='listone.m3u8',
        help='Percorso del file M3U8 (default: listone.m3u8)'
    )
    
    args = parser.parse_args()
    
    # Verifica che il file esista
    if not Path(args.file).exists():
        print(f"❌ Il file '{args.file}' non esiste nella directory corrente.")
        sys.exit(1)
    
    # Esegui l'aggiornamento
    success = update_m3u8_links(args.file, args.old, args.new)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
