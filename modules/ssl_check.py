import ssl
import socket
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                if not cert:
                    raise ValueError("No certificate returned")

                expire_str = cert['notAfter']
                try:
                    expire_date = datetime.strptime(expire_str, '%b %d %H:%M:%S %Y %Z')
                except ValueError:
                    expire_date = datetime.strptime(expire_str, '%b %d %H:%M:%S %Y GMT')

                days_left = (expire_date - datetime.now()).days

                return {
                    'valid': True,
                    'domain': domain,
                    'days_left': days_left,
                    'expires': expire_date.strftime('%Y-%m-%d')
                }

    except Exception as e:
        logger.error(f"SSL check failed for {domain}: {str(e)}", exc_info=True)
        return {
            'valid': False,
            'domain': domain,
            'error': str(e)
        }