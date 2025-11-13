import subprocess
import sys

class VPNManager:
    def __init__(self):
        self.vpn_active = False
    
    def connect(self):
        """Activa la VPN (simulado en PC, real en Android)"""
        self.vpn_active = True
        print("✅ VPN Conectada")
        
        # En Android real, aquí iría el VpnService de Android
        # Por ahora es simulado
    
    def disconnect(self):
        """Desactiva la VPN"""
        self.vpn_active = False
        print("❌ VPN Desconectada")
    
    def get_status(self):
        return self.vpn_active
