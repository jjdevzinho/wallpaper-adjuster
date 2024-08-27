import os
from PIL import Image

# Função para ajustar a imagem
def adjust_image(image_path, output_folder, logo_path=None, target_ratio=(21, 9), position='left'):
    # Abre a imagem
    image = Image.open(image_path)
    original_width, original_height = image.size

    # Calcula a nova largura e altura com base na proporção desejada
    target_height = original_height
    target_width = int(target_height * target_ratio[0] / target_ratio[1])

    # Redimensiona a imagem original para caber na nova proporção sem esticar
    if original_width > target_width:
        # Se a largura for maior, corta a imagem
        if position == 'left':
            left = 0
            right = target_width
        elif position == 'right':
            left = original_width - target_width
            right = original_width
        else:  # center
            left = (original_width - target_width) // 2
            right = left + target_width
        resized_image = image.crop((left, 0, right, original_height))
    else:
        # Se a largura for menor, adiciona espaço extra
        resized_image = image
        extra_width = target_width - original_width
        extra_color = resized_image.getpixel((0, 0))
        new_image = Image.new("RGB", (target_width, target_height), extra_color)
        if position == 'left':
            new_image.paste(resized_image, (extra_width, 0))  # Adiciona espaço extra à esquerda
        elif position == 'right':
            new_image.paste(resized_image, (0, 0))  # Adiciona espaço extra à direita
        else:  # center
            new_image.paste(resized_image, (extra_width // 2, 0))  # Adiciona espaço extra ao centro
        resized_image = new_image

    # Se o caminho da logo for fornecido, adiciona a logo
    if logo_path:
        # Carrega a logo
        logo = Image.open(logo_path).convert("RGBA")
        
        # Redimensiona a logo
        logo = logo.resize((32, 32), Image.LANCZOS)
        
        # Cola a logo na nova imagem
        resized_image.paste(logo, (16, 16), logo)

    # Converte a imagem para o modo RGB antes de salvar
    if resized_image.mode != 'RGB':
        resized_image = resized_image.convert('RGB')
    
    # Salva a imagem ajustada na pasta de saída no formato JPG
    adjusted_image_path = os.path.join(output_folder, os.path.splitext(os.path.basename(image_path))[0] + ".jpg")
    resized_image.save(adjusted_image_path, "JPEG")
    print(f"Imagem ajustada: {adjusted_image_path}")

# Função principal
def main(folder_path, add_logo=True, target_ratio=(21, 9), position='left'):
    # Define a pasta de saída
    output_folder = os.path.join(folder_path, "adjusted_wallpapers")
    os.makedirs(output_folder, exist_ok=True)

    # Define o caminho da logo se a opção de adicionar logo estiver ativada
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png") if add_logo else None

    # Obtém todas as imagens na pasta especificada
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if not images:
        print("Nenhuma imagem encontrada na pasta especificada.")
        return

    # Ajusta cada imagem e salva na pasta de saída
    for image in images:
        image_path = os.path.join(folder_path, image)
        adjust_image(image_path, output_folder, logo_path, target_ratio, position)

if __name__ == "__main__":
    # Define a pasta de entrada
    folder_path = "W:\\wallpapers"
    # Define se a logo deve ser adicionada ou não
    add_logo = True  # Altere para False se não quiser adicionar a logo
    # Define a proporção desejada (21, 9) ou (16, 9)
    target_ratio = (21, 9)  # Altere para (16, 9) se desejar
    # Define a posição para adicionar espaço extra ou cortar a imagem ('left', 'right', 'center')
    position = 'left'  # Altere para 'right' ou 'center' conforme necessário
    main(folder_path, add_logo, target_ratio, position)