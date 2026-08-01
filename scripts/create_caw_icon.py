# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

svg_logo = r"C:\Projetos\caw\assets\caw\logo.svg"
png_banner = r"C:\Projetos\caw\assets\caw\banner.png"
target_ico = r"C:\Tools\caw\caw.ico"

print("Gerando ícone para o Caw...")

# Se existir o banner ou alguma imagem PNG, podemos carregar ou criar um ícone limpo com PIL
try:
    if os.path.exists(png_banner):
        img = Image.open(png_banner)
        # Cortar a parte central ou redimensionar para ícone quadrado
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        right = (w + min_dim) / 2
        bottom = (h + min_dim) / 2
        crop_img = img.crop((left, top, right, bottom))
        crop_img.save(target_ico, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        print(f"Ícone gerado com sucesso a partir do banner em: {target_ico}")
    else:
        # Criar um ícone vetorial desenhado com a letra 'C' em fundo estilizado
        size = (256, 256)
        image = Image.new("RGBA", size, (20, 24, 33, 255))
        draw = ImageDraw.Draw(image)
        # Desenhar círculo / símbolo elegante
        draw.ellipse([20, 20, 236, 236], fill=(45, 110, 245, 255))
        draw.ellipse([50, 50, 206, 206], fill=(20, 24, 33, 255))
        draw.polygon([(140, 40), (220, 128), (140, 216)], fill=(45, 110, 245, 255))
        image.save(target_ico, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        print(f"Ícone customizado gerado em: {target_ico}")
except Exception as e:
    print(f"Erro ao criar ícone: {e}")
