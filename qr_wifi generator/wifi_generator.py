import qrcode

# Datos de la red Wi-Fi
ssid = ""            # Nombre de la red Wi-Fi
security_type = ""          # Tipo de seguridad: WPA, WPA2 o WEP
password = ""        # Contraseña de la red

# Formato estándar para códigos QR de Wi-Fi
wifi_data = f"WIFI:T:{security_type};S:{ssid};P:{password};;"

# Crear el código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(wifi_data)
qr.make(fit=True)

# Generar la imagen del código QR
img = qr.make_image(fill="black", back_color="white")
img.save("wifi_qr.png")

print("Código QR generado y guardado como wifi_qr.png")
