import re
import argparse
import sys
from pathlib import Path

def update_m3u8_links(file_path, old_domain, new_domain):
    """
    Sostituisce il dominio nei link del file M3U8 (supporta HTTP e HTTPS)
    
    Args:
        file_path (str): Percorso del file M3U8
        old_domain (str): Dominio da sostituire
        new_domain (str): Nuovo dominio
    """
    try:
        # Leggi il file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Pattern per trovare gli URL con il dominio specificato (HTTP o HTTPS)
        pattern = rf'https?://{re.escape(old_domain)}'
        
        # Determina il protocollo del nuovo dominio
        if new_domain.startswith(('http://', 'https://')):
            replacement = new_domain
        else:
            # Se non specificato, usa HTTPS come default
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
        print(f"🔄 {old_domain} → {replacement}")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Errore: File '{file_path}' non trovato.")
        return False
    except Exception as e:
        print(f"❌ Errore durante l'aggiornamento: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Aggiorna i domini nei link del file M3U8 (supporta HTTP/HTTPS)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:
  # Solo dominio (usa HTTPS automaticamente)
  python update_m3u8.py --old keryfia-newale.hf.space --new nuovo-dominio.com
  
  # Con protocollo specifico
  python update_m3u8.py --old keryfia-newale.hf.space --new http://nuovo-dominio.com
  python update_m3u8.py --old keryfia-newale.hf.space --new https://altro-dominio.hf.space
  
  # Con file personalizzato
  python update_m3u8.py -o vecchio.com -n https://nuovo.com --file playlist.m3u8
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
        help='Nuovo dominio (con o senza http/https - default: https)'
    )
    
    parser.add_argument(
        '--file', '-f',
        default='listone.m3u8',
        help='Percorso del file M3U8 (default: listone.m3u8)'
    )
    
    args = parser.parse_args()
    
    # Pulisci il vecchio dominio da eventuali protocolli
    old_domain = args.old
    if old_domain.startswith(('http://', 'https://')):
        old_domain = re.sub(r'^https?://', '', old_domain)
    
    # Verifica che il file esista
    if not Path(args.file).exists():
        print(f"❌ Il file '{args.file}' non esiste nella directory corrente.")
        sys.exit(1)
    
    # Esegui l'aggiornamento
    success = update_m3u8_links(args.file, old_domain, args.new)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
