import os
from PIL import Image

# Função para ajustar a imagem
def adjust_image(image_path, output_folder):
    # Define a largura e altura desejadas
    target_width = 2560
    target_height = 1080

    # Abre a imagem
    image = Image.open(image_path)
    original_width, original_height = image.size

    # Verifica se a altura da imagem é 1080px
    if original_height != target_height:
        print(f"Imagem ignorada (altura diferente de 1080px): {image_path}")
        return

    # Obtém a cor do primeiro pixel à esquerda da imagem
    extra_color = image.getpixel((0, 0))
    
    # Cria uma nova imagem com a cor extra
    new_image = Image.new("RGB", (target_width, target_height), extra_color)
    
    # Cola a imagem original à direita
    new_image.paste(image, (target_width - original_width, 0))
    
    # Salva a imagem ajustada na pasta de saída no formato JPG
    adjusted_image_path = os.path.join(output_folder, os.path.splitext(os.path.basename(image_path))[0] + ".jpg")
    new_image.save(adjusted_image_path, "JPEG")
    print(f"Imagem ajustada: {adjusted_image_path}")

# Função principal
def main(folder_path):
    # Define a pasta de saída
    output_folder = os.path.join(folder_path, "adjusted_wallpapers")
    os.makedirs(output_folder, exist_ok=True)

    # Obtém todas as imagens na pasta especificada
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if not images:
        print("Nenhuma imagem encontrada na pasta especificada.")
        return

    # Ajusta cada imagem e salva na pasta de saída
    for image in images:
        image_path = os.path.join(folder_path, image)
        adjust_image(image_path, output_folder)

if __name__ == "__main__":
    # Define a pasta de entrada
    folder_path = "W:\\wallpapers"
    main(folder_path)